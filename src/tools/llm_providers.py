import os
import asyncio
from typing import Dict, Any

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")


_PROVIDERS = {}


def register_provider(name: str, func):
    _PROVIDERS[name] = func


def get_provider(name: str):
    return _PROVIDERS.get(name)


async def openai_generate(
    prompt: str, max_tokens: int = 256, temperature: float = 0.7
) -> Dict[str, Any]:
    """Simple wrapper for OpenAI completions - uses stub if key not present."""
    # If no API key, return stub
    if not OPENAI_KEY:
        await asyncio.sleep(0.05)
        return {
            "text": f"Stub OpenAI response for: {prompt[:100]}",
            "model": "gpt-stub",
            "tokens_used": len(prompt.split()) // 2,
            "finish_reason": "stop",
        }

    # Try to call the openai package if installed
    try:
        import openai

        openai.api_key = OPENAI_KEY
        # Use ChatCompletion where available; fall back to Completion
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = (
                resp.choices[0].message.content
                if hasattr(resp.choices[0], "message")
                else resp.choices[0].text
            )
            return {
                "text": text,
                "model": resp.model if hasattr(resp, "model") else "openai",
                "tokens_used": None,
                "finish_reason": "stop",
            }
        except Exception:
            resp = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
            text = resp.choices[0].text
            return {
                "text": text,
                "model": resp.model if hasattr(resp, "model") else "openai",
                "tokens_used": None,
                "finish_reason": "stop",
            }
    except Exception:
        # Fall back to stub if openai package not available or call fails
        await asyncio.sleep(0.05)
        return {
            "text": f"OpenAI response (simulated) for: {prompt[:100]}",
            "model": "gpt-sim",
            "tokens_used": 10,
            "finish_reason": "stop",
        }


async def anthropic_generate(
    prompt: str, max_tokens: int = 256, temperature: float = 0.7
) -> Dict[str, Any]:
    """Anthropic provider stub."""
    if not ANTHROPIC_KEY:
        await asyncio.sleep(0.05)
        return {
            "text": f"Stub Anthropic response for: {prompt[:100]}",
            "model": "claude-stub",
            "tokens_used": 8,
            "finish_reason": "stop",
        }
    await asyncio.sleep(0.05)
    return {
        "text": f"Anthropic response (simulated) for: {prompt[:100]}",
        "model": "claude-sim",
        "tokens_used": 8,
        "finish_reason": "stop",
    }


# Register defaults
register_provider("openai", openai_generate)
register_provider("anthropic", anthropic_generate)
