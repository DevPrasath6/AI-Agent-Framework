"""
Apache Airflow integration for the AI Agent Framework.

This module provides utilities to convert workflow definitions into Airflow DAGs
and execute them using Airflow operators.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType

# Optional Airflow imports with graceful fallback
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.bash import BashOperator
    # Use EmptyOperator instead of deprecated DummyOperator
    try:
        from airflow.operators.empty import EmptyOperator as DummyOperator
    except ImportError:
        from airflow.operators.dummy import DummyOperator
    from airflow.utils.dates import days_ago
    AIRFLOW_AVAILABLE = True
except (ImportError, AttributeError, RuntimeError) as e:
    # Provide stub classes when Airflow is not installed or not compatible (e.g., Windows)
    DAG = None
    PythonOperator = None
    BashOperator = None
    DummyOperator = None
    days_ago = None
    AIRFLOW_AVAILABLE = False

logger = logging.getLogger(__name__)


class AirflowIntegration:
    """Converts AI Agent Framework workflows to Airflow DAGs."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def workflow_to_dag(
        self,
        workflow_def: WorkflowDefinition,
        dag_id: Optional[str] = None,
        schedule_interval: Optional[str] = None,
        start_date: Optional[datetime] = None,
        default_args: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """Convert a WorkflowDefinition to an Airflow DAG.

        Args:
            workflow_def: The workflow definition to convert
            dag_id: Override DAG ID (defaults to workflow.id)
            schedule_interval: Airflow schedule interval
            start_date: DAG start date
            default_args: Additional DAG arguments

        Returns:
            Airflow DAG object or None if Airflow unavailable
        """
        if not AIRFLOW_AVAILABLE:
            self.logger.warning("Airflow not available - returning None")
            return None

        # Set defaults
        dag_id = dag_id or workflow_def.id
        start_date = start_date or days_ago(1)
        schedule_interval = schedule_interval or None  # Manual trigger only

        default_dag_args = {
            'owner': 'ai-agent-framework',
            'depends_on_past': False,
            'email_on_failure': False,
            'email_on_retry': False,
            'retries': 1,
            'retry_delay': timedelta(minutes=5),
        }
        if default_args:
            default_dag_args.update(default_args)

        # Create the DAG
        dag = DAG(
            dag_id=dag_id,
            default_args=default_dag_args,
            description=workflow_def.description or f"Generated from {workflow_def.name}",
            schedule_interval=schedule_interval,
            start_date=start_date,
            catchup=False,
            tags=['ai-agent-framework', 'generated'],
        )

        # Create operators for each step
        operators = {}
        for step in workflow_def.steps:
            operator = self._create_operator_for_step(step, dag)
            operators[step.id] = operator

        # Set up dependencies
        for step in workflow_def.steps:
            if step.dependencies:
                for dep_id in step.dependencies:
                    if dep_id in operators:
                        operators[dep_id] >> operators[step.id]

        return dag

    def _create_operator_for_step(self, step: WorkflowStep, dag: Any) -> Any:
        """Create an Airflow operator for a workflow step."""
        if step.step_type == StepType.AGENT:
            return self._create_agent_operator(step, dag)
        elif step.step_type == StepType.TOOL:
            return self._create_tool_operator(step, dag)
        elif step.step_type == StepType.CONDITION:
            return self._create_condition_operator(step, dag)
        elif step.step_type == StepType.PARALLEL:
            return self._create_parallel_operator(step, dag)
        else:
            # Default to dummy operator
            return DummyOperator(
                task_id=step.id,
                dag=dag,
            )

    def _create_agent_operator(self, step: WorkflowStep, dag: Any) -> Any:
        """Create a PythonOperator for agent execution."""
        def execute_agent(**context):
            """Execute agent step."""
            from src.orchestrator.celery_tasks import execute_agent_run

            # Get input from previous tasks or DAG run conf
            input_data = context.get('dag_run').conf or {}
            agent_name = step.config.get('agent_name', 'default_agent')

            # Generate a run ID for tracking
            run_id = f"airflow_{context['dag_run'].run_id}_{step.id}"

            # Execute the agent
            result = execute_agent_run(run_id, agent_name, input_data)

            # Return result for downstream tasks
            return result

        return PythonOperator(
            task_id=step.id,
            python_callable=execute_agent,
            dag=dag,
            provide_context=True,
        )

    def _create_tool_operator(self, step: WorkflowStep, dag: Any) -> Any:
        """Create a PythonOperator for tool execution."""
        def execute_tool(**context):
            """Execute tool step."""
            from src.sdk.tools import get_tool

            # Get tool configuration
            tool_name = step.config.get('tool_name')
            tool_params = step.config.get('tool_params', {})

            if not tool_name:
                raise ValueError(f"Tool step {step.id} missing tool_name in config")

            # Get tool instance
            tool = get_tool(tool_name)
            if not tool:
                raise ValueError(f"Tool {tool_name} not found in registry")

            # Get input from previous tasks or DAG run conf
            input_data = context.get('dag_run').conf or {}

            # Execute the tool
            result = tool.execute(input_data, **tool_params)

            return result

        return PythonOperator(
            task_id=step.id,
            python_callable=execute_tool,
            dag=dag,
            provide_context=True,
        )

    def _create_condition_operator(self, step: WorkflowStep, dag: Any) -> Any:
        """Create a PythonOperator for conditional logic."""
        def evaluate_condition(**context):
            """Evaluate condition step."""
            from src.core.workflow_base import safe_eval_expr, EvalContext

            condition_expr = step.config.get('condition', 'True')
            input_data = context.get('dag_run').conf or {}

            # Create evaluation context
            eval_context = EvalContext(
                input=input_data,
                context={},
                step_results={},
                metadata={}
            )

            # Evaluate condition
            result = safe_eval_expr(condition_expr, eval_context)

            # Return result for branching
            return result

        return PythonOperator(
            task_id=step.id,
            python_callable=evaluate_condition,
            dag=dag,
            provide_context=True,
        )

    def _create_parallel_operator(self, step: WorkflowStep, dag: Any) -> Any:
        """Create a DummyOperator for parallel coordination."""
        return DummyOperator(
            task_id=step.id,
            dag=dag,
        )


def generate_airflow_dag_file(
    workflow_def: WorkflowDefinition,
    output_path: str,
    dag_id: Optional[str] = None,
    schedule_interval: Optional[str] = None
) -> bool:
    """Generate a standalone Airflow DAG file from a workflow definition.

    Args:
        workflow_def: The workflow definition
        output_path: Path to write the DAG file
        dag_id: Override DAG ID
        schedule_interval: Airflow schedule interval

    Returns:
        True if file was generated successfully
    """
    if not AIRFLOW_AVAILABLE:
        logger.warning("Airflow not available - cannot generate DAG file")
        return False

    integration = AirflowIntegration()
    dag = integration.workflow_to_dag(
        workflow_def,
        dag_id=dag_id,
        schedule_interval=schedule_interval
    )

    if not dag:
        return False

    # Generate Python code for the DAG
    dag_code = f'''"""
Auto-generated Airflow DAG from AI Agent Framework workflow.
Generated on: {datetime.now().isoformat()}
Original workflow: {workflow_def.name}
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago

# Import AI Agent Framework components
from src.orchestrator.celery_tasks import execute_agent_run
from src.sdk.tools import get_tool
from src.core.workflow_base import safe_eval_expr, EvalContext

# DAG configuration
default_args = {{
    'owner': 'ai-agent-framework',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}}

dag = DAG(
    '{dag_id or workflow_def.id}',
    default_args=default_args,
    description='{workflow_def.description or workflow_def.name}',
    schedule_interval={repr(schedule_interval)},
    start_date=days_ago(1),
    catchup=False,
    tags=['ai-agent-framework', 'generated'],
)

# Task definitions
'''

    # Add task definitions
    for step in workflow_def.steps:
        if step.step_type == StepType.AGENT:
            dag_code += _generate_agent_task_code(step)
        elif step.step_type == StepType.TOOL:
            dag_code += _generate_tool_task_code(step)
        else:
            dag_code += f'''
{step.id} = DummyOperator(
    task_id='{step.id}',
    dag=dag,
)
'''

    # Add dependencies
    dag_code += "\n# Task dependencies\n"
    for step in workflow_def.steps:
        if step.dependencies:
            for dep_id in step.dependencies:
                dag_code += f"{dep_id} >> {step.id}\n"

    # Write to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dag_code)
        logger.info(f"Generated Airflow DAG file: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to write DAG file: {e}")
        return False


def _generate_agent_task_code(step: WorkflowStep) -> str:
    """Generate Python code for an agent task."""
    agent_name = step.config.get('agent_name', 'default_agent')

    return f'''
def execute_{step.id}(**context):
    """Execute agent step: {step.name}"""
    input_data = context.get('dag_run').conf or {{}}
    run_id = f"airflow_{{context['dag_run'].run_id}}_{step.id}"
    return execute_agent_run(run_id, '{agent_name}', input_data)

{step.id} = PythonOperator(
    task_id='{step.id}',
    python_callable=execute_{step.id},
    dag=dag,
    provide_context=True,
)
'''


def _generate_tool_task_code(step: WorkflowStep) -> str:
    """Generate Python code for a tool task."""
    tool_name = step.config.get('tool_name', 'default_tool')
    tool_params = step.config.get('tool_params', {})

    return f'''
def execute_{step.id}(**context):
    """Execute tool step: {step.name}"""
    tool = get_tool('{tool_name}')
    if not tool:
        raise ValueError('Tool {tool_name} not found')
    input_data = context.get('dag_run').conf or {{}}
    return tool.execute(input_data, **{tool_params})

{step.id} = PythonOperator(
    task_id='{step.id}',
    python_callable=execute_{step.id},
    dag=dag,
    provide_context=True,
)
'''
