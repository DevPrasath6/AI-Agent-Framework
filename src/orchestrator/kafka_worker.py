import json
import time
from threading import Thread
from typing import Callable

try:
    from kafka import KafkaConsumer
except Exception:
    KafkaConsumer = None

from django.conf import settings
from .celery_tasks import execute_agent_run, execute_workflow_run


def _handle_message(msg: dict):
    t = msg.get("type")
    if t == "agent.run.requested":
        run_id = msg.get("run_id")
        agent_id = msg.get("agent_id") or msg.get("agent")
        payload = msg.get("payload", {})
        if execute_agent_run:
            try:
                execute_agent_run.delay(run_id, str(agent_id), payload)
            except Exception:
                execute_agent_run(run_id, str(agent_id), payload)
    elif t == "workflow.run.requested":
        run_id = msg.get("run_id")
        workflow_id = msg.get("workflow_id")
        payload = msg.get("payload", {})
        # In this setup we expect the workflow definition to be loaded by id elsewhere.
        # For now, pass a minimal wrapper
        wf_def = {"id": workflow_id, "input": payload}
        try:
            execute_workflow_run.delay(run_id, wf_def, payload)
        except Exception:
            execute_workflow_run(run_id, wf_def, payload)


def run_kafka_worker(
    bootstrap_servers: str = None, topics=None, group_id: str = "ai-agent-framework"
):
    if KafkaConsumer is None:
        print("kafka-python not available; kafka worker disabled")
        return
    bootstrap_servers = bootstrap_servers or getattr(
        settings, "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
    )
    topics = topics or ["agent-requests", "workflow-requests"]
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id=group_id,
        auto_offset_reset="earliest",
    )
    print("Kafka worker listening on", topics)
    try:
        for msg in consumer:
            try:
                _handle_message(msg.value)
            except Exception as e:
                print("Error handling message", e)
    finally:
        consumer.close()


def start_in_thread(**kwargs):
    t = Thread(target=run_kafka_worker, kwargs=kwargs, daemon=True)
    t.start()
    return t
