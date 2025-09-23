"""Simple async Kafka consumer worker for testing.

Uses the `src.messaging.kafka_client` factories to obtain consumers for
`workflow-requests` and `agent-requests`. Events are dispatched to the
orchestrator Celery task functions but those are imported at handling time
to avoid import-time side-effects during tests.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from src.messaging.kafka_client import get_consumer

logger = logging.getLogger(__name__)


async def _handle_workflow_event(ev: Any):
    try:
        # Import here so tests can monkeypatch sys.modules before the import
        from src.orchestrator.celery_tasks import execute_workflow_run

        run_id = ev.get("run_id")
        workflow_id = ev.get("workflow_id")
        payload = ev.get("payload")
        try:
            execute_workflow_run.delay(run_id, {"id": str(workflow_id)}, payload)
        except Exception:
            execute_workflow_run(run_id, {"id": str(workflow_id)}, payload)
    except Exception as err:
        logger.exception("Failed to handle workflow event: %s", err)


async def _handle_agent_event(ev: Any):
    try:
        from src.orchestrator.celery_tasks import execute_agent_run

        run_id = ev.get("run_id")
        agent_id = ev.get("agent_id")
        payload = ev.get("payload")
        try:
            execute_agent_run.delay(run_id, str(agent_id), payload)
        except Exception:
            execute_agent_run(run_id, str(agent_id), payload)
    except Exception as err:
        logger.exception("Failed to handle agent event: %s", err)


async def run_worker(backend: str = "inmemory", bootstrap_servers: str | None = None, *, stop_after: float | None = None):
    """Run the consumer loop. Callers may start this in background for tests.

    If `stop_after` is provided the worker will exit after that many
    seconds; useful for integration tests.
    """
    consumer_wf = await get_consumer(backend=backend, topic="workflow-requests", bootstrap_servers=bootstrap_servers)
    consumer_ag = await get_consumer(backend=backend, topic="agent-requests", bootstrap_servers=bootstrap_servers)

    async def _consume_one(consumer, handler):
        async for ev in consumer:
            try:
                await handler(ev)
            except Exception:
                logger.exception("Handler raised an exception for event: %s", ev)

    tasks = [asyncio.create_task(_consume_one(consumer_wf, _handle_workflow_event)), asyncio.create_task(_consume_one(consumer_ag, _handle_agent_event))]

    if stop_after is not None:
        await asyncio.sleep(stop_after)
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        return

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run_worker())
