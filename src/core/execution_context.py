"""
Execution context management for agent workflows.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from enum import Enum


class ExecutionPhase(Enum):
    """Execution phases for tracking workflow progress."""
    INITIALIZATION = "initialization"
    INPUT_PROCESSING = "input_processing"
    TOOL_EXECUTION = "tool_execution"
    AGENT_EXECUTION = "agent_execution"
    OUTPUT_PROCESSING = "output_processing"
    COMPLETION = "completion"
    ERROR_HANDLING = "error_handling"


class ExecutionContext:
    """
    Context object that tracks execution state across workflow steps.

    Provides shared state, metadata, and coordination mechanisms
    for agents and tools within a workflow execution.
    """

    def __init__(
        self,
        workflow_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        # Legacy compatibility
        run_id: Optional[str] = None,
        memory: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize execution context.

        Args:
            workflow_id: ID of the executing workflow
            agent_id: ID of the primary agent
            user_id: ID of the user initiating execution
            session_id: Session identifier for grouping executions
            metadata: Additional metadata
            run_id: Legacy run ID (for compatibility)
            memory: Legacy memory dict (for compatibility)
        """
        self.execution_id = str(uuid.uuid4())
        self.workflow_id = workflow_id
        self.agent_id = agent_id
        self.user_id = user_id
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

        # Legacy compatibility
        self.run_id = run_id or self.execution_id

        # Execution state
        self.phase = ExecutionPhase.INITIALIZATION
        self.step_count = 0
        self.is_cancelled = False

        # Shared data between workflow steps
        self.shared_data: Dict[str, Any] = {}
        self.intermediate_results: List[Dict[str, Any]] = []

        # Legacy memory support
        self.memory = memory or {}

        # Tool and agent tracking
        self.executed_tools: List[str] = []
        self.executed_agents: List[str] = []
        self.agent_outputs: Dict[str, Any] = {}

        # Error tracking
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[str] = []

        # Metadata and configuration
        self.metadata = metadata or {}
        self.config: Dict[str, Any] = {}

        # Performance tracking
        self.start_time = None
        self.end_time = None
        self.step_timings: Dict[str, float] = {}

        # Resource usage tracking
        self.memory_usage: List[int] = []
        self.cpu_usage: List[float] = []

    def start_execution(self) -> None:
        """Mark the start of execution."""
        self.start_time = datetime.utcnow()
        self.phase = ExecutionPhase.INPUT_PROCESSING
        self._update_timestamp()

    def end_execution(self) -> None:
        """Mark the end of execution."""
        self.end_time = datetime.utcnow()
        self.phase = ExecutionPhase.COMPLETION
        self._update_timestamp()

    def advance_phase(self, phase: ExecutionPhase) -> None:
        """Advance to the next execution phase."""
        self.phase = phase
        self.step_count += 1
        self._update_timestamp()

    def cancel_execution(self, reason: str = "") -> None:
        """Cancel the current execution."""
        self.is_cancelled = True
        self.add_error("execution_cancelled", reason or "Execution cancelled by user")
        self.phase = ExecutionPhase.ERROR_HANDLING
        self._update_timestamp()

    def set_shared_data(self, key: str, value: Any) -> None:
        """Set shared data accessible across workflow steps."""
        self.shared_data[key] = value
        self._update_timestamp()

    def get_shared_data(self, key: str, default: Any = None) -> Any:
        """Get shared data by key."""
        return self.shared_data.get(key, default)

    def add_intermediate_result(
        self,
        step_name: str,
        result: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an intermediate result from a workflow step."""
        result_entry = {
            "step_name": step_name,
            "result": result,
            "timestamp": datetime.utcnow().isoformat(),
            "step_number": len(self.intermediate_results) + 1,
            "metadata": metadata or {}
        }
        self.intermediate_results.append(result_entry)
        self._update_timestamp()

    def record_tool_execution(self, tool_name: str) -> None:
        """Record that a tool was executed."""
        self.executed_tools.append(tool_name)
        self._update_timestamp()

    def record_agent_execution(self, agent_id: str, output: Any = None) -> None:
        """Record that an agent was executed."""
        self.executed_agents.append(agent_id)
        if output is not None:
            self.agent_outputs[agent_id] = output
        self._update_timestamp()

    def add_error(
        self,
        error_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add an error to the execution context."""
        error_entry = {
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "phase": self.phase.value,
            "step_count": self.step_count,
            "details": details or {}
        }
        self.errors.append(error_entry)
        self._update_timestamp()

    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        warning_entry = f"[{datetime.utcnow().isoformat()}] {message}"
        self.warnings.append(warning_entry)
        self._update_timestamp()

    def record_step_timing(self, step_name: str, duration: float) -> None:
        """Record timing for a workflow step."""
        self.step_timings[step_name] = duration
        self._update_timestamp()

    def get_execution_duration(self) -> Optional[float]:
        """Get total execution duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.utcnow() - self.start_time).total_seconds()
        return None

    def has_errors(self) -> bool:
        """Check if execution has any errors."""
        return len(self.errors) > 0

    def get_last_error(self) -> Optional[Dict[str, Any]]:
        """Get the most recent error."""
        return self.errors[-1] if self.errors else None

    def get_summary(self) -> Dict[str, Any]:
        """Get execution context summary."""
        duration = self.get_execution_duration()

        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "phase": self.phase.value,
            "step_count": self.step_count,
            "duration": duration,
            "is_cancelled": self.is_cancelled,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "tools_executed": len(self.executed_tools),
            "agents_executed": len(self.executed_agents),
            "has_intermediate_results": len(self.intermediate_results) > 0,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert execution context to dictionary."""
        return {
            "execution_id": self.execution_id,
            "workflow_id": self.workflow_id,
            "agent_id": self.agent_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "phase": self.phase.value,
            "step_count": self.step_count,
            "is_cancelled": self.is_cancelled,
            "shared_data": self.shared_data,
            "intermediate_results": self.intermediate_results,
            "executed_tools": self.executed_tools,
            "executed_agents": self.executed_agents,
            "agent_outputs": self.agent_outputs,
            "errors": self.errors,
            "warnings": self.warnings,
            "metadata": self.metadata,
            "config": self.config,
            "step_timings": self.step_timings,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            # Legacy compatibility
            "run_id": self.run_id,
            "memory": self.memory
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionContext":
        """Create execution context from dictionary."""
        context = cls(
            workflow_id=data.get("workflow_id"),
            agent_id=data.get("agent_id"),
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            metadata=data.get("metadata", {}),
            run_id=data.get("run_id"),
            memory=data.get("memory", {})
        )

        # Restore state
        context.execution_id = data.get("execution_id", context.execution_id)
        context.phase = ExecutionPhase(data.get("phase", ExecutionPhase.INITIALIZATION.value))
        context.step_count = data.get("step_count", 0)
        context.is_cancelled = data.get("is_cancelled", False)
        context.shared_data = data.get("shared_data", {})
        context.intermediate_results = data.get("intermediate_results", [])
        context.executed_tools = data.get("executed_tools", [])
        context.executed_agents = data.get("executed_agents", [])
        context.agent_outputs = data.get("agent_outputs", {})
        context.errors = data.get("errors", [])
        context.warnings = data.get("warnings", [])
        context.config = data.get("config", {})
        context.step_timings = data.get("step_timings", {})

        # Parse timestamps
        if data.get("created_at"):
            context.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("updated_at"):
            context.updated_at = datetime.fromisoformat(data["updated_at"])
        if data.get("start_time"):
            context.start_time = datetime.fromisoformat(data["start_time"])
        if data.get("end_time"):
            context.end_time = datetime.fromisoformat(data["end_time"])

        return context

    def _update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self.updated_at = datetime.utcnow()
