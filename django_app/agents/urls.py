from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AgentViewSet, AgentRunViewSet

router = DefaultRouter()
router.register("", AgentViewSet, basename="agent")
router.register("runs", AgentRunViewSet, basename="agentrun")
urlpatterns = [
    path("", include(router.urls)),
]
