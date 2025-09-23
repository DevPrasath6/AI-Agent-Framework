try:
    from celery import shared_task
except Exception:
    # Provide a no-op decorator when Celery is not importable so the module
    # can be imported during tests without requiring Celery to be present.
    def shared_task(func=None, **kwargs):
        if func is None:

            def _wrap(f):
                return f

            return _wrap
        return func


from typing import Any
import asyncio
import uuid
from src.core.workflow_base import (
    SimpleDAGWorkflow,
    WorkflowDefinition,
    WorkflowStep,
    StepType,
)
from src.sdk.agents import get_agent, list_agents
from src.sdk.tools import get_tool
from src.state_memory.persistence import save_record


def _run_async(coro):
    try:
        return asyncio.get_event_loop().run_until_complete(coro)
    except RuntimeError:
        return asyncio.new_event_loop().run_until_complete(coro)


def _workflow_from_dict(defn: dict) -> SimpleDAGWorkflow:
    """Convert a dict workflow definition into a SimpleDAGWorkflow instance."""
    try:
        steps = []
        for s in (
            defn.get("steps", []) if isinstance(defn.get("steps", []), list) else []
        ):
            step_id = s.get("id") or s.get("name") or str(uuid.uuid4())
            name = s.get("name", step_id)
            stype = s.get("step_type") or s.get("type") or "agent"
            try:
                stype_enum = (
                    StepType(stype) if isinstance(stype, StepType) else StepType(stype)
                )
            except Exception:
                # default to AGENT
                stype_enum = StepType.AGENT
            config = s.get("config", {})
            deps = s.get("dependencies", []) or []
            steps.append(
                WorkflowStep(
                    id=step_id,
                    name=name,
                    step_type=stype_enum,
                    config=config,
                    dependencies=deps,
                )
            )

        wf_def = WorkflowDefinition(
            id=str(defn.get("id") or defn.get("name") or str(uuid.uuid4())),
            name=defn.get("name", "workflow"),
            description=defn.get("description", ""),
            steps=steps,
            metadata=defn.get("metadata", {}),
        )
        return SimpleDAGWorkflow(wf_def)
    except Exception:
        # Last-resort: create minimal empty workflow
        wf_def = WorkflowDefinition(
            id=str(defn.get("id", str(uuid.uuid4()))),
            name=str(defn.get("name", "workflow")),
            description="",
            steps=[],
        )
        return SimpleDAGWorkflow(wf_def)


@shared_task
def execute_workflow_run(run_id: str, workflow_def: dict, payload: dict):
    """Execute a workflow definition (dict) with the provided payload.

    This task is intentionally simple: it constructs a SimpleDAGWorkflow
    from the provided dict (assuming it was serialized) and runs it in-process.
    """
    # If workflow_def is a simple identifier, try loading the full definition
    wf_obj = None
    try:
        wf_id = None
        if isinstance(workflow_def, dict):
            wf_id = workflow_def.get("id")
        elif isinstance(workflow_def, str):
            wf_id = workflow_def

        if wf_id:
            # Try to load Django model if available
            try:
                from django_app.workflows.models import Workflow as DjangoWorkflow

                wf_model = DjangoWorkflow.objects.filter(id=wf_id).first()
                if wf_model:
                    # Attempt to parse YAML or JSON from yaml_definition
                    import json

                    try:
                        defn = json.loads(wf_model.yaml_definition)
                    except Exception:
                        # Fall back to a minimal wrapper
                        defn = {
                            "id": str(wf_model.id),
                            "name": wf_model.name,
                            "steps": [],
                        }
                    wf_obj = _workflow_from_dict(defn)
            except Exception:
                wf_obj = None

    except Exception:
        wf_obj = None

    if wf_obj is None:
        # Try to build from provided definition directly
        if isinstance(workflow_def, SimpleDAGWorkflow):
            wf_obj = workflow_def
        else:
            try:
                if isinstance(workflow_def, dict):
                    wf_obj = _workflow_from_dict(workflow_def)
                else:
                    wf_obj = (
                        SimpleDAGWorkflow.from_definition(workflow_def)
                        if hasattr(SimpleDAGWorkflow, "from_definition")
                        else SimpleDAGWorkflow(workflow_def)
                    )
            except Exception:
                # Final fallback: wrap minimal definition
                wf_obj = _workflow_from_dict(
                    workflow_def
                    if isinstance(workflow_def, dict)
                    else {
                        "id": str(workflow_def),
                        "name": str(workflow_def),
                        "steps": [],
                    }
                )

    # Create execution context and run synchronously via asyncio
    ctx = (
        wf_obj.create_execution_context(payload)
        if hasattr(wf_obj, "create_execution_context")
        else None
    )
    if asyncio.iscoroutinefunction(wf_obj.execute):
        result = _run_async(wf_obj.execute(payload, ctx))
    else:
        result = wf_obj.execute(payload, ctx)
    # persist run result for visibility
    persisted = False
    try:
        # If Django models are available, update the WorkflowRun record
        from django.apps import apps as _apps

        DjangoWorkflowRun = _apps.get_model("workflows", "WorkflowRun")
        try:
            wr = DjangoWorkflowRun.objects.filter(id=run_id).first()
            if not wr:
                try:
                    import uuid as _uuid

                    wr = DjangoWorkflowRun.objects.filter(
                        id=_uuid.UUID(str(run_id))
                    ).first()
                except Exception:
                    wr = DjangoWorkflowRun.objects.filter(id=str(run_id)).first()

            if wr:
                # Serialize WorkflowExecutionResult into JSON-friendly dict
                try:
                    ser = {
                        "workflow_id": getattr(result, "workflow_id", None),
                        "execution_id": getattr(result, "execution_id", None),
                        "status": getattr(result, "status", None).value
                        if getattr(result, "status", None)
                        else None,
                        "start_time": getattr(result, "start_time", None).isoformat()
                        if getattr(result, "start_time", None)
                        else None,
                        "end_time": getattr(result, "end_time", None).isoformat()
                        if getattr(result, "end_time", None)
                        else None,
                        "duration": getattr(result, "duration", None),
                        "output": getattr(result, "output", None),
                        "error": getattr(result, "error", None),
                        "step_results": getattr(result, "step_results", None),
                    }
                except Exception:
                    ser = {"output": result}

                wr.result = ser
                wr.status = "COMPLETED"
                wr.save()
                persisted = True
        except Exception:
            # don't let DB problems break the task
            persisted = False
    except Exception:
        persisted = False

    if not persisted:
        try:
            save_record("workflow_runs", {"run_id": run_id, "result": result})
        except Exception:
            pass

    return result


@shared_task
def execute_agent_run(run_id: str, agent_name: str, payload: dict):
    # Resolve agent by name or id
    agent = get_agent(agent_name)
    if agent is None:
        # Try lookup by id across registered agents
        for key in list_agents():
            a = get_agent(key)
            try:
                if getattr(a, "id", None) == agent_name or str(
                    getattr(a, "id", "")
                ) == str(agent_name):
                    agent = a
                    break
            except Exception:
                continue

    if agent is None:
        return {"error": "agent_not_found"}

    try:
        # Run agent (agent.run may be async)
        if asyncio.iscoroutinefunction(agent.run):
            result = _run_async(agent.run(payload))
        else:
            result = agent.run(payload)
        # persist into Django AgentRun if possible
        persisted = False
        try:
            from django.apps import apps as _apps

            DjangoAgentRun = _apps.get_model("agents", "AgentRun")
            try:
                ar = DjangoAgentRun.objects.filter(id=run_id).first()
                # handle string UUIDs or different types
                if not ar:
                    try:
                        import uuid as _uuid

                        ar = DjangoAgentRun.objects.filter(
                            id=_uuid.UUID(str(run_id))
                        ).first()
                    except Exception:
                        ar = DjangoAgentRun.objects.filter(id=str(run_id)).first()

                if ar:
                    ar.output = result
                    ar.status = "COMPLETED"
                    ar.save()
                    persisted = True
            except Exception:
                persisted = False
        except Exception:
            persisted = False

        if not persisted:
            try:
                save_record(
                    "agent_runs",
                    {"run_id": run_id, "agent": agent_name, "result": result},
                )
            except Exception:
                pass

        return result
    except Exception as e:
        # attempt to set status=FAILED in DB if possible
        try:
            from django.apps import apps as _apps

            DjangoWorkflowRun = _apps.get_model("workflows", "WorkflowRun")
            try:
                wr = DjangoWorkflowRun.objects.filter(id=run_id).first()
                if not wr:
                    try:
                        import uuid as _uuid

                        wr = DjangoWorkflowRun.objects.filter(
                            id=_uuid.UUID(str(run_id))
                        ).first()
                    except Exception:
                        wr = DjangoWorkflowRun.objects.filter(id=str(run_id)).first()

                if wr:
                    wr.result = {"error": str(e)}
                    wr.status = "FAILED"
                    wr.save()
            except Exception:
                pass
        except Exception:
            pass
        try:
            from django.apps import apps as _apps

            DjangoAgentRun = _apps.get_model("agents", "AgentRun")
            try:
                ar = DjangoAgentRun.objects.filter(id=run_id).first()
                if not ar:
                    try:
                        import uuid as _uuid

                        ar = DjangoAgentRun.objects.filter(
                            id=_uuid.UUID(str(run_id))
                        ).first()
                    except Exception:
                        ar = DjangoAgentRun.objects.filter(id=str(run_id)).first()

                if ar:
                    ar.output = {"error": str(e)}
                    ar.status = "FAILED"
                    ar.save()
            except Exception:
                pass
        except Exception:
            pass
        return {"error": str(e)}
