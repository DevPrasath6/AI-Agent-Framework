# Frontend Disconnected

This frontend has been **disconnected** from the AI Agent Framework to keep the framework focused on core backend functionality.

## Status: 🔌 DISCONNECTED

The frontend is fully functional but not integrated with the main framework. You can use this React frontend for other projects or reconnect it if needed.

## To Reconnect (Optional):

1. **Enable CORS in Django settings:**
   ```python
   # In django_app/ai_framework/settings.py
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://127.0.0.1:3000",
   ]
   CORS_ALLOW_CREDENTIALS = True
   ```

2. **Configure API URL:**
   ```bash
   # In frontend/.env
   REACT_APP_API_URL=http://localhost:8000/api
   ```

3. **Start both services:**
   ```bash
   # Terminal 1: Start Django backend
   python django_app/manage.py runserver
   
   # Terminal 2: Start React frontend
   cd frontend && npm start
   ```

## Framework Architecture (Backend Only):

```
REST API → Django → Orchestrator → Agents → Memory/State
    ↓
  Kafka → Workers → Tools → Guardrails
```

The framework operates entirely through REST APIs and doesn't require a frontend for core functionality.

## Frontend Features (Available for Other Projects):

- ✅ Modern React 18 with hooks
- ✅ Tailwind CSS styling
- ✅ Chart.js for data visualization
- ✅ Framer Motion animations
- ✅ Agent management interface
- ✅ Workflow visualization
- ✅ Real-time monitoring dashboard
- ✅ Responsive design

Feel free to reuse this frontend for any project that needs a modern React admin interface!