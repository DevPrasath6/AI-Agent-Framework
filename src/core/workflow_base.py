"""
Workflow base classes and execution framework.
"""

import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Callable
from enum import Enum
from dataclasses import dataclass

from .execution_context import ExecutionContext, ExecutionPhase
from .agent_base import AgentBase
from ..observability.audit_trail import AuditTrail


class WorkflowStatus(Enum):
    """Workflow execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class StepType(Enum):
    """Types of workflow steps."""

    AGENT = "agent"
    TOOL = "tool"
    CONDITION = "condition"
    PARALLEL = "parallel"
    HUMAN_INPUT = "human_input"
    DELAY = "delay"


@dataclass
class WorkflowStep:
    """Definition of a single workflow step."""

    id: str
    name: str
    step_type: StepType
    config: Dict[str, Any]
    dependencies: List[str] = None
    timeout: Optional[int] = None
    retry_count: int = 0
    condition: Optional[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""

    id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    metadata: Dict[str, Any] = None
    timeout: Optional[int] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class WorkflowExecutionResult:
    """Result of workflow execution."""

    def __init__(
        self,
        workflow_id: str,
        execution_id: str,
        status: WorkflowStatus,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        output: Any = None,
        error: Optional[str] = None,
        step_results: Optional[Dict[str, Any]] = None,
    ):
        self.workflow_id = workflow_id
        self.execution_id = execution_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.output = output
        self.error = error
        self.step_results = step_results or {}

        # Calculate duration
        if self.end_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
        else:
            self.duration = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the execution result to a JSON-friendly dict."""
        return {
            "workflow_id": self.workflow_id,
            "execution_id": self.execution_id,
            "status": self.status.value
            if isinstance(self.status, WorkflowStatus)
            else str(self.status),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration,
            "output": self.output,
            "error": self.error,
            "step_results": self.step_results,
        }


class WorkflowBase(ABC):
    """
    Base class for workflow execution engines.

    Supports DAG-based workflows with conditional logic,
    parallel execution, and error handling.
    """

    def __init__(
        self,
        definition: WorkflowDefinition,
        agent_registry: Optional[Dict[str, AgentBase]] = None,
        tool_registry: Optional[Dict[str, Callable]] = None,
    ):
        """
        Initialize workflow.

        Args:
            definition: Workflow definition with steps and configuration
            agent_registry: Registry of available agents
            tool_registry: Registry of available tools
        """
        self.definition = definition
        self.agent_registry = agent_registry or {}
        self.tool_registry = tool_registry or {}

        self.id = definition.id
        self.name = definition.name
        self.logger = logging.getLogger(f"workflow.{self.name}")
        self.audit_trail = AuditTrail(agent_id=f"workflow_{self.id}")

        # Execution tracking
        self.status = WorkflowStatus.PENDING
        self.current_execution_id = None
        self.execution_history: List[WorkflowExecutionResult] = []

        # Validate workflow definition
        self._validate_definition()

    async def execute(
        self,
        input_data: Any,
        context: Optional[ExecutionContext] = None,
        user_id: Optional[str] = None,
    ) -> WorkflowExecutionResult:
        """
        Execute the workflow.

        Args:
            input_data: Input data for the workflow
            context: Optional execution context
            user_id: Optional user ID for auditing

        Returns:
            Workflow execution result
        """
        execution_id = str(uuid.uuid4())
        start_time = datetime.utcnow()

        if context is None:
            context = ExecutionContext(workflow_id=self.id, user_id=user_id)

        context.start_execution()
        self.current_execution_id = execution_id
        self.status = WorkflowStatus.RUNNING

        try:
            self.logger.info(f"Starting workflow execution {execution_id}")

            # Log workflow start
            await self.audit_trail.log_execution_start(
                execution_id=execution_id,
                input_data=input_data,
                context=context.to_dict(),
            )

            # Execute workflow steps
            output = await self._execute_workflow(input_data, context)

            # Mark as completed
            self.status = WorkflowStatus.COMPLETED
            end_time = datetime.utcnow()
            context.end_execution()

            # Create result
            result = WorkflowExecutionResult(
                workflow_id=self.id,
                execution_id=execution_id,
                status=self.status,
                start_time=start_time,
                end_time=end_time,
                output=output,
                step_results=self._extract_step_results(context),
            )

            # Log completion
            await self.audit_trail.log_execution_complete(
                execution_id=execution_id, output_data=output, duration=result.duration
            )

            self.execution_history.append(result)
            self.logger.info(
                f"Workflow execution {execution_id} completed successfully"
            )

            return result

        except Exception as e:
            # Handle execution error
            self.status = WorkflowStatus.FAILED
            end_time = datetime.utcnow()
            error_msg = str(e)

            context.add_error("workflow_execution_error", error_msg)

            # Create error result
            result = WorkflowExecutionResult(
                workflow_id=self.id,
                execution_id=execution_id,
                status=self.status,
                start_time=start_time,
                end_time=end_time,
                error=error_msg,
                step_results=self._extract_step_results(context),
            )

            # Log error
            await self.audit_trail.log_execution_error(
                execution_id=execution_id, error=error_msg, duration=result.duration
            )

            self.execution_history.append(result)
            self.logger.error(f"Workflow execution {execution_id} failed: {error_msg}")

            return result

    @abstractmethod
    async def _execute_workflow(
        self, input_data: Any, context: ExecutionContext
    ) -> Any:
        """
        Execute the workflow logic.

        This method should be implemented by subclasses to define
        the specific workflow execution strategy (DAG, state machine, etc.)
        """
        pass

    async def cancel_execution(self) -> bool:
        """Cancel the current workflow execution."""
        if self.status == WorkflowStatus.RUNNING:
            self.status = WorkflowStatus.CANCELLED
            self.logger.info(
                f"Workflow execution {self.current_execution_id} cancelled"
            )
            return True
        return False

    async def pause_execution(self) -> bool:
        """Pause the current workflow execution."""
        if self.status == WorkflowStatus.RUNNING:
            self.status = WorkflowStatus.PAUSED
            self.logger.info(f"Workflow execution {self.current_execution_id} paused")
            return True
        return False

    async def resume_execution(self) -> bool:
        """Resume a paused workflow execution."""
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.RUNNING
            self.logger.info(f"Workflow execution {self.current_execution_id} resumed")
            return True
        return False

    def get_step_by_id(self, step_id: str) -> Optional[WorkflowStep]:
        """Get a workflow step by ID."""
        for step in self.definition.steps:
            if step.id == step_id:
                return step
        return None

    def get_dependencies(self, step_id: str) -> List[str]:
        """Get dependencies for a specific step."""
        step = self.get_step_by_id(step_id)
        return step.dependencies if step else []

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get workflow execution summary."""
        return {
            "workflow_id": self.id,
            "name": self.name,
            "status": self.status.value,
            "total_executions": len(self.execution_history),
            "current_execution_id": self.current_execution_id,
            "step_count": len(self.definition.steps),
            "agent_count": len(self.agent_registry),
            "tool_count": len(self.tool_registry),
            "success_rate": self._calculate_success_rate(),
            "average_duration": self._calculate_average_duration(),
        }

    def _validate_definition(self) -> None:
        """Validate the workflow definition."""
        if not self.definition.steps:
            raise ValueError("Workflow must have at least one step")

        step_ids = {step.id for step in self.definition.steps}

        # Check for duplicate step IDs
        if len(step_ids) != len(self.definition.steps):
            raise ValueError("Workflow steps must have unique IDs")

        # Check dependencies
        for step in self.definition.steps:
            for dep_id in step.dependencies:
                if dep_id not in step_ids:
                    raise ValueError(
                        f"Step {step.id} depends on non-existent step {dep_id}"
                    )

        # Check for circular dependencies (simple check)
        self._check_circular_dependencies()

    def _check_circular_dependencies(self) -> None:
        """Check for circular dependencies in workflow steps."""
        # Simple cycle detection using DFS
        visited = set()
        rec_stack = set()

        def has_cycle(step_id: str) -> bool:
            visited.add(step_id)
            rec_stack.add(step_id)

            step = self.get_step_by_id(step_id)
            if step:
                for dep_id in step.dependencies:
                    if dep_id not in visited:
                        if has_cycle(dep_id):
                            return True
                    elif dep_id in rec_stack:
                        return True

            rec_stack.remove(step_id)
            return False

        for step in self.definition.steps:
            if step.id not in visited:
                if has_cycle(step.id):
                    raise ValueError(
                        f"Circular dependency detected involving step {step.id}"
                    )

    def _extract_step_results(self, context: ExecutionContext) -> Dict[str, Any]:
        """Extract step results from execution context."""
        return {
            "intermediate_results": context.intermediate_results,
            "executed_tools": context.executed_tools,
            "executed_agents": context.executed_agents,
            "agent_outputs": context.agent_outputs,
            "step_timings": context.step_timings,
        }

    def _calculate_success_rate(self) -> float:
        """Calculate workflow success rate."""
        if not self.execution_history:
            return 0.0

        successful = sum(
            1
            for result in self.execution_history
            if result.status == WorkflowStatus.COMPLETED
        )
        return (successful / len(self.execution_history)) * 100

    def _calculate_average_duration(self) -> Optional[float]:
        """Calculate average execution duration."""
        durations = [
            result.duration
            for result in self.execution_history
            if result.duration is not None
        ]

        if not durations:
            return None

        return sum(durations) / len(durations)

    def create_execution_context(
        self, initial_shared: Optional[Any] = None, user_id: Optional[str] = None
    ) -> ExecutionContext:
        """Create a pre-populated ExecutionContext for this workflow.

        Args:
            initial_shared: Optional initial shared data (will be stored under
                the key `workflow_input`).
            user_id: Optional user id for audit purposes.

        Returns:
            ExecutionContext instance ready to be passed to `execute()`.
        """
        ctx = ExecutionContext(workflow_id=self.id, user_id=user_id)
        if initial_shared is not None:
            # Store initial input under a canonical key
            ctx.set_shared_data("workflow_input", initial_shared)
        return ctx


class SimpleDAGWorkflow(WorkflowBase):
    """
    Simple DAG-based workflow implementation.

    Executes workflow steps based on their dependencies,
    supporting parallel execution where possible.
    """

    async def _execute_workflow(
        self, input_data: Any, context: ExecutionContext
    ) -> Any:
        """Execute workflow using DAG execution strategy."""
        context.advance_phase(ExecutionPhase.AGENT_EXECUTION)

        # Build execution order based on dependencies
        execution_order = self._build_execution_order()

        # Track completed steps and their outputs
        completed_steps: Set[str] = set()
        step_outputs: Dict[str, Any] = {}

        # Set initial input
        context.set_shared_data("workflow_input", input_data)
        current_data = input_data

        # Execute steps in dependency order
        for step_batch in execution_order:
            if self.status == WorkflowStatus.CANCELLED:
                raise Exception("Workflow execution was cancelled")

            # Execute steps in parallel within each batch
            batch_results = await self._execute_step_batch(
                step_batch, current_data, context, step_outputs
            )

            # Update completed steps and outputs
            for step_id, output in batch_results.items():
                completed_steps.add(step_id)
                step_outputs[step_id] = output
                current_data = output  # Use last output as input for next batch

        # Return final output
        context.advance_phase(ExecutionPhase.OUTPUT_PROCESSING)
        return current_data

    def _build_execution_order(self) -> List[List[str]]:
        """Build execution order based on step dependencies."""
        # Topological sort to determine execution order
        in_degree = {}
        graph = {}

        # Initialize
        for step in self.definition.steps:
            in_degree[step.id] = len(step.dependencies)
            graph[step.id] = []

        # Build graph
        for step in self.definition.steps:
            for dep in step.dependencies:
                graph[dep].append(step.id)

        # Topological sort
        execution_order = []
        queue = [step_id for step_id, degree in in_degree.items() if degree == 0]

        while queue:
            # Current batch can execute in parallel
            current_batch = queue[:]
            execution_order.append(current_batch)
            queue = []

            # Process current batch
            for step_id in current_batch:
                for neighbor in graph[step_id]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

        return execution_order

    async def _execute_step_batch(
        self,
        step_ids: List[str],
        input_data: Any,
        context: ExecutionContext,
        previous_outputs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a batch of steps in parallel."""
        tasks = []

        for step_id in step_ids:
            step = self.get_step_by_id(step_id)
            if step:
                task = self._execute_single_step(
                    step, input_data, context, previous_outputs
                )
                tasks.append((step_id, task))

        # Execute all steps in parallel
        results = {}
        for step_id, task in tasks:
            try:
                result = await task
                results[step_id] = result
                context.add_intermediate_result(step_id, result)
            except Exception as e:
                self.logger.error(f"Step {step_id} failed: {e}")
                context.add_error("step_execution_error", f"Step {step_id}: {str(e)}")
                raise

        return results

    async def _execute_single_step(
        self,
        step: WorkflowStep,
        input_data: Any,
        context: ExecutionContext,
        previous_outputs: Dict[str, Any],
    ) -> Any:
        """Execute a single workflow step."""
        step_start_time = datetime.utcnow()

        try:
            # Prepare step input based on dependencies
            step_input = self._prepare_step_input(step, input_data, previous_outputs)

            # Execute based on step type
            if step.step_type == StepType.AGENT:
                result = await self._execute_agent_step(step, step_input, context)
            elif step.step_type == StepType.TOOL:
                result = await self._execute_tool_step(step, step_input, context)
            elif step.step_type == StepType.CONDITION:
                result = await self._execute_condition_step(step, step_input, context)
            else:
                raise ValueError(f"Unsupported step type: {step.step_type}")

            # Record timing
            duration = (datetime.utcnow() - step_start_time).total_seconds()
            context.record_step_timing(step.id, duration)

            return result

        except Exception:
            duration = (datetime.utcnow() - step_start_time).total_seconds()
            context.record_step_timing(step.id, duration)
            raise

    async def _execute_agent_step(
        self, step: WorkflowStep, input_data: Any, context: ExecutionContext
    ) -> Any:
        """Execute an agent step."""
        agent_name = step.config.get("agent_name")
        if not agent_name or agent_name not in self.agent_registry:
            raise ValueError(f"Agent {agent_name} not found in registry")

        agent = self.agent_registry[agent_name]
        # Run the agent (agent.run may be sync or async)
        if asyncio.iscoroutinefunction(agent.run):
            result = await agent.run(input_data, context)
        else:
            result = agent.run(input_data, context)

        output = result.get("output") if isinstance(result, dict) else result

        # Best-effort: create an AgentRun record in Django DB for observability
        try:
            from django.apps import apps as _apps

            AgentRunModel = _apps.get_model("agents", "AgentRun")
            # Try to locate agent model by name
            AgentModel = _apps.get_model("agents", "Agent")
            agent_obj = AgentModel.objects.filter(name=agent_name).first()
            # Create AgentRun only if we can identify the Agent
            if agent_obj:
                AgentRunModel.objects.create(
                    agent=agent_obj,
                    input_payload=input_data,
                    output=output,
                    status="COMPLETED",
                )
        except Exception:
            # If Django isn't available or DB write fails, ignore (best-effort)
            pass

        context.record_agent_execution(getattr(agent, "id", agent_name), output)
        return output

    async def _execute_tool_step(
        self, step: WorkflowStep, input_data: Any, context: ExecutionContext
    ) -> Any:
        """Execute a tool step."""
        tool_name = step.config.get("tool_name")
        if not tool_name or tool_name not in self.tool_registry:
            raise ValueError(f"Tool {tool_name} not found in registry")

        tool_func = self.tool_registry[tool_name]

        # Execute tool function
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(
                input_data, context, **step.config.get("tool_params", {})
            )
        else:
            result = tool_func(
                input_data, context, **step.config.get("tool_params", {})
            )

        context.record_tool_execution(tool_name)
        return result

    async def _execute_condition_step(
        self, step: WorkflowStep, input_data: Any, context: ExecutionContext
    ) -> Any:
        """Execute a conditional step."""
        condition = step.config.get("condition")
        if not condition:
            raise ValueError(f"Condition step {step.id} missing condition")

        # Simple condition evaluation (in practice, you'd use a proper expression evaluator)
        if self._evaluate_condition(condition, input_data, context):
            return step.config.get("true_value", input_data)
        else:
            return step.config.get("false_value", input_data)

    def _prepare_step_input(
        self, step: WorkflowStep, workflow_input: Any, previous_outputs: Dict[str, Any]
    ) -> Any:
        """Prepare input for a step based on its dependencies."""
        if not step.dependencies:
            return workflow_input

        # If step has dependencies, use output from the last dependency
        # In a more sophisticated implementation, you could merge multiple outputs
        last_dep = step.dependencies[-1]
        return previous_outputs.get(last_dep, workflow_input)

    def _evaluate_condition(
        self, condition: str, input_data: Any, context: ExecutionContext
    ) -> bool:
        """Evaluate a simple condition."""
        # This is a simplified condition evaluator
        # In practice, you'd use a proper expression language

        # Support simple conditions like "input.length > 10"
        if "input" in condition:
            try:
                # Replace 'input' with actual input data
                safe_globals = {"input": input_data, "context": context}
                return eval(condition, safe_globals)
            except Exception:
                return False

        return bool(condition)
