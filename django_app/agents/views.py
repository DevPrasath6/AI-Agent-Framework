from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Agent, AgentRun
from .serializers import AgentSerializer, AgentRunSerializer
from src.sdk.agents import list_agents, get_agent


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    @action(detail=True, methods=["post"])
    def start(self, request, pk=None):
        agent = self.get_object()
        payload = request.data.get("input", {})
        run = AgentRun.objects.create(
            agent=agent, input_payload=payload, status="QUEUED"
        )
        from ..workflows.adapters import enqueue_agent_run

        enqueue_agent_run(str(run.id), agent.id, payload)
        return Response(AgentRunSerializer(run).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def available(self, request):
        """List in-memory SDK-registered agents available for registration."""
        keys = list_agents()
        return Response({"agents": keys})

    @action(detail=False, methods=["post"])
    def register_from_sdk(self, request):
        """Create a DB Agent from an SDK-registered agent name."""
        name = request.data.get("name")
        if not name:
            return Response(
                {"error": "name required"}, status=status.HTTP_400_BAD_REQUEST
            )
        a = get_agent(name)
        if a is None:
            return Response(
                {"error": "agent not found in SDK registry"},
                status=status.HTTP_404_NOT_FOUND,
            )
        # Create DB record
        agent = Agent.objects.create(
            name=getattr(a, "name", name), description=getattr(a, "description", "")
        )
        return Response(AgentSerializer(agent).data, status=status.HTTP_201_CREATED)


class AgentRunViewSet(viewsets.ModelViewSet):
    queryset = AgentRun.objects.all()
    serializer_class = AgentRunSerializer
