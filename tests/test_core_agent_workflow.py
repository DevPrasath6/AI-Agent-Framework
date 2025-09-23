import asyncio

from src.core.agent_base import SimpleAgent
from src.core.workflow_base import (
    WorkflowDefinition,
    WorkflowStep,
    StepType,
    SimpleDAGWorkflow,
)


def test_simple_agent_run_sync():
    agent = SimpleAgent(
        name="echo_agent", processor_func=lambda inp, ctx: {"echo": inp}
    )
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(agent.run("hello"))
    assert res["status"] == "completed" or res["status"] == "completed"
    assert res["output"]["echo"] == "hello"


def test_simple_dag_workflow_execution():
    # Two-step workflow where step1 produces output consumed by step2
    def step1_func(inp, ctx):
        return {"step1": "ok", "value": 42}

    def step2_func(inp, ctx):
        # Expect input from step1
        return {"step2": "ok", "value_from_prev": inp.get("value")}

    agent1 = SimpleAgent(name="a1", processor_func=step1_func)
    agent2 = SimpleAgent(name="a2", processor_func=step2_func)

    wf_def = WorkflowDefinition(
        id="test_wf",
        name="Test WF",
        description="",
        steps=[
            WorkflowStep(
                id="s1",
                name="step1",
                step_type=StepType.AGENT,
                config={"agent_name": "a1"},
                dependencies=[],
            ),
            WorkflowStep(
                id="s2",
                name="step2",
                step_type=StepType.AGENT,
                config={"agent_name": "a2"},
                dependencies=["s1"],
            ),
        ],
    )

    wf = SimpleDAGWorkflow(
        definition=wf_def, agent_registry={"a1": agent1, "a2": agent2}
    )
    ctx = wf.create_execution_context({"input": "x"})

    # run the async execute method synchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(wf.execute({"input": "x"}, ctx))
    assert result is not None
    # ensure execution_history entry present
    assert len(wf.execution_history) >= 1


if __name__ == "__main__":
    test_simple_agent_run_sync()
    test_simple_dag_workflow_execution()
