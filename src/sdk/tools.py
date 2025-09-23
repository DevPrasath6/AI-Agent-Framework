"""
SDK helper for registering tools in an in-memory registry for demos/tests.
"""

from typing import Any, Dict

_TOOLS: Dict[str, Any] = {}


def register_tool(tool: Any) -> None:
    """Register a tool in the SDK registry.

    Tool must have a `name` attribute.
    """
    name = getattr(tool, "name", None)
    if not name:
        raise ValueError("Tool must have a 'name' attribute")
    _TOOLS[name] = tool


def get_tool(name: str) -> Any:
    return _TOOLS.get(name)


def list_tools() -> list:
    return list(_TOOLS.keys())
