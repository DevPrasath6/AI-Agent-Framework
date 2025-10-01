"""
Professional Agent ID Generator

This module provides a professional agent ID generation system with:
- Unique and ordered agent IDs
- Readable format with timestamp and sequence
- Thread-safe generation
- Customizable prefixes and formats
"""

import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib


class AgentIDGenerator:
    """
    Professional agent ID generator that creates unique, ordered, and readable agent IDs.

    Format: AGENT-YYYYMMDD-HHMMSS-NNNN-XXXX
    Where:
    - AGENT: Fixed prefix for agent identification
    - YYYYMMDD: Date of creation (20251001)
    - HHMMSS: Time of creation (143052)
    - NNNN: Sequential counter (0001, 0002, etc.)
    - XXXX: Short hash for uniqueness guarantee

    Example: AGENT-20251001-143052-0001-A7B3
    """

    _instance = None
    _lock = threading.Lock()
    _counter = 0
    _last_timestamp = ""

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.prefix = "AGENT"
            self.counter_width = 4
            self.hash_width = 4
            self._initialized = True

    def generate_id(self, agent_name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a professional, unique, and ordered agent ID.

        Args:
            agent_name: Optional agent name to include in hash calculation
            metadata: Optional metadata for additional uniqueness

        Returns:
            Professional agent ID string
        """
        with self._lock:
            # Get current timestamp
            now = datetime.utcnow()
            timestamp_str = now.strftime("%Y%m%d-%H%M%S")

            # Reset counter if timestamp changed (new second)
            if timestamp_str != self._last_timestamp:
                self._counter = 0
                self._last_timestamp = timestamp_str

            # Increment counter
            self._counter += 1
            counter_str = str(self._counter).zfill(self.counter_width)

            # Generate unique hash component
            hash_input = f"{timestamp_str}-{counter_str}-{agent_name or ''}-{str(metadata or '')}"
            hash_obj = hashlib.md5(hash_input.encode())
            hash_str = hash_obj.hexdigest()[:self.hash_width].upper()

            # Construct professional ID
            agent_id = f"{self.prefix}-{timestamp_str}-{counter_str}-{hash_str}"

            return agent_id

    def parse_id(self, agent_id: str) -> Dict[str, Any]:
        """
        Parse a professional agent ID to extract components.

        Args:
            agent_id: Agent ID to parse

        Returns:
            Dictionary with parsed components
        """
        try:
            parts = agent_id.split('-')
            if len(parts) >= 5 and parts[0] == self.prefix:
                return {
                    "prefix": parts[0],
                    "date": parts[1],
                    "time": parts[2],
                    "sequence": int(parts[3]),
                    "hash": parts[4],
                    "created_at": datetime.strptime(f"{parts[1]}-{parts[2]}", "%Y%m%d-%H%M%S"),
                    "is_valid": True
                }
        except Exception:
            pass

        return {"is_valid": False, "original": agent_id}

    def is_valid_id(self, agent_id: str) -> bool:
        """Check if an agent ID is valid and properly formatted."""
        return self.parse_id(agent_id)["is_valid"]

    def get_creation_time(self, agent_id: str) -> Optional[datetime]:
        """Extract creation timestamp from agent ID."""
        parsed = self.parse_id(agent_id)
        return parsed.get("created_at") if parsed["is_valid"] else None


class SequentialAgentIDGenerator:
    """
    Sequential agent ID generator for simpler use cases.

    Format: AGT_YYYYMMDD_NNNNNN
    Where:
    - AGT: Agent prefix
    - YYYYMMDD: Date of creation
    - NNNNNN: Global sequential number

    Example: AGT_20251001_000042
    """

    _instance = None
    _lock = threading.Lock()
    _global_counter = 0

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.prefix = "AGT"
            self.counter_width = 6
            self._initialized = True

    def generate_id(self) -> str:
        """Generate a sequential agent ID."""
        with self._lock:
            self._global_counter += 1
            date_str = datetime.utcnow().strftime("%Y%m%d")
            counter_str = str(self._global_counter).zfill(self.counter_width)
            return f"{self.prefix}_{date_str}_{counter_str}"

    def get_counter(self) -> int:
        """Get current global counter value."""
        return self._global_counter


class HierarchicalAgentIDGenerator:
    """
    Hierarchical agent ID generator for complex systems.

    Format: ORG-DEPT-TEAM-AGENT-NNNN
    Where each level can be customized.

    Example: PROD-AI-WORKFLOW-PROCESSOR-0001
    """

    def __init__(self, org: str = "SYS", dept: str = "AI", team: str = "CORE"):
        self.org = org.upper()
        self.dept = dept.upper()
        self.team = team.upper()
        self.counters = {}
        self.lock = threading.Lock()

    def generate_id(self, agent_type: str = "AGENT") -> str:
        """Generate hierarchical agent ID."""
        agent_type = agent_type.upper()

        with self.lock:
            if agent_type not in self.counters:
                self.counters[agent_type] = 0

            self.counters[agent_type] += 1
            counter_str = str(self.counters[agent_type]).zfill(4)

            return f"{self.org}-{self.dept}-{self.team}-{agent_type}-{counter_str}"


# Global instances
_default_generator = AgentIDGenerator()
_sequential_generator = SequentialAgentIDGenerator()


def generate_professional_agent_id(agent_name: Optional[str] = None,
                                 metadata: Optional[Dict[str, Any]] = None,
                                 generator_type: str = "professional") -> str:
    """
    Generate a professional agent ID using the specified generator.

    Args:
        agent_name: Optional agent name for uniqueness
        metadata: Optional metadata for additional context
        generator_type: Type of generator ("professional", "sequential", "hierarchical")

    Returns:
        Professional agent ID string
    """
    if generator_type == "sequential":
        return _sequential_generator.generate_id()
    elif generator_type == "hierarchical":
        # Use default hierarchical generator
        hier_gen = HierarchicalAgentIDGenerator()
        return hier_gen.generate_id()
    else:
        # Default to professional generator
        return _default_generator.generate_id(agent_name, metadata)


def parse_agent_id(agent_id: str) -> Dict[str, Any]:
    """Parse an agent ID to extract information."""
    return _default_generator.parse_id(agent_id)


def is_valid_agent_id(agent_id: str) -> bool:
    """Validate an agent ID format."""
    return _default_generator.is_valid_id(agent_id)
