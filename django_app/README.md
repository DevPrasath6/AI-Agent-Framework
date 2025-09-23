This README explains how to run the Django control plane for local development.

Prerequisites (local dev)
- Python 3.10+
- (optional) Redis for Celery: `redis-server`
- (optional) Kafka for event transport

Running Django dev server
1. Create virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
```

2. Run migrations and start server:

```powershell
python manage.py migrate
python manage.py runserver
```

Running the Kafka worker (dev)

If you have Kafka running, use the management command to start the consumer that bridges events to the orchestrator:

```powershell
python manage.py run_kafka_worker
```

Running Celery worker (dev)

If you have Redis (or other broker) configured, start a Celery worker:

```powershell
celery -A ai_framework worker --loglevel=info
```

Notes
- The adapters attempt to send events to Kafka if available; otherwise they will call Celery tasks directly or write debug files to `/tmp/`.
- For quick local testing you can create an Agent via the SDK (reference agents are registered on import) and then use the API endpoints to register it into the DB and start runs.

API endpoints
- `GET /api/agents/available/` — list SDK-registered agents
- `POST /api/agents/register_from_sdk/` — create DB agent from SDK-registered name
- `POST /api/agents/{id}/start/` — enqueue agent run
- `GET /api/workflows/{id}/definition/` — get parsed workflow definition (JSON)
- `POST /api/workflows/{id}/start/` — enqueue workflow run
