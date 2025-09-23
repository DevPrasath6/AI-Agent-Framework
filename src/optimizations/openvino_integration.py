"""OpenVINO integration placeholder.

This does not load real OpenVINO models; it provides a stub interface
so calling code can be exercised during development.
"""
from pathlib import Path


def load_openvino_model(path: str) -> dict:
	p = Path(path)
	if not p.exists():
		raise FileNotFoundError(path)
	# Return a small descriptor instead of a real model object
	return {"model_path": str(p), "loaded": True, "framework": "openvino"}
