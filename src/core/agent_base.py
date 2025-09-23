"""
Core agent base classes for the AI Agent Framework.
"""

import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum

from .execution_context import ExecutionContext
from ..observability.audit_trail import AuditTrail
from ..guardrails.policy_checker import PolicyChecker
from ..state_memory.session_memory import SessionMemory


class AgentStatus(Enum):
    """Agent execution status."""

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class AgentCapability(Enum):
    """Agent capabilities."""

    TEXT_PROCESSING = "text_processing"
    DOCUMENT_ANALYSIS = "document_analysis"
    DATA_EXTRACTION = "data_extraction"
    CONVERSATION = "conversation"
    WORKFLOW_ORCHESTRATION = "workflow_orchestration"
    MULTI_MODAL = "multi_modal"


class AgentBase(ABC):
    """
    Base class for all agents in the framework.

    Provides core functionality for agent lifecycle management,
    execution context, memory, and observability.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        capabilities: List[AgentCapability] = None,
        config: Dict[str, Any] = None,
        memory_enabled: bool = True,
        guardrails_enabled: bool = True,
    ):
        """
        Initialize the agent.

        Args:
            name: Unique name for the agent
            description: Human-readable description
            capabilities: List of agent capabilities
            config: Agent-specific configuration
            memory_enabled: Whether to enable session memory
            guardrails_enabled: Whether to enable policy checking
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.created_at = datetime.utcnow()
        self.last_executed = None

        # Core components
        self.logger = logging.getLogger(f"agent.{self.name}")
        self.audit_trail = AuditTrail(agent_id=self.id)

        # Optional components
        self.memory = SessionMemory(agent_id=self.id) if memory_enabled else None
        self.policy_checker = PolicyChecker() if guardrails_enabled else None

        # Execution tracking
        self.execution_count = 0
        self.error_count = 0

        self.logger.info(f"Agent '{self.name}' initialized with ID: {self.id}")

    @abstractmethod
    async def execute(self, input_data: Any, context: ExecutionContext) -> Any:
        """
        Execute the agent's main logic.

        Args:
            input_data: Input data to process
            context: Execution context with workflow state

        Returns:
            Processed output data
        """
        pass

    async def run(
        self, input_data: Any, context: Optional[ExecutionContext] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with full lifecycle management.

        Args:
            input_data: Input data to process
            context: Optional execution context

        Returns:
            Execution result with metadata
        """
        if context is None:
            context = ExecutionContext(agent_id=self.id)

        execution_id = str(uuid.uuid4())
        start_time = datetime.utcnow()

        try:
            self.status = AgentStatus.RUNNING
            self.last_executed = start_time
            self.execution_count += 1

            # Log execution start
            self.logger.info(f"Starting execution {execution_id}")
            await self.audit_trail.log_execution_start(
                execution_id=execution_id,
                input_data=input_data,
                context=context.to_dict(),
            )

            # Check guardrails if enabled
            if self.policy_checker:
                policy_result = await self.policy_checker.check_input(input_data)
                if not policy_result.allowed:
                    raise PolicyViolationError(policy_result.reason)

            # Execute main logic
            output = await self.execute(input_data, context)

            # Check output guardrails
            if self.policy_checker:
                policy_result = await self.policy_checker.check_output(output)
                if not policy_result.allowed:
                    raise PolicyViolationError(policy_result.reason)

            # Update memory if enabled
            if self.memory:
                await self.memory.store_interaction(
                    input_data=input_data, output_data=output, context=context.to_dict()
                )

            self.status = AgentStatus.COMPLETED
            end_time = datetime.utcnow()
            execution_duration = (end_time - start_time).total_seconds()

            # Log successful execution
            await self.audit_trail.log_execution_complete(
                execution_id=execution_id,
                output_data=output,
                duration=execution_duration,
            )

            self.logger.info(
                f"Execution {execution_id} completed in {execution_duration:.2f}s"
            )

            return {
                "execution_id": execution_id,
                "status": self.status.value,
                "output": output,
                "duration": execution_duration,
                "agent_id": self.id,
                "agent_name": self.name,
            }

        except Exception as e:
            self.status = AgentStatus.FAILED
            self.error_count += 1
            end_time = datetime.utcnow()
            execution_duration = (end_time - start_time).total_seconds()

            # Log error
            self.logger.error(f"Execution {execution_id} failed: {str(e)}")
            await self.audit_trail.log_execution_error(
                execution_id=execution_id, error=str(e), duration=execution_duration
            )

            return {
                "execution_id": execution_id,
                "status": self.status.value,
                "error": str(e),
                "duration": execution_duration,
                "agent_id": self.id,
                "agent_name": self.name,
            }

    async def stop(self) -> None:
        """Stop the agent execution."""
        self.status = AgentStatus.STOPPED
        self.logger.info(f"Agent '{self.name}' stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and metrics."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "capabilities": [cap.value for cap in self.capabilities],
            "created_at": self.created_at.isoformat(),
            "last_executed": self.last_executed.isoformat()
            if self.last_executed
            else None,
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.execution_count, 1) * 100,
        }

    async def get_memory_summary(self) -> Optional[Dict[str, Any]]:
        """Get agent memory summary if memory is enabled."""
        if self.memory:
            return await self.memory.get_summary()
        return None


class PolicyViolationError(Exception):
    """Raised when agent input/output violates policies."""

    pass


class SimpleAgent(AgentBase):
    """
    A simple agent implementation for basic text processing tasks.
    """

    def __init__(self, name: str, processor_func=None, **kwargs):
        """
        Initialize simple agent.

        Args:
            name: Agent name
            processor_func: Function to process input data
            **kwargs: Additional agent configuration
        """
        super().__init__(
            name=name, capabilities=[AgentCapability.TEXT_PROCESSING], **kwargs
        )
        self.processor_func = processor_func or self._default_processor

    async def execute(self, input_data: Any, context: ExecutionContext) -> Any:
        """Execute the processor function."""
        return await self._run_processor(input_data, context)

    async def _run_processor(self, input_data: Any, context: ExecutionContext) -> Any:
        """Run the processor function with error handling."""
        if asyncio.iscoroutinefunction(self.processor_func):
            return await self.processor_func(input_data, context)
        else:
            return self.processor_func(input_data, context)

    def _default_processor(self, input_data: Any, context: ExecutionContext) -> Any:
        """Default processor that returns input unchanged."""
        return input_data
