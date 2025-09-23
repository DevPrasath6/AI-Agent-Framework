from django.test import TestCase
import uuid

from src.orchestrator.celery_tasks import execute_agent_run

from src.sdk.agents import register_agent
from agents.models import Agent, AgentRun


class PersistenceTasksTest(TestCase):
    """Tests that orchestrator tasks persist results into Django models.

    This uses Django's TestCase which sets up a test database (sqlite by default)
    when run via `manage.py test`.
    """

    def setUp(self):
        self.agent = Agent.objects.create(name="test-agent")

        # Register a simple runtime agent implementation in the SDK so
        # orchestrator tasks can resolve and run it during tests.
        class DummyAgent:
            def __init__(self, name):
                self.name = name

            def run(self, payload):
                # simple echo result
                return {"echo": payload}

        register_agent(DummyAgent(self.agent.name))

    def test_execute_agent_run_updates_agentrun(self):
        # Create an AgentRun placeholder that the task should update
        run_id = uuid.uuid4()
        ar = AgentRun.objects.create(
            id=run_id, agent=self.agent, input_payload={"q": "hello"}
        )

        # Call the task directly (synchronously)
        payload = {"message": "hi"}
        execute_agent_run(str(run_id), self.agent.name, payload)

        # Reload from DB and assert
        ar.refresh_from_db()
        self.assertEqual(ar.status, "COMPLETED")
        # output may be a dict or other serializable result
        self.assertIsNotNone(ar.output)

    def test_execute_agent_run_handles_missing_agent(self):
        run_id = uuid.uuid4()
        ar = AgentRun.objects.create(
            id=run_id, agent=self.agent, input_payload={"q": "hello"}
        )
        res = execute_agent_run(str(run_id), "non-existent-agent", {"x": 1})
        self.assertEqual(res.get("error"), "agent_not_found")
        # ensure DB untouched (status still default PENDING)
        ar.refresh_from_db()
        self.assertEqual(ar.status, "PENDING")
