from django.contrib import admin
from .models import Workflow, WorkflowRun


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at')
	search_fields = ('name',)


@admin.register(WorkflowRun)
class WorkflowRunAdmin(admin.ModelAdmin):
	list_display = ('id', 'workflow', 'status', 'created_at', 'updated_at')
	search_fields = ('workflow__name', 'id')
