"""
Customer Support Agent - Reference implementation for customer service workflows.

This agent demonstrates:
- Multi-step conversation handling
- Knowledge base integration
- Sentiment analysis
- Human-in-the-loop escalation
- Ticket creation and tracking
"""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.agent_base import AgentBase, AgentCapability
from src.core.execution_context import ExecutionContext
from src.core.workflow_base import WorkflowDefinition, WorkflowStep, StepType, SimpleDAGWorkflow
from src.tools.llm_tool import ConversationLLMTool


class CustomerSupportAgent(AgentBase):
    """
    Customer support agent with conversation management and escalation capabilities.
    """

    def __init__(
        self,
        name: str = "customer_support_agent",
        llm_config: Optional[Dict[str, Any]] = None,
        knowledge_base: Optional[Dict[str, Any]] = None,
        escalation_threshold: float = 0.7,
        **kwargs
    ):
        """
        Initialize customer support agent.

        Args:
            name: Agent name
            llm_config: Configuration for LLM tool
            knowledge_base: Knowledge base for FAQ and solutions
            escalation_threshold: Sentiment threshold for human escalation
            **kwargs: Additional agent configuration
        """
        super().__init__(
            name=name,
            description="AI-powered customer support agent with escalation capabilities",
            capabilities=[
                AgentCapability.CONVERSATION,
                AgentCapability.TEXT_PROCESSING,
                AgentCapability.WORKFLOW_ORCHESTRATION
            ],
            **kwargs
        )

        # Initialize LLM tool for conversations
        self.llm_tool = ConversationLLMTool(
            name="support_llm",
            **(llm_config or {})
        )

        # Knowledge base for FAQ and solutions
        self.knowledge_base = knowledge_base or self._get_default_knowledge_base()

        # Configuration
        self.escalation_threshold = escalation_threshold
        self.max_conversation_turns = 10

        # Support ticket tracking
        self.active_tickets: Dict[str, Dict[str, Any]] = {}
        self.ticket_counter = 0

    async def execute(
        self,
        input_data: Any,
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Execute customer support workflow."""
        # Parse customer inquiry
        inquiry = self._parse_inquiry(input_data)

        # Get or create session for conversation tracking
        session_id = context.session_id or "default"

        # Analyze inquiry sentiment and urgency
        analysis = await self._analyze_inquiry(inquiry, context)

        # Check if human escalation is needed
        if analysis["sentiment_score"] < self.escalation_threshold or analysis["requires_human"]:
            return await self._escalate_to_human(inquiry, analysis, context)

        # Search knowledge base for relevant information
        kb_results = await self._search_knowledge_base(inquiry, context)

        # Generate response using LLM with knowledge base context
        response = await self._generate_response(
            inquiry, kb_results, analysis, session_id, context
        )

        # Check if issue is resolved or needs follow-up
        resolution_status = await self._assess_resolution(response, context)

        # Create or update support ticket if needed
        ticket_info = await self._manage_ticket(
            inquiry, response, resolution_status, session_id, context
        )

        return {
            "response": response,
            "analysis": analysis,
            "knowledge_base_matches": kb_results,
            "resolution_status": resolution_status,
            "ticket_info": ticket_info,
            "requires_human_escalation": analysis["requires_human"],
            "session_id": session_id
        }

    def _parse_inquiry(self, input_data: Any) -> str:
        """Parse customer inquiry from input data."""
        if isinstance(input_data, str):
            return input_data
        elif isinstance(input_data, dict):
            return input_data.get("message", input_data.get("inquiry", str(input_data)))
        else:
            return str(input_data)

    async def _analyze_inquiry(
        self,
        inquiry: str,
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Analyze customer inquiry for sentiment and urgency."""
        # Simple sentiment analysis (in practice, use a proper sentiment analyzer)
        negative_words = ["angry", "frustrated", "terrible", "awful", "hate", "broken", "urgent"]
        positive_words = ["thanks", "great", "good", "excellent", "love", "perfect"]

        inquiry_lower = inquiry.lower()
        negative_count = sum(1 for word in negative_words if word in inquiry_lower)
        positive_count = sum(1 for word in positive_words if word in inquiry_lower)

        # Calculate sentiment score (0.0 = very negative, 1.0 = very positive)
        sentiment_score = max(0.0, min(1.0, (positive_count - negative_count + 2) / 4))

        # Check for urgency indicators
        urgent_indicators = ["urgent", "emergency", "asap", "immediately", "critical"]
        is_urgent = any(indicator in inquiry_lower for indicator in urgent_indicators)

        # Check for complex issues that need human attention
        complex_indicators = ["billing", "refund", "cancel", "subscription", "legal"]
        requires_human = any(indicator in inquiry_lower for indicator in complex_indicators)

        return {
            "sentiment_score": sentiment_score,
            "is_urgent": is_urgent,
            "requires_human": requires_human or sentiment_score < self.escalation_threshold,
            "detected_keywords": [word for word in negative_words + positive_words if word in inquiry_lower],
            "analysis_timestamp": datetime.utcnow().isoformat()
        }

    async def _search_knowledge_base(
        self,
        inquiry: str,
        context: ExecutionContext
    ) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant information."""
        inquiry_lower = inquiry.lower()
        matches = []

        for category, items in self.knowledge_base.items():
            for item in items:
                # Simple keyword matching (in practice, use semantic search)
                keywords = item.get("keywords", [])
                if any(keyword.lower() in inquiry_lower for keyword in keywords):
                    matches.append({
                        "category": category,
                        "title": item["title"],
                        "content": item["content"],
                        "relevance_score": self._calculate_relevance(inquiry, item["keywords"])
                    })

        # Sort by relevance score
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)

        return matches[:3]  # Return top 3 matches

    def _calculate_relevance(self, inquiry: str, keywords: List[str]) -> float:
        """Calculate relevance score for knowledge base item."""
        inquiry_lower = inquiry.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in inquiry_lower)
        return matches / len(keywords) if keywords else 0.0

    async def _generate_response(
        self,
        inquiry: str,
        kb_results: List[Dict[str, Any]],
        analysis: Dict[str, Any],
        session_id: str,
        context: ExecutionContext
    ) -> str:
        """Generate response using LLM with knowledge base context."""
        # Build context for LLM
        kb_context = "\n".join([
            f"- {result['title']}: {result['content']}"
            for result in kb_results
        ]) if kb_results else "No specific knowledge base matches found."

        system_message = f"""You are a helpful customer support agent. Use the following knowledge base information to help answer the customer's question:

Knowledge Base:
{kb_context}

Guidelines:
- Be helpful, polite, and professional
- Use the knowledge base information when relevant
- If you cannot fully resolve the issue, let them know you can escalate to a human agent
- Keep responses concise but thorough
- Show empathy if the customer seems frustrated
"""

        # Generate response using conversation LLM
        response = await self.llm_tool.chat(
            message=inquiry,
            session_id=session_id,
            system_message=system_message,
            context=context
        )

        return response.text

    async def _assess_resolution(
        self,
        response: str,
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Assess if the issue has been resolved."""
        # Simple resolution assessment (in practice, use ML model)
        resolution_indicators = [
            "solved", "resolved", "fixed", "working", "complete",
            "should work now", "try this", "follow these steps"
        ]

        response_lower = response.lower()
        resolution_score = sum(1 for indicator in resolution_indicators if indicator in response_lower)

        is_resolved = resolution_score > 0
        needs_followup = "follow up" in response_lower or "let me know" in response_lower

        return {
            "is_resolved": is_resolved,
            "needs_followup": needs_followup,
            "resolution_score": resolution_score,
            "assessment_timestamp": datetime.utcnow().isoformat()
        }

    async def _manage_ticket(
        self,
        inquiry: str,
        response: str,
        resolution_status: Dict[str, Any],
        session_id: str,
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Create or update support ticket."""
        ticket_id = f"TICKET_{self.ticket_counter:06d}"

        if session_id not in self.active_tickets:
            # Create new ticket
            self.ticket_counter += 1
            self.active_tickets[session_id] = {
                "ticket_id": ticket_id,
                "status": "open",
                "created_at": datetime.utcnow().isoformat(),
                "customer_inquiry": inquiry,
                "conversation_history": [],
                "resolution_attempts": 0
            }

        ticket = self.active_tickets[session_id]

        # Update ticket with current interaction
        ticket["conversation_history"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "customer_message": inquiry,
            "agent_response": response,
            "resolution_status": resolution_status
        })

        ticket["resolution_attempts"] += 1
        ticket["last_updated"] = datetime.utcnow().isoformat()

        # Update ticket status based on resolution
        if resolution_status["is_resolved"]:
            ticket["status"] = "resolved"
        elif ticket["resolution_attempts"] >= 3:
            ticket["status"] = "escalated"

        return {
            "ticket_id": ticket["ticket_id"],
            "status": ticket["status"],
            "resolution_attempts": ticket["resolution_attempts"],
            "created_at": ticket["created_at"]
        }

    async def _escalate_to_human(
        self,
        inquiry: str,
        analysis: Dict[str, Any],
        context: ExecutionContext
    ) -> Dict[str, Any]:
        """Escalate inquiry to human agent."""
        escalation_reason = []

        if analysis["sentiment_score"] < self.escalation_threshold:
            escalation_reason.append("negative_sentiment")
        if analysis["is_urgent"]:
            escalation_reason.append("urgent_request")
        if analysis["requires_human"]:
            escalation_reason.append("complex_issue")

        escalation_id = f"ESC_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        return {
            "response": "I understand this is important to you. Let me connect you with one of our human specialists who can better assist you with this matter.",
            "escalation_id": escalation_id,
            "escalation_reason": escalation_reason,
            "requires_human_escalation": True,
            "priority": "high" if analysis["is_urgent"] else "normal",
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _get_default_knowledge_base(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get default knowledge base for customer support."""
        return {
            "account_issues": [
                {
                    "title": "Password Reset",
                    "content": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and follow the instructions in the email you receive.",
                    "keywords": ["password", "reset", "forgot", "login", "access"]
                },
                {
                    "title": "Account Locked",
                    "content": "If your account is locked due to multiple failed login attempts, it will automatically unlock after 30 minutes. You can also contact support to unlock it immediately.",
                    "keywords": ["locked", "account", "login", "attempts", "unlock"]
                }
            ],
            "billing": [
                {
                    "title": "Payment Issues",
                    "content": "If you're experiencing payment issues, please check that your payment method is valid and has sufficient funds. You can update your payment method in Account Settings.",
                    "keywords": ["payment", "billing", "charge", "card", "declined"]
                },
                {
                    "title": "Refund Policy",
                    "content": "We offer refunds within 30 days of purchase. Please contact our billing department with your order number for refund requests.",
                    "keywords": ["refund", "return", "money", "back", "cancel"]
                }
            ],
            "technical_support": [
                {
                    "title": "App Not Working",
                    "content": "If the app is not working properly, try clearing your browser cache or updating to the latest version. If the problem persists, please provide details about the error you're seeing.",
                    "keywords": ["app", "not working", "broken", "error", "bug", "crash"]
                },
                {
                    "title": "Slow Performance",
                    "content": "Slow performance can be caused by network issues or browser problems. Try refreshing the page, checking your internet connection, or using a different browser.",
                    "keywords": ["slow", "performance", "loading", "speed", "lag"]
                }
            ]
        }

    def get_ticket_summary(self) -> Dict[str, Any]:
        """Get summary of all support tickets."""
        total_tickets = len(self.active_tickets)
        open_tickets = sum(1 for ticket in self.active_tickets.values() if ticket["status"] == "open")
        resolved_tickets = sum(1 for ticket in self.active_tickets.values() if ticket["status"] == "resolved")
        escalated_tickets = sum(1 for ticket in self.active_tickets.values() if ticket["status"] == "escalated")

        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "resolved_tickets": resolved_tickets,
            "escalated_tickets": escalated_tickets,
            "resolution_rate": (resolved_tickets / max(total_tickets, 1)) * 100,
            "escalation_rate": (escalated_tickets / max(total_tickets, 1)) * 100
        }


# Define customer support workflow
def create_customer_support_workflow() -> SimpleDAGWorkflow:
    """Create a customer support workflow definition."""

    workflow_definition = WorkflowDefinition(
        id="customer_support_v1",
        name="Customer Support Workflow",
        description="Automated customer support with human escalation",
        steps=[
            WorkflowStep(
                id="analyze_inquiry",
                name="Analyze Customer Inquiry",
                step_type=StepType.AGENT,
                config={"agent_name": "customer_support_agent"},
                dependencies=[]
            ),
            WorkflowStep(
                id="check_escalation",
                name="Check for Human Escalation",
                step_type=StepType.CONDITION,
                config={
                    "condition": "input.get('requires_human_escalation', False)",
                    "true_value": "escalate",
                    "false_value": "continue"
                },
                dependencies=["analyze_inquiry"]
            ),
            WorkflowStep(
                id="generate_followup",
                name="Generate Follow-up",
                step_type=StepType.AGENT,
                config={"agent_name": "customer_support_agent"},
                dependencies=["check_escalation"],
                condition="input != 'escalate'"
            )
        ],
        metadata={
            "version": "1.0",
            "author": "AI Agent Framework",
            "tags": ["customer_support", "conversation", "escalation"]
        }
    )

    # Create agent registry
    agent_registry = {
        "customer_support_agent": CustomerSupportAgent()
    }

    return SimpleDAGWorkflow(
        definition=workflow_definition,
        agent_registry=agent_registry
    )


# Example usage and flow definition for legacy compatibility
flow = {
    'flow_id': 'support_v1',
    'description': 'Customer support flow with AI agent and human escalation',
    'tasks': [
        {
            'id': 'intake',
            'type': 'agent_execution',
            'agent': 'customer_support_agent',
            'config': {
                'max_turns': 5,
                'escalation_threshold': 0.7
            }
        },
        {
            'id': 'human_escalation',
            'type': 'human_in_loop',
            'condition': 'requires_escalation',
            'config': {
                'timeout': 3600,  # 1 hour
                'priority': 'normal'
            }
        },
        {
            'id': 'ticket_creation',
            'type': 'data_persistence',
            'config': {
                'store_conversation': True,
                'create_ticket': True
            }
        }
    ],
    'metadata': {
        'version': '1.0',
        'created_by': 'ai_agent_framework'
    }
}
from src.sdk.agents import register_agent

# Register an instance for SDK discovery
try:
    register_agent(CustomerSupportAgent())
except Exception:
    # Registration is best-effort for local dev
    pass
