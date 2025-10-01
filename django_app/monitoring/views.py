
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from agents.models import Agent
from workflows.models import Workflow

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})

@api_view(["GET"])
def monitoring_root(request):
    """Return basic monitoring info (counts, status, etc)."""
    return Response({
        "agents_count": Agent.objects.count(),
        "workflows_count": Workflow.objects.count(),
        "db_status": db_status(),
    })

@api_view(["GET"])
def monitoring_stats(request):
    """Return system stats (can be expanded)."""
    # Example: return DB connection info and row counts
    stats = {
        "agents": Agent.objects.count(),
        "workflows": Workflow.objects.count(),
        "db_vendor": connection.vendor,
    }
    return Response(stats)

def db_status():
    try:
        connection.ensure_connection()
        return "ok"
    except Exception as e:
        return f"error: {e}"
