import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_framework.settings')

app = Celery('ai_framework')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Use a placeholder broker for tests (Django TestCase calls tasks directly)
app.conf.task_always_eager = True


# Discover task modules from installed apps
app.autodiscover_tasks()
