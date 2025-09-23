"""Top-level ai_framework package shim.

This package delegates to the real Django project package located at
`django_app/ai_framework`. We modify `__path__` so submodule imports like
`ai_framework.test_settings` resolve to files under `django_app/ai_framework`.

When the target package isn't available (e.g. partial workspace), this shim
keeps imports from failing at import-time.
"""

import os
import sys
import importlib
import types

# Try to locate the django_app/ai_framework directory and insert it into
# this package __path__ so normal submodule imports work.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
django_pkg_path = os.path.join(ROOT, "django_app", "ai_framework")
if os.path.isdir(django_pkg_path):
    # Prepend so it takes precedence over this package's directory
    __path__.insert(0, django_pkg_path)
    try:
        # Import a few top-level attributes if available to preserve behavior
        pkg = importlib.import_module("django_app.ai_framework")
        this = sys.modules.setdefault(__name__, types.ModuleType(__name__))
        for k, v in pkg.__dict__.items():
            if k.startswith("__"):
                continue
            setattr(this, k, v)
    except Exception:
        # best-effort; continue with path mapping even if attribute copy fails
        pass
else:
    # fallback minimal package
    __all__ = []
