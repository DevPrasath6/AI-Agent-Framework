import logging
from django.conf import settings

from src.messaging.kafka_client import get_producer

logger = logging.getLogger(__name__)


def _producer_backend():
    # Use settings to decide backend; default to in-memory for tests
    return getattr(settings, "KAFKA_BACKEND", "inmemory")


async def _send_event(topic: str, event: dict) -> None:
    try:
        prod = await get_producer(backend=_producer_backend(), bootstrap_servers=getattr(settings, "KAFKA_BOOTSTRAP_SERVERS", None))
        await prod.send(topic, event)
    except Exception as err:
        # Log and fallback to direct call
        logger.debug("Failed to send event to kafka (%s): %s", topic, err)
        raise


def enqueue_workflow_run(run_id: str, workflow_id: str, payload: dict):
    event = {
        "type": "workflow.run.requested",
        "run_id": run_id,
        "workflow_id": workflow_id,
        "payload": payload,
    }

    try:
        # Try to publish asynchronously to the configured backend
        import asyncio

        asyncio.get_event_loop().run_until_complete(_send_event("workflow-requests", event))
        return
    except Exception:
        # Fallback: call in-process orchestrator
        try:
            from src.orchestrator.celery_tasks import execute_workflow_run

            try:
                execute_workflow_run.delay(run_id, {"id": str(workflow_id)}, payload)
            except Exception:
                execute_workflow_run(run_id, {"id": str(workflow_id)}, payload)
            return
        except Exception as err:
            logger.debug("Fallback orchestrator call failed: %s", err)


def enqueue_agent_run(run_id: str, agent_id: str, payload: dict):
    event = {
        "type": "agent.run.requested",
        "run_id": run_id,
        "agent_id": str(agent_id),
        "payload": payload,
    }

    try:
        import asyncio

        asyncio.get_event_loop().run_until_complete(_send_event("agent-requests", event))
        return
    except Exception:
        try:
            from src.orchestrator.celery_tasks import execute_agent_run

            try:
                execute_agent_run.delay(run_id, str(agent_id), payload)
            except Exception:
                execute_agent_run(run_id, str(agent_id), payload)
            return
        except Exception as err:
            logger.debug("Fallback orchestrator agent call failed: %s", err)
