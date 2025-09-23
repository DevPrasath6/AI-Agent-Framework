"""
SDK agent registry for demos and examples.
"""
from typing import Any, Dict

_AGENTS: Dict[str, Any] = {}


def register_agent(defn: Any) -> None:
	"""Register an agent definition or instance.

	If `defn` has a `name` attribute it will be used as the key; when a
	dict with an `id` is provided the `id` is used.
	"""
	name = getattr(defn, "name", None) or (defn.get("id") if isinstance(defn, dict) else None)
	if not name:
		raise ValueError("Agent must have a name or id")
	_AGENTS[name] = defn


def get_agent(name: str) -> Any:
	return _AGENTS.get(name)


def list_agents() -> list:
	return list(_AGENTS.keys())
