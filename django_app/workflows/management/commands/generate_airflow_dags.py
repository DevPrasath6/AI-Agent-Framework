from django.core.management.base import BaseCommand
from django.conf import settings
import os
from pathlib import Path

from django_app.workflows.models import Workflow
from src.orchestrator.airflow_integration import generate_airflow_dag_file
from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType


class Command(BaseCommand):
    help = "Generate Airflow DAG files from workflow definitions"

    def add_arguments(self, parser):
        parser.add_argument(
            '--workflow-id',
            type=str,
            help='Generate DAG for specific workflow ID'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default='airflow_dags',
            help='Output directory for DAG files (default: airflow_dags)'
        )
        parser.add_argument(
            '--schedule-interval',
            type=str,
            help='Airflow schedule interval (e.g., "@daily", "0 0 * * *")'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output_dir'])
        output_dir.mkdir(exist_ok=True)

        workflow_id = options.get('workflow_id')
        schedule_interval = options.get('schedule_interval')

        if workflow_id:
            workflows = Workflow.objects.filter(id=workflow_id)
            if not workflows.exists():
                self.stdout.write(
                    self.style.ERROR(f'Workflow {workflow_id} not found')
                )
                return
        else:
            workflows = Workflow.objects.all()

        generated_count = 0

        for workflow in workflows:
            try:
                # Parse workflow definition
                import json
                try:
                    workflow_dict = json.loads(workflow.yaml_definition)
                except json.JSONDecodeError:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Skipping {workflow.name} - invalid JSON definition'
                        )
                    )
                    continue

                # Convert to WorkflowDefinition
                workflow_def = self._dict_to_workflow_definition(workflow_dict, workflow)

                # Generate DAG file
                dag_filename = f"{workflow.id}.py"
                output_path = output_dir / dag_filename

                success = generate_airflow_dag_file(
                    workflow_def,
                    str(output_path),
                    dag_id=f"ai_framework_{workflow.id}",
                    schedule_interval=schedule_interval
                )

                if success:
                    generated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Generated DAG: {output_path}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Failed to generate DAG for {workflow.name}'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error processing {workflow.name}: {str(e)}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Generated {generated_count} Airflow DAG files in {output_dir}'
            )
        )

    def _dict_to_workflow_definition(self, workflow_dict: dict, workflow_model) -> WorkflowDefinition:
        """Convert a dictionary to WorkflowDefinition."""
        steps = []
        for step_dict in workflow_dict.get('steps', []):
            step = WorkflowStep(
                id=step_dict.get('id'),
                name=step_dict.get('name', step_dict.get('id')),
                step_type=StepType(step_dict.get('step_type', 'agent')),
                config=step_dict.get('config', {}),
                dependencies=step_dict.get('dependencies', []),
                condition=step_dict.get('condition')
            )
            steps.append(step)

        return WorkflowDefinition(
            id=str(workflow_model.id),
            name=workflow_model.name,
            description=workflow_dict.get('description', ''),
            steps=steps,
            metadata=workflow_dict.get('metadata', {})
        )
