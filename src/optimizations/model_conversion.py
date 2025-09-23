"""Model conversion helpers (placeholder).

These functions are lightweight placeholders. Real conversions require
tooling like ONNX, OpenVINO Model Optimizer, TensorRT, etc.
"""

from pathlib import Path


def convert_model(src: str, dst: str) -> bool:
    """Pretend to convert a model by copying the file path.

    Returns True on "success".
    """
    src_path = Path(src)
    dst_path = Path(dst)
    try:
        if not src_path.exists():
            raise FileNotFoundError(src)
        # For demo purposes, just create a small marker file
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(f"Converted from {src_path}\n")
        return True
    except Exception:
        return False
