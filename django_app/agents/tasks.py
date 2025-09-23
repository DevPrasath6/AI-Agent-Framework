from celery import shared_task
from .models import AgentRun
from ..workflows.adapters import enqueue_agent_run


@shared_task
def submit_agent_run(agent_run_id):
    run = AgentRun.objects.get(id=agent_run_id)
    enqueue_agent_run(str(run.id), str(run.agent.id), run.input_payload)
    run.status = "ENQUEUED"
    run.save()
