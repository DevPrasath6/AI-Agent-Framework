import json
from django.conf import settings

try:
    from kafka import KafkaProducer
except Exception:
    KafkaProducer = None

producer = None


def _get_producer():
    global producer
    if KafkaProducer is None:
        return None
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return producer


def enqueue_workflow_run(run_id: str, workflow_id: str, payload: dict):
    p = _get_producer()
    event = {
        "type": "workflow.run.requested",
        "run_id": run_id,
        "workflow_id": workflow_id,
        "payload": payload,
    }
    if p is not None:
        p.send("workflow-requests", event)
        p.flush()
        return
    # Fallback: call in-process orchestrator
    try:
        from src.orchestrator.celery_tasks import execute_workflow_run

        try:
            execute_workflow_run.delay(run_id, {"id": str(workflow_id)}, payload)
        except Exception:
            execute_workflow_run(run_id, {"id": str(workflow_id)}, payload)
    except Exception:
        # Last resort: write to a local file for debugging
        with open("/tmp/workflow_event_%s.json" % run_id, "w") as f:
            json.dump(event, f)


def enqueue_agent_run(run_id: str, agent_id: str, payload: dict):
    p = _get_producer()
    event = {
        "type": "agent.run.requested",
        "run_id": run_id,
        "agent_id": str(agent_id),
        "payload": payload,
    }
    if p is not None:
        p.send("agent-requests", event)
        p.flush()
        return
    try:
        from src.orchestrator.celery_tasks import execute_agent_run

        try:
            execute_agent_run.delay(run_id, str(agent_id), payload)
        except Exception:
            execute_agent_run(run_id, str(agent_id), payload)
    except Exception:
        with open("/tmp/agent_event_%s.json" % run_id, "w") as f:
            json.dump(event, f)
