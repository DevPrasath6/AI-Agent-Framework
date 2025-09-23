"""
LLM tool for language model interactions and text generation.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from ..core.tool_base import ToolBase, ToolType
from ..core.execution_context import ExecutionContext


@dataclass
class LLMRequest:
    """Request structure for LLM interactions."""

    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    system_message: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = None

    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []


@dataclass
class LLMResponse:
    """Response structure from LLM."""

    text: str
    model: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class LLMTool(ToolBase):
    """
    Tool for interacting with Language Learning Models.

    Supports various LLM providers and configurations.
    """

    def __init__(
        self,
        name: str = "llm_tool",
        model_name: str = "gpt-3.5-turbo",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        timeout: int = 30,
        **kwargs,
    ):
        """
        Initialize LLM tool.

        Args:
            name: Tool name
            model_name: Name of the LLM model to use
            api_key: API key for the LLM service
            base_url: Base URL for the LLM API
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            timeout: Request timeout in seconds
            **kwargs: Additional configuration
        """
        super().__init__(
            name=name,
            description=f"Language model tool using {model_name}",
            tool_type=ToolType.LLM,
            timeout=timeout,
            **kwargs,
        )

        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature

        # Statistics
        self.total_tokens_used = 0
        self.total_requests = 0

        # Legacy configuration support
        self.cfg = {
            "model_name": model_name,
            "api_key": api_key,
            "base_url": base_url,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

    async def _execute_tool(
        self, payload: Any, context: ExecutionContext
    ) -> LLMResponse:
        """Execute LLM generation."""
        # Parse input payload
        llm_request = self._parse_request(payload)

        # Generate response
        response = await self._generate_response(llm_request, context)

        # Update statistics
        self.total_requests += 1
        if response.tokens_used:
            self.total_tokens_used += response.tokens_used

        return response

    def _parse_request(self, payload: Any) -> LLMRequest:
        """Parse input payload into LLM request."""
        if isinstance(payload, str):
            # Simple string prompt
            return LLMRequest(prompt=payload)

        elif isinstance(payload, dict):
            # Dictionary with prompt and options
            return LLMRequest(
                prompt=payload.get("prompt", ""),
                max_tokens=payload.get("max_tokens", self.max_tokens),
                temperature=payload.get("temperature", self.temperature),
                system_message=payload.get("system_message"),
                conversation_history=payload.get("conversation_history", []),
            )

        elif isinstance(payload, LLMRequest):
            # Already parsed request
            return payload

        else:
            # Convert to string as fallback
            return LLMRequest(prompt=str(payload))

    async def _generate_response(
        self, request: LLMRequest, context: ExecutionContext
    ) -> LLMResponse:
        """Generate response from LLM."""
        try:
            # Prefer provider selected via environment/configuration
            import os

            provider_name = os.getenv("LLM_PROVIDER", None)
            if provider_name:
                try:
                    from .llm_providers import get_provider

                    provider = get_provider(provider_name)
                    if provider:
                        out = await provider(
                            request.prompt,
                            max_tokens=request.max_tokens or self.max_tokens,
                            temperature=request.temperature or self.temperature,
                        )
                        return LLMResponse(
                            text=out.get("text", ""),
                            model=out.get("model", self.model_name),
                            tokens_used=out.get("tokens_used"),
                            finish_reason=out.get("finish_reason"),
                            metadata=out,
                        )
                except Exception:
                    pass

            # Fallback heuristics based on model name
            if self.model_name.startswith("gpt"):
                return await self._call_openai_api(request)
            elif self.model_name.startswith("claude"):
                return await self._call_anthropic_api(request)
            elif self.model_name.startswith("llama"):
                return await self._call_local_llama(request)
            else:
                return await self._call_generic_api(request)

        except Exception as e:
            self.logger.error(f"LLM generation failed: {e}")
            # Return a fallback response
            return LLMResponse(
                text=f"Error: Unable to generate response - {str(e)}",
                model=self.model_name,
                finish_reason="error",
                metadata={"error": str(e)},
            )

    async def _call_openai_api(self, request: LLMRequest) -> LLMResponse:
        """Call OpenAI API (delegates to provider adapter)."""
        self.logger.info(f"Calling OpenAI provider for model {self.model_name}")

        try:
            from .llm_providers import openai_generate
        except Exception:
            openai_generate = None

        # Prefer provider adapter if available
        if openai_generate is not None:
            out = await openai_generate(
                request.prompt,
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature or self.temperature,
            )
            return LLMResponse(
                text=out.get("text", ""),
                model=out.get("model", self.model_name),
                tokens_used=out.get("tokens_used"),
                finish_reason=out.get("finish_reason"),
                metadata=out,
            )

        # Fallback stub
        await self._simulate_api_delay()
        response_text = f"Generated response for prompt: {request.prompt[:50]}..."
        return LLMResponse(
            text=response_text,
            model=self.model_name,
            tokens_used=len(response_text.split()),
            finish_reason="stop",
            metadata={"provider": "openai_stub"},
        )

    async def _call_anthropic_api(self, request: LLMRequest) -> LLMResponse:
        """Call Anthropic API (stub implementation)."""
        self.logger.info(f"Calling Anthropic API with model {self.model_name}")

        await self._simulate_api_delay()

        response_text = f"Claude response for: {request.prompt[:50]}..."

        return LLMResponse(
            text=response_text,
            model=self.model_name,
            tokens_used=len(response_text.split()),
            finish_reason="stop",
            metadata={"provider": "anthropic"},
        )

    async def _call_local_llama(self, request: LLMRequest) -> LLMResponse:
        """Call local Llama model (stub implementation)."""
        self.logger.info(f"Calling local Llama model {self.model_name}")

        await self._simulate_api_delay()

        response_text = f"Llama response for: {request.prompt[:50]}..."

        return LLMResponse(
            text=response_text,
            model=self.model_name,
            tokens_used=len(response_text.split()),
            finish_reason="stop",
            metadata={"provider": "local_llama"},
        )

    async def _call_generic_api(self, request: LLMRequest) -> LLMResponse:
        """Call generic LLM API (stub implementation)."""
        self.logger.info(f"Calling generic API with model {self.model_name}")

        await self._simulate_api_delay()

        response_text = f"Generic LLM response for: {request.prompt[:50]}..."

        return LLMResponse(
            text=response_text,
            model=self.model_name,
            tokens_used=len(response_text.split()),
            finish_reason="stop",
            metadata={"provider": "generic"},
        )

    async def _simulate_api_delay(self) -> None:
        """Simulate API call delay."""
        import asyncio

        await asyncio.sleep(0.1)  # Simulate 100ms API delay

    def generate(self, prompt: str) -> Dict[str, str]:
        """
        Legacy sync generation method for backward compatibility.

        Args:
            prompt: Text prompt for generation

        Returns:
            Dictionary with generated text
        """
        # For legacy compatibility, return a stub response
        return {
            "text": f"Stub response for: {prompt[:50]}...",
            "model": self.model_name,
            "tokens": str(len(prompt.split()) + 10),
        }

    async def generate_async(
        self, prompt: str, context: Optional[ExecutionContext] = None
    ) -> LLMResponse:
        """
        Async generation method.

        Args:
            prompt: Text prompt for generation
            context: Optional execution context

        Returns:
            LLM response object
        """
        if context is None:
            context = ExecutionContext()

        request = LLMRequest(prompt=prompt)
        return await self._generate_response(request, context)

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get LLM usage statistics."""
        avg_tokens = self.total_tokens_used / max(self.total_requests, 1)

        return {
            "total_requests": self.total_requests,
            "total_tokens_used": self.total_tokens_used,
            "average_tokens_per_request": avg_tokens,
            "model_name": self.model_name,
            "tool_executions": self.execution_count,
            "success_rate": (
                (self.execution_count - self.error_count) / max(self.execution_count, 1)
            )
            * 100,
        }


class ConversationLLMTool(LLMTool):
    """
    LLM tool with conversation history management.
    """

    def __init__(self, max_history_length: int = 10, **kwargs):
        """
        Initialize conversation LLM tool.

        Args:
            max_history_length: Maximum conversation history length
            **kwargs: Additional LLM tool configuration
        """
        super().__init__(**kwargs)
        self.max_history_length = max_history_length
        self.conversation_histories: Dict[str, List[Dict[str, str]]] = {}

    async def chat(
        self,
        message: str,
        session_id: str = "default",
        system_message: Optional[str] = None,
        context: Optional[ExecutionContext] = None,
    ) -> LLMResponse:
        """
        Have a conversation with the LLM.

        Args:
            message: User message
            session_id: Conversation session ID
            system_message: Optional system message
            context: Optional execution context

        Returns:
            LLM response
        """
        if context is None:
            context = ExecutionContext()

        # Get or create conversation history
        if session_id not in self.conversation_histories:
            self.conversation_histories[session_id] = []

        history = self.conversation_histories[session_id]

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Trim history if too long
        if len(history) > self.max_history_length:
            history = history[-self.max_history_length :]
            self.conversation_histories[session_id] = history

        # Create request with conversation history
        request = LLMRequest(
            prompt=message, conversation_history=history, system_message=system_message
        )

        # Generate response
        response = await self._generate_response(request, context)

        # Add assistant response to history
        history.append({"role": "assistant", "content": response.text})

        return response

    def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation history for a session."""
        if session_id in self.conversation_histories:
            del self.conversation_histories[session_id]
            return True
        return False

    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session."""
        return self.conversation_histories.get(session_id, [])
