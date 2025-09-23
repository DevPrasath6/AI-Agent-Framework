"""
Tool base classes and execution framework for agent tools.
"""

import asyncio
import logging
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass

from .execution_context import ExecutionContext


class ToolType(Enum):
    """Types of tools available in the framework."""

    LLM = "llm"
    WEB_SEARCH = "web_search"
    DATA_EXTRACTION = "data_extraction"
    FILE_PROCESSING = "file_processing"
    API_CALL = "api_call"
    DATABASE = "database"
    COMPUTATION = "computation"
    CUSTOM = "custom"


class ToolStatus(Enum):
    """Tool execution status."""

    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class ToolResult:
    """Result of tool execution."""

    tool_name: str
    status: ToolStatus
    output: Any
    error: Optional[str] = None
    duration: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ToolBase(ABC):
    """
    Base class for all tools in the framework.

    Provides standardized interface for tool execution,
    error handling, and result reporting.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        tool_type: ToolType = ToolType.CUSTOM,
        timeout: Optional[int] = None,
        retry_count: int = 0,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize tool.

        Args:
            name: Unique name for the tool
            description: Human-readable description
            tool_type: Type of tool
            timeout: Execution timeout in seconds
            retry_count: Number of retries on failure
            config: Tool-specific configuration
        """
        self.name = name
        self.description = description
        self.tool_type = tool_type
        self.timeout = timeout
        self.retry_count = retry_count
        self.config = config or {}

        self.logger = logging.getLogger(f"tool.{self.name}")
        self.status = ToolStatus.READY
        self.execution_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self.created_at = datetime.utcnow()

    async def execute(
        self, payload: Any, context: Optional[ExecutionContext] = None
    ) -> ToolResult:
        """
        Execute the tool with full lifecycle management.

        Args:
            payload: Input data for the tool
            context: Optional execution context

        Returns:
            Tool execution result
        """
        if context is None:
            context = ExecutionContext()

        execution_id = str(uuid.uuid4())
        start_time = time.time()

        try:
            self.status = ToolStatus.RUNNING
            self.execution_count += 1

            self.logger.info(
                f"Executing tool '{self.name}' with execution ID: {execution_id}"
            )

            # Execute with retries
            result = await self._execute_with_retries(payload, context)

            # Calculate duration
            duration = time.time() - start_time
            self.total_duration += duration

            # Create successful result
            tool_result = ToolResult(
                tool_name=self.name,
                status=ToolStatus.COMPLETED,
                output=result,
                duration=duration,
                metadata={
                    "execution_id": execution_id,
                    "execution_count": self.execution_count,
                    "tool_type": self.tool_type.value,
                },
            )

            self.status = ToolStatus.COMPLETED
            self.logger.info(f"Tool '{self.name}' completed in {duration:.2f}s")

            # Record in context
            context.record_tool_execution(self.name)

            return tool_result

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            self.status = ToolStatus.TIMEOUT
            self.error_count += 1

            error_msg = f"Tool execution timed out after {self.timeout}s"
            self.logger.error(error_msg)

            return ToolResult(
                tool_name=self.name,
                status=ToolStatus.TIMEOUT,
                output=None,
                error=error_msg,
                duration=duration,
                metadata={"execution_id": execution_id},
            )

        except Exception as e:
            duration = time.time() - start_time
            self.status = ToolStatus.FAILED
            self.error_count += 1

            error_msg = str(e)
            self.logger.error(f"Tool execution failed: {error_msg}")

            return ToolResult(
                tool_name=self.name,
                status=ToolStatus.FAILED,
                output=None,
                error=error_msg,
                duration=duration,
                metadata={"execution_id": execution_id},
            )

    async def _execute_with_retries(
        self, payload: Any, context: ExecutionContext
    ) -> Any:
        """Execute tool with retry logic."""
        last_error = None

        for attempt in range(self.retry_count + 1):
            try:
                if self.timeout:
                    # Execute with timeout
                    result = await asyncio.wait_for(
                        self._execute_tool(payload, context), timeout=self.timeout
                    )
                else:
                    # Execute without timeout
                    result = await self._execute_tool(payload, context)

                return result

            except Exception as e:
                last_error = e
                if attempt < self.retry_count:
                    self.logger.warning(
                        f"Tool execution attempt {attempt + 1} failed, retrying: {e}"
                    )
                    await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
                else:
                    self.logger.error(
                        f"Tool execution failed after {self.retry_count + 1} attempts"
                    )

        raise last_error

    @abstractmethod
    async def _execute_tool(self, payload: Any, context: ExecutionContext) -> Any:
        """
        Execute the tool's core logic.

        This method should be implemented by subclasses.
        """
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get tool status and metrics."""
        avg_duration = self.total_duration / max(self.execution_count, 1)
        error_rate = (self.error_count / max(self.execution_count, 1)) * 100

        return {
            "name": self.name,
            "description": self.description,
            "type": self.tool_type.value,
            "status": self.status.value,
            "execution_count": self.execution_count,
            "error_count": self.error_count,
            "error_rate": error_rate,
            "average_duration": avg_duration,
            "total_duration": self.total_duration,
            "created_at": self.created_at.isoformat(),
            "config": self.config,
        }

    def reset_metrics(self) -> None:
        """Reset tool execution metrics."""
        self.execution_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self.status = ToolStatus.READY


class SimpleTool(ToolBase):
    """
    Simple tool implementation that wraps a function.
    """

    def __init__(
        self,
        name: str,
        func: Callable,
        description: str = "",
        tool_type: ToolType = ToolType.CUSTOM,
        **kwargs,
    ):
        """
        Initialize simple tool.

        Args:
            name: Tool name
            func: Function to execute
            description: Tool description
            tool_type: Type of tool
            **kwargs: Additional tool configuration
        """
        super().__init__(name, description, tool_type, **kwargs)
        self.func = func

    async def _execute_tool(self, payload: Any, context: ExecutionContext) -> Any:
        """Execute the wrapped function."""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(payload, context)
        else:
            return self.func(payload, context)


class DataProcessingTool(ToolBase):
    """
    Tool for data processing operations.
    """

    def __init__(
        self,
        name: str,
        processor_func: Callable,
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize data processing tool.

        Args:
            name: Tool name
            processor_func: Data processing function
            input_schema: Expected input schema
            output_schema: Expected output schema
            **kwargs: Additional tool configuration
        """
        super().__init__(name=name, tool_type=ToolType.DATA_EXTRACTION, **kwargs)
        self.processor_func = processor_func
        self.input_schema = input_schema
        self.output_schema = output_schema

    async def _execute_tool(self, payload: Any, context: ExecutionContext) -> Any:
        """Execute data processing."""
        # Validate input if schema provided
        if self.input_schema:
            self._validate_data(payload, self.input_schema, "input")

        # Process data
        if asyncio.iscoroutinefunction(self.processor_func):
            result = await self.processor_func(payload, context)
        else:
            result = self.processor_func(payload, context)

        # Validate output if schema provided
        if self.output_schema:
            self._validate_data(result, self.output_schema, "output")

        return result

    def _validate_data(self, data: Any, schema: Dict[str, Any], data_type: str) -> None:
        """Validate data against schema (simplified validation)."""
        # This is a simplified validation
        # In practice, you'd use a proper schema validation library
        if not isinstance(data, dict):
            return

        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required {data_type} field: {field}")


class ToolRegistry:
    """
    Registry for managing available tools.
    """

    def __init__(self):
        """Initialize tool registry."""
        self.tools: Dict[str, ToolBase] = {}
        self.logger = logging.getLogger("tool_registry")

    def register_tool(self, tool: ToolBase) -> None:
        """Register a tool."""
        if tool.name in self.tools:
            self.logger.warning(f"Overwriting existing tool: {tool.name}")

        self.tools[tool.name] = tool
        self.logger.info(f"Registered tool: {tool.name}")

    def unregister_tool(self, tool_name: str) -> bool:
        """Unregister a tool."""
        if tool_name in self.tools:
            del self.tools[tool_name]
            self.logger.info(f"Unregistered tool: {tool_name}")
            return True
        return False

    def get_tool(self, tool_name: str) -> Optional[ToolBase]:
        """Get a tool by name."""
        return self.tools.get(tool_name)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self.tools.keys())

    def get_tools_by_type(self, tool_type: ToolType) -> List[ToolBase]:
        """Get all tools of a specific type."""
        return [tool for tool in self.tools.values() if tool.tool_type == tool_type]

    def get_tool_summary(self) -> Dict[str, Any]:
        """Get summary of all registered tools."""
        tools_by_type = {}
        for tool in self.tools.values():
            tool_type = tool.tool_type.value
            if tool_type not in tools_by_type:
                tools_by_type[tool_type] = []
            tools_by_type[tool_type].append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "status": tool.status.value,
                    "execution_count": tool.execution_count,
                }
            )

        return {
            "total_tools": len(self.tools),
            "tools_by_type": tools_by_type,
            "tool_names": list(self.tools.keys()),
        }

    async def execute_tool(
        self, tool_name: str, payload: Any, context: Optional[ExecutionContext] = None
    ) -> ToolResult:
        """Execute a tool by name."""
        tool = self.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool '{tool_name}' not found in registry")

        return await tool.execute(payload, context)


# Global tool registry instance
default_tool_registry = ToolRegistry()


# Legacy compatibility function
def execute_tool(payload: Any, ctx: Optional[ExecutionContext] = None) -> Any:
    """Legacy tool execution function for backward compatibility."""
    logger = logging.getLogger("tool.legacy")
    logger.info(f"Legacy tool execution - Payload: {payload}")
    return payload  # Just return the payload for compatibility
