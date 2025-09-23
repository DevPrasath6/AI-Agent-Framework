"""
Audit trail functionality for tracking agent execution history.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path


class AuditTrail:
    """
    Audit trail for tracking agent execution events and history.
    """

    def __init__(self, agent_id: str, storage_path: Optional[str] = None):
        """
        Initialize audit trail.

        Args:
            agent_id: ID of the agent being audited
            storage_path: Optional path for storing audit logs
        """
        self.agent_id = agent_id
        self.storage_path = storage_path
        self.logger = logging.getLogger(f"audit.{agent_id}")
        self.events: List[Dict[str, Any]] = []

    async def log_execution_start(
        self, execution_id: str, input_data: Any, context: Dict[str, Any]
    ) -> None:
        """Log the start of an execution."""
        event = {
            "event_type": "execution_start",
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input_data": self._serialize_data(input_data),
            "context": context,
        }
        await self._log_event(event)

    async def log_execution_complete(
        self, execution_id: str, output_data: Any, duration: float
    ) -> None:
        """Log successful completion of an execution."""
        event = {
            "event_type": "execution_complete",
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "output_data": self._serialize_data(output_data),
            "duration": duration,
        }
        await self._log_event(event)

    async def log_execution_error(
        self, execution_id: str, error: str, duration: float
    ) -> None:
        """Log an execution error."""
        event = {
            "event_type": "execution_error",
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "error": error,
            "duration": duration,
        }
        await self._log_event(event)

    async def log_tool_execution(
        self,
        execution_id: str,
        tool_name: str,
        tool_input: Any,
        tool_output: Any,
        duration: float,
    ) -> None:
        """Log tool execution within an agent run."""
        event = {
            "event_type": "tool_execution",
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "tool_name": tool_name,
            "timestamp": datetime.utcnow().isoformat(),
            "tool_input": self._serialize_data(tool_input),
            "tool_output": self._serialize_data(tool_output),
            "duration": duration,
        }
        await self._log_event(event)

    async def log_policy_violation(
        self, execution_id: str, policy_type: str, violation_details: str
    ) -> None:
        """Log a policy violation."""
        event = {
            "event_type": "policy_violation",
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat(),
            "policy_type": policy_type,
            "violation_details": violation_details,
        }
        await self._log_event(event)

    async def _log_event(self, event: Dict[str, Any]) -> None:
        """Log an event to the audit trail."""
        self.events.append(event)
        self.logger.info(f"Audit event: {event['event_type']}", extra=event)

        # Optionally persist to storage
        if self.storage_path:
            await self._persist_event(event)

    async def _persist_event(self, event: Dict[str, Any]) -> None:
        """Persist event to storage."""
        try:
            audit_file = Path(self.storage_path) / f"audit_{self.agent_id}.jsonl"
            audit_file.parent.mkdir(parents=True, exist_ok=True)

            with open(audit_file, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            self.logger.error(f"Failed to persist audit event: {e}")

    def _serialize_data(self, data: Any) -> Any:
        """Serialize data for audit logging."""
        try:
            # Convert to JSON-serializable format
            return json.loads(json.dumps(data, default=str))
        except Exception:
            # If serialization fails, convert to string
            return str(data)

    def get_events(
        self,
        event_type: Optional[str] = None,
        execution_id: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get audit events with optional filtering."""
        events = self.events

        if event_type:
            events = [e for e in events if e.get("event_type") == event_type]

        if execution_id:
            events = [e for e in events if e.get("execution_id") == execution_id]

        if limit:
            events = events[-limit:]

        return events

    def get_execution_summary(self, execution_id: str) -> Dict[str, Any]:
        """Get summary of events for a specific execution."""
        events = self.get_events(execution_id=execution_id)

        if not events:
            return {
                "execution_id": execution_id,
                "events": [],
                "summary": "No events found",
            }

        start_event = next(
            (e for e in events if e["event_type"] == "execution_start"), None
        )
        end_event = next(
            (
                e
                for e in events
                if e["event_type"] in ["execution_complete", "execution_error"]
            ),
            None,
        )
        tool_events = [e for e in events if e["event_type"] == "tool_execution"]

        summary = {
            "execution_id": execution_id,
            "agent_id": self.agent_id,
            "start_time": start_event["timestamp"] if start_event else None,
            "end_time": end_event["timestamp"] if end_event else None,
            "status": end_event["event_type"] if end_event else "running",
            "tool_count": len(tool_events),
            "total_events": len(events),
            "events": events,
        }

        if end_event and "duration" in end_event:
            summary["duration"] = end_event["duration"]

        return summary


# Legacy function for compatibility
def append_audit(run_id: str, event: Any) -> None:
    """Legacy audit function for backward compatibility."""
    logger = logging.getLogger("audit.legacy")
    logger.info(f"Legacy audit - Run ID: {run_id}, Event: {event}")
