import asyncio
import uuid
import sys
import types

from src.messaging.kafka_client import get_inmemory_broker, InMemoryBroker


def test_adapter_falls_back_to_orchestrator(monkeypatch):
    """If the producer fails to send, adapter should fallback to orchestrator task."""
    # Use a fresh broker for this test to avoid interference
    fresh_broker = InMemoryBroker()

    # Replace the global broker temporarily
    monkeypatch.setattr("src.messaging.kafka_client._GLOBAL_INMEM_BROKER", fresh_broker)

    # Simulate get_producer raising
    async def fake_get_producer(*args, **kwargs):
        raise RuntimeError("connection failed")

    monkeypatch.setitem(sys.modules, "src.messaging.kafka_client", sys.modules["src.messaging.kafka_client"])
    monkeypatch.setattr("src.messaging.kafka_client.get_producer", fake_get_producer)

    calls = []

    def fake_execute_workflow_run(run_id, workflow_obj, payload):
        calls.append((run_id, workflow_obj, payload))

    # Patch orchestrator module
    fake_mod = types.SimpleNamespace(execute_workflow_run=fake_execute_workflow_run)
    monkeypatch.setitem(sys.modules, "src.orchestrator.celery_tasks", fake_mod)

    # Call adapter enqueue_workflow_run which should attempt producer then fallback
    from django_app.workflows.adapters import enqueue_workflow_run

    run_id = str(uuid.uuid4())
    enqueue_workflow_run(run_id, "wf1", {"a": 1})

    assert len(calls) == 1
    assert calls[0][0] == run_id


def test_worker_continues_after_handler_exception(monkeypatch):
    """Consumer should keep processing after one handler raises an exception."""
    # Use a fresh broker for this test to avoid interference
    fresh_broker = InMemoryBroker()

    # Replace the global broker temporarily
    monkeypatch.setattr("src.messaging.kafka_client._GLOBAL_INMEM_BROKER", fresh_broker)

    prod = fresh_broker.create_producer()

    processed = []

    async def failing_handler(ev):
        if ev.get("payload", {}).get("bad"):
            raise RuntimeError("handler failure")
        processed.append(ev.get("run_id"))

    # Patch kafka_worker handlers to use failing_handler for workflow events
    from src.orchestrator import kafka_worker as kw

    monkeypatch.setattr(kw, "_handle_workflow_event", failing_handler)

    async def main():
        # Start worker for a longer time to ensure messages are processed
        task = asyncio.create_task(kw.run_worker(backend="inmemory", stop_after=1.0))
        await asyncio.sleep(0.1)  # Give worker time to start

        # Send a bad message that causes handler to raise
        await prod.send("workflow-requests", {"run_id": "r1", "payload": {"bad": True}})
        # Send a good message that should be processed
        await prod.send("workflow-requests", {"run_id": "r2", "payload": {"good": True}})

        # Give more time for messages to be processed
        await asyncio.sleep(0.2)

        await task

    asyncio.run(main())

    assert "r2" in processed
