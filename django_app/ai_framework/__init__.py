try:
	# Import celery app if available; avoid failing import if Celery or local modules
	# cause issues during test discovery or in environments without Celery installed.
	from .celery import app as celery_app  # noqa
except Exception:
	celery_app = None

__all__ = ('celery_app',)
