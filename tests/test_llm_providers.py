import os
import asyncio

from src.tools.llm_tool import LLMTool


def test_llm_tool_provider_fallback():
    # Ensure provider env var picks up registered provider
    os.environ["LLM_PROVIDER"] = "openai"
    tool = LLMTool(name="test_llm", model_name="gpt-stub")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(tool.generate_async("Hello world"))
    assert res is not None
    assert hasattr(res, "text")
