"""Simple scheduler that enqueues workflow/agent runs.

This scheduler will prefer Celery if available; otherwise it will execute
work locally using the dag_executor.
"""

from typing import Any

try:
    from src.orchestrator.celery_tasks import execute_workflow_run, execute_agent_run
except Exception:
    execute_workflow_run = None
    execute_agent_run = None

from .dag_executor import execute_dag


def schedule_workflow(run_id: str, workflow_def: Any, payload: dict) -> Any:
    if execute_workflow_run is not None:
        try:
            return execute_workflow_run.delay(run_id, workflow_def, payload)
        except Exception:
            return execute_workflow_run(run_id, workflow_def, payload)
    # Fallback
    return execute_dag(workflow_def if workflow_def else {"input": payload})


def schedule_agent(run_id: str, agent_name: str, payload: dict) -> Any:
    if execute_agent_run is not None:
        try:
            return execute_agent_run.delay(run_id, agent_name, payload)
        except Exception:
            return execute_agent_run(run_id, agent_name, payload)
    # If no Celery, try a direct in-process call via execute_agent_run function if available
    if execute_agent_run is not None:
        return execute_agent_run(run_id, agent_name, payload)
    return {"status": "scheduled_local", "agent": agent_name}
