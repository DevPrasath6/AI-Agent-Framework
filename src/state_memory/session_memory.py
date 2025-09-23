"""
Session memory management for agent state and conversation history.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict, deque


class SessionMemory:
    """
    Session memory for storing agent state and interaction history.

    Supports both in-memory and Redis-backed storage for agent sessions.
    """

    def __init__(
        self,
        agent_id: str,
        max_history_size: int = 100,
        session_timeout: int = 3600,  # 1 hour in seconds
        redis_client=None,
    ):
        """
        Initialize session memory.

        Args:
            agent_id: ID of the agent this memory belongs to
            max_history_size: Maximum number of interactions to store
            session_timeout: Session timeout in seconds
            redis_client: Optional Redis client for persistent storage
        """
        self.agent_id = agent_id
        self.max_history_size = max_history_size
        self.session_timeout = session_timeout
        self.redis_client = redis_client
        self.logger = logging.getLogger(f"memory.{agent_id}")

        # In-memory storage (used when Redis is not available)
        self._store: Dict[str, Any] = {}
        self._interaction_history: deque = deque(maxlen=max_history_size)
        self._session_data: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._last_access: Dict[str, datetime] = {}

        # Memory statistics
        self.total_interactions = 0
        self.created_at = datetime.utcnow()

    async def store_interaction(
        self,
        input_data: Any,
        output_data: Any,
        context: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> None:
        """Store an interaction in memory."""
        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": self._serialize_data(input_data),
            "output": self._serialize_data(output_data),
            "context": context,
            "session_id": session_id or "default",
            "interaction_id": f"{self.agent_id}_{self.total_interactions}",
        }

        # Store in history
        self._interaction_history.append(interaction)
        self.total_interactions += 1

        # Update session data
        if session_id:
            self._session_data[session_id]["last_interaction"] = interaction
            self._last_access[session_id] = datetime.utcnow()

        # Optionally store in Redis
        if self.redis_client:
            await self._store_interaction_redis(interaction)

        self.logger.debug(f"Stored interaction {interaction['interaction_id']}")

    def get(self, key: str, session_id: Optional[str] = None) -> Any:
        """Get a value from memory."""
        if session_id:
            return self._session_data.get(session_id, {}).get(key)
        return self._store.get(key)

    def set(self, key: str, value: Any, session_id: Optional[str] = None) -> None:
        """Set a value in memory."""
        if session_id:
            self._session_data[session_id][key] = value
            self._last_access[session_id] = datetime.utcnow()
        else:
            self._store[key] = value

    def get_interaction_history(
        self, session_id: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get interaction history."""
        history = list(self._interaction_history)

        # Filter by session if specified
        if session_id:
            history = [h for h in history if h.get("session_id") == session_id]

        # Apply limit
        if limit:
            history = history[-limit:]

        return history

    def get_recent_context(
        self, session_id: Optional[str] = None, lookback_count: int = 5
    ) -> Dict[str, Any]:
        """Get recent context for continuing conversations."""
        recent_interactions = self.get_interaction_history(session_id, lookback_count)

        if not recent_interactions:
            return {}

        # Build context from recent interactions
        context = {
            "recent_inputs": [i["input"] for i in recent_interactions[-3:]],
            "recent_outputs": [i["output"] for i in recent_interactions[-3:]],
            "last_interaction": recent_interactions[-1]
            if recent_interactions
            else None,
            "conversation_length": len(recent_interactions),
            "session_id": session_id,
        }

        return context

    async def get_summary(self) -> Dict[str, Any]:
        """Get memory summary and statistics."""
        active_sessions = self._count_active_sessions()

        return {
            "agent_id": self.agent_id,
            "total_interactions": self.total_interactions,
            "history_size": len(self._interaction_history),
            "active_sessions": active_sessions,
            "total_sessions": len(self._session_data),
            "memory_size_kb": self._estimate_memory_size(),
            "created_at": self.created_at.isoformat(),
            "using_redis": self.redis_client is not None,
        }

    def clear_session(self, session_id: str) -> bool:
        """Clear all data for a specific session."""
        if session_id in self._session_data:
            del self._session_data[session_id]

        if session_id in self._last_access:
            del self._last_access[session_id]

        # Remove from interaction history
        self._interaction_history = deque(
            [h for h in self._interaction_history if h.get("session_id") != session_id],
            maxlen=self.max_history_size,
        )

        self.logger.info(f"Cleared session {session_id}")
        return True

    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions based on timeout."""
        now = datetime.utcnow()
        expired_sessions = []

        for session_id, last_access in self._last_access.items():
            if (now - last_access).total_seconds() > self.session_timeout:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            self.clear_session(session_id)

        if expired_sessions:
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

        return len(expired_sessions)

    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific session."""
        if session_id not in self._session_data:
            return None

        session_interactions = [
            h for h in self._interaction_history if h.get("session_id") == session_id
        ]

        return {
            "session_id": session_id,
            "data_keys": list(self._session_data[session_id].keys()),
            "interaction_count": len(session_interactions),
            "last_access": self._last_access.get(session_id),
            "first_interaction": session_interactions[0]
            if session_interactions
            else None,
            "last_interaction": session_interactions[-1]
            if session_interactions
            else None,
        }

    def _count_active_sessions(self) -> int:
        """Count sessions that have been accessed recently."""
        now = datetime.utcnow()
        active_count = 0

        for last_access in self._last_access.values():
            if (now - last_access).total_seconds() <= self.session_timeout:
                active_count += 1

        return active_count

    def _estimate_memory_size(self) -> float:
        """Estimate memory usage in KB."""
        try:
            # Rough estimate based on string representation
            data_str = json.dumps(
                {
                    "store": self._store,
                    "history": list(self._interaction_history),
                    "sessions": dict(self._session_data),
                },
                default=str,
            )
            return len(data_str.encode("utf-8")) / 1024
        except Exception:
            return 0.0

    def _serialize_data(self, data: Any) -> Any:
        """Serialize data for storage."""
        try:
            return json.loads(json.dumps(data, default=str))
        except Exception:
            return str(data)

    async def _store_interaction_redis(self, interaction: Dict[str, Any]) -> None:
        """Store interaction in Redis if available."""
        if not self.redis_client:
            return

        try:
            key = f"agent:{self.agent_id}:interaction:{interaction['interaction_id']}"
            await self.redis_client.setex(
                key, self.session_timeout, json.dumps(interaction, default=str)
            )
        except Exception as e:
            self.logger.error(f"Failed to store interaction in Redis: {e}")


class SharedMemory:
    """
    Shared memory for cross-agent communication and data sharing.
    """

    def __init__(self, redis_client=None):
        """Initialize shared memory."""
        self.redis_client = redis_client
        self._shared_store: Dict[str, Any] = {}
        self.logger = logging.getLogger("shared_memory")

    async def set_shared(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a shared value accessible by all agents."""
        self._shared_store[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "ttl": ttl,
        }

        if self.redis_client and ttl:
            try:
                await self.redis_client.setex(
                    f"shared:{key}", ttl, json.dumps(value, default=str)
                )
            except Exception as e:
                self.logger.error(f"Failed to set shared value in Redis: {e}")

    async def get_shared(self, key: str) -> Any:
        """Get a shared value."""
        stored_data = self._shared_store.get(key)
        if stored_data:
            return stored_data["value"]

        # Try Redis fallback
        if self.redis_client:
            try:
                value = await self.redis_client.get(f"shared:{key}")
                if value:
                    return json.loads(value)
            except Exception as e:
                self.logger.error(f"Failed to get shared value from Redis: {e}")

        return None

    def list_shared_keys(self) -> List[str]:
        """List all shared keys."""
        return list(self._shared_store.keys())
