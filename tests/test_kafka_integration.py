import asyncio
import sys
import types
import uuid

from src.messaging.kafka_client import get_inmemory_broker


def test_workflow_request_triggers_orchestrator(monkeypatch):
    broker = get_inmemory_broker()

    # Capture calls to the orchestrator
    calls = []

    def fake_execute_workflow_run(run_id, workflow_obj, payload):
        calls.append({"run_id": run_id, "workflow_id": workflow_obj.get("id"), "payload": payload})

    # Patch the celery_tasks module with a simple module object
    fake_mod = types.SimpleNamespace(execute_workflow_run=fake_execute_workflow_run)
    monkeypatch.setitem(sys.modules, "src.orchestrator.celery_tasks", fake_mod)

    async def main():
        # Start the worker in background
        from src.orchestrator.kafka_worker import run_worker

        worker_task = asyncio.create_task(run_worker(backend="inmemory", stop_after=1.0))

        # Give the worker a moment to start
        await asyncio.sleep(0.05)

        # Publish a workflow request event
        prod = broker.create_producer()
        run_id = str(uuid.uuid4())
        workflow_id = "test-wf"
        event = {"type": "workflow.run.requested", "run_id": run_id, "workflow_id": workflow_id, "payload": {"foo": "bar"}}

        await prod.send("workflow-requests", event)

        await worker_task

        return run_id, workflow_id

    run_id, workflow_id = asyncio.run(main())

    assert len(calls) == 1
    assert calls[0]["run_id"] == run_id
    assert calls[0]["workflow_id"] == workflow_id
    assert calls[0]["payload"] == {"foo": "bar"}
