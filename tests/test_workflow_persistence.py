from django.test import TestCase
import uuid

from src.orchestrator.celery_tasks import execute_workflow_run
from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType
from django.apps import apps


class WorkflowPersistenceTest(TestCase):
    def setUp(self):
        # create a minimal workflow record and WorkflowRun placeholder
        Workflow = apps.get_model("workflows", "Workflow")
        WorkflowRun = apps.get_model("workflows", "WorkflowRun")

        self.wf = Workflow.objects.create(name="test-workflow", yaml_definition="{}")
        self.run_id = uuid.uuid4()
        self.wfr = WorkflowRun.objects.create(
            id=self.run_id, workflow=self.wf, input={}
        )

    def test_execute_workflow_run_updates_workflowrun(self):
        # Build a minimal workflow def that returns input using a condition step
        defn = {
            "id": str(self.wf.id),
            "name": self.wf.name,
            "steps": [
                {
                    "id": "s1",
                    "name": "return_input",
                    "step_type": "condition",
                    "config": {"condition": "True", "true_value": {"returned": True}},
                    "dependencies": [],
                }
            ],
        }

        result = execute_workflow_run(str(self.run_id), defn, {"x": 1})

        # Reload and assert
        wfr = apps.get_model("workflows", "WorkflowRun").objects.get(id=self.run_id)
        self.assertEqual(wfr.status, "COMPLETED")
        self.assertIsNotNone(wfr.result)
