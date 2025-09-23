def create_celery_app(name="ai_agent_framework"):
    # Import Celery lazily to avoid import-time dependency on Celery during
    # Django test discovery or when the package is not available.
    try:
        from celery import Celery
    except Exception:
        Celery = None
    # Avoid importing django.conf.settings at module import time because that
    # triggers Django setup (and fails if DJANGO_SETTINGS_MODULE isn't set
    # during test collection). Prefer environment variables or defaults.
    import os

    broker = os.environ.get("CELERY_BROKER_URL", None)
    backend = os.environ.get("CELERY_RESULT_BACKEND", None)
    if broker is None or backend is None:
        # Only try to read Django settings if a settings module is configured
        if os.environ.get("DJANGO_SETTINGS_MODULE"):
            try:
                from django.conf import settings

                if broker is None:
                    broker = getattr(settings, "CELERY_BROKER_URL", None)
                if backend is None:
                    backend = getattr(settings, "CELERY_RESULT_BACKEND", None)
            except Exception:
                # Fall through to defaults
                pass

    if not broker:
        broker = "redis://localhost:6379/0"
    if not backend:
        backend = broker
    if Celery is None:
        # Return a minimal dummy object with expected attributes for tests that
        # simply import this module but don't actually create tasks.
        class _DummyApp:
            def __init__(self):
                self.conf = {}

            def conf_update(self, *args, **kwargs):
                self.conf.update(*args, **kwargs)

        return _DummyApp()

    app = Celery(name, broker=broker, backend=backend)
    # Minimal config: allow tasks to be discovered in this package
    app.conf.update(
        {
            "task_serializer": "json",
            "accept_content": ["json"],
            "result_serializer": "json",
        }
    )
    return app


# Instantiate default app lazily
# Instantiate default app lazily (call create_celery_app() at import time is okay
# now because we avoid touching django.conf.settings unless DJANGO_SETTINGS_MODULE
# is explicitly set).
celery_app = create_celery_app()
