from django.urls import path
from .views import health, monitoring_root, monitoring_stats

urlpatterns = [
    path("health/", health),
    path("", monitoring_root),
    path("stats/", monitoring_stats),
]
