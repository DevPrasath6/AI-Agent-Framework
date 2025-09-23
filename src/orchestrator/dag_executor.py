"""Lightweight DAG executor for development/testing.

This executor accepts either a dictionary workflow definition or a
`SimpleDAGWorkflow` instance and executes steps in topological order using
the SDK agent/tool registries. It is intended for local testing and will
not replace the full `SimpleDAGWorkflow` execution semantics (which are in
`src.core.workflow_base`).
"""
import asyncio
from typing import Any

from src.core.workflow_base import SimpleDAGWorkflow


def _run_async(coro):
    try:
        return asyncio.get_event_loop().run_until_complete(coro)
    except RuntimeError:
        return asyncio.new_event_loop().run_until_complete(coro)


def execute_dag(dag_def: Any, context: Any = None) -> Any:
    """Execute a DAG definition or SimpleDAGWorkflow.

    Returns the final output or an execution result object.
    """
    # If already a SimpleDAGWorkflow, delegate to its execute
    if isinstance(dag_def, SimpleDAGWorkflow):
        if asyncio.iscoroutinefunction(dag_def.execute):
            return _run_async(dag_def.execute(context.shared_data.get('workflow_input') if context else None, context))
        return dag_def.execute(context.shared_data.get('workflow_input') if context else None, context)

    # If a dict is provided, try to construct SimpleDAGWorkflow
    try:
        wf = SimpleDAGWorkflow.from_definition(dag_def) if hasattr(SimpleDAGWorkflow, 'from_definition') else SimpleDAGWorkflow(dag_def)
        ctx = wf.create_execution_context(dag_def.get('input') if isinstance(dag_def, dict) else None)
        if asyncio.iscoroutinefunction(wf.execute):
            return _run_async(wf.execute(dag_def.get('input') if isinstance(dag_def, dict) else None, ctx))
        return wf.execute(dag_def.get('input') if isinstance(dag_def, dict) else None, ctx)
    except Exception:
        # Last resort: return the provided input
        return {'status': 'noop', 'input': dag_def}
