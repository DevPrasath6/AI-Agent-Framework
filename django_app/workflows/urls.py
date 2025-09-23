from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet, WorkflowRunViewSet
router = DefaultRouter()
router.register('', WorkflowViewSet, basename='workflow')
router.register('runs', WorkflowRunViewSet, basename='workflowrun')
urlpatterns = [path('', include(router.urls)),]
