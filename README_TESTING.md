Running Django tests locally

This project includes a lightweight test settings file so you can run the Django
control-plane tests locally without needing an external Postgres service.

Quick steps (PowerShell):

1. From the repository root, run the specific test file:

```powershell
python django_app/manage.py test tests.test_persistence_tasks -v 2
python django_app/manage.py test tests.test_workflow_persistence -v 2
```

2. To run all tests:

```powershell
python django_app/manage.py test
```

Notes:
- When `manage.py` detects `test` in argv it uses `ai_framework.test_settings` (sqlite)
  so tests run without Postgres.
- If you add new Django tests, they should import models using the app label
  (e.g., `from agents.models import Agent`) or use `django.apps.apps.get_model()`.
- The orchestrator task modules include safe fallbacks for Celery to allow tests
  to import without needing a running Celery worker.
