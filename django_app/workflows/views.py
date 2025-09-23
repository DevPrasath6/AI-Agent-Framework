from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Workflow, WorkflowRun
from .serializers import WorkflowSerializer, WorkflowRunSerializer
from .adapters import enqueue_workflow_run


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        wf = self.get_object()
        payload = request.data.get("input", {})
        run = WorkflowRun.objects.create(workflow=wf, input=payload, status="QUEUED")
        enqueue_workflow_run(str(run.id), str(wf.id), payload)
        return Response(WorkflowRunSerializer(run).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def definition(self, request, pk=None):
        wf = self.get_object()
        raw = wf.yaml_definition
        # Try to parse as JSON first, else return raw
        try:
            import json

            parsed = json.loads(raw)
            return Response(parsed)
        except Exception:
            return Response({"yaml_definition": raw})


class WorkflowRunViewSet(viewsets.ModelViewSet):
    queryset = WorkflowRun.objects.all()
    serializer_class = WorkflowRunSerializer
