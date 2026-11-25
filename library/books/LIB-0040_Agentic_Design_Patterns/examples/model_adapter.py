"""Provider-agnostic LangChain chat model factory for LIB-0040 examples.

Only explicit provider selection; no automatic cloud fallback.
Supported: ollama, openai, gemini, anthropic, openai-compatible.
Install provider-specific integration packages listed in MODEL_PROVIDERS_RU.md.
"""
import os
from dataclasses import dataclass
from urllib.parse import urlparse

PROVIDERS = ("ollama", "openai", "gemini", "anthropic", "openai-compatible")
DEFAULT_MODELS = {
    "ollama": "ministral-3:8b",
    "openai": "gpt-4o-mini",
    "gemini": "gemini-2.5-flash",
    "anthropic": "claude-sonnet-4-5",
}
API_KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    base_url: str | None = None
    temperature: float = 0.0
    timeout: int = 45

    @classmethod
    def from_env(cls):
        provider = os.getenv("AGENT_LLM_PROVIDER", "ollama").strip().lower()
        model = os.getenv("AGENT_LLM_MODEL", DEFAULT_MODELS.get(provider, "")).strip()
        url = os.getenv("AGENT_LLM_BASE_URL", "").strip() or None
        temperature = float(os.getenv("AGENT_LLM_TEMPERATURE", "0"))
        timeout = int(os.getenv("AGENT_LLM_TIMEOUT", "45"))
        return cls(provider, model, url, temperature, timeout)

    def validate(self):
        if self.provider not in PROVIDERS:
            raise ValueError(f"Unknown provider {self.provider!r}. Supported: {PROVIDERS}")
        if not self.model:
            raise ValueError("AGENT_LLM_MODEL is required for this provider")
        if not 0 <= self.temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        if self.timeout < 1:
            raise ValueError("Timeout must be a positive number of seconds")
        if self.provider == "openai-compatible" and not self.base_url:
            raise ValueError("AGENT_LLM_BASE_URL is required for openai-compatible API")
        if self.base_url:
            parsed = urlparse(self.base_url)
            if not parsed.hostname or parsed.scheme not in {"http", "https"}:
                raise ValueError("AGENT_LLM_BASE_URL must be a valid HTTP(S) URL")
            if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
                raise ValueError("Unencrypted HTTP is restricted to local loopback; use HTTPS for remote endpoints")
        if self.provider in API_KEYS and not os.getenv(API_KEYS[self.provider]):
            raise ValueError(f"Missing environment variable {API_KEYS[self.provider]}")
        if self.provider == "openai-compatible":
            # A dummy key is sufficient only when the local server needs no authentication.
            if not os.getenv("AGENT_LLM_API_KEY") and (
                urlparse(self.base_url).hostname not in {"localhost", "127.0.0.1", "::1"}
            ):
                raise ValueError("Set AGENT_LLM_API_KEY for remote compatible endpoints")


def create_chat_model(config: ModelConfig):
    """Create a LangChain BaseChatModel from configuration (no request issued)."""
    config.validate()
    common = {"model": config.model, "temperature": config.temperature}
    if config.provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError as exc:
            raise RuntimeError("Install: python -m pip install langchain-ollama") from exc
        return ChatOllama(**common, base_url=config.base_url or "http://127.0.0.1:11434")
    if config.provider in {"openai", "openai-compatible"}:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise RuntimeError("Install: python -m pip install langchain-openai") from exc
        options = dict(common, timeout=config.timeout, max_retries=2)
        if config.provider == "openai-compatible":
            options["base_url"] = config.base_url
            options["api_key"] = os.getenv("AGENT_LLM_API_KEY", "local-only-placeholder")
            options["use_responses_api"] = False
        return ChatOpenAI(**options)
    if config.provider == "gemini":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as exc:
            raise RuntimeError("Install: python -m pip install langchain-google-genai") from exc
        return ChatGoogleGenerativeAI(**common)
    if config.provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as exc:
            raise RuntimeError("Install: python -m pip install langchain-anthropic") from exc
        return ChatAnthropic(**common)
    raise AssertionError("Provider validation should have rejected this value")
