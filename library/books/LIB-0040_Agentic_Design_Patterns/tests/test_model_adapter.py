"""Offline unit tests; no API calls; no LLM package required for model_adapter."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from model_adapter import ModelConfig, create_chat_model

class ModelAdapterTests(unittest.TestCase):
    def test_default_ollama(self):
        with patch.dict(os.environ, {}, clear=True):
            cfg = ModelConfig.from_env()
            self.assertEqual(cfg.provider, "ollama")
            self.assertEqual(cfg.model, "ministral-3:8b")
            cfg.validate()

    def test_missing_cloud_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY"):
                ModelConfig("openai", "gpt-4o-mini").validate()

    def test_missing_compatible_url(self):
        with self.assertRaisesRegex(ValueError, "BASE_URL"):
            ModelConfig("openai-compatible", "local-model").validate()

    def test_prevent_plaintext_remote_endpoint(self):
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            ModelConfig("openai-compatible", "local-model", "http://example.org/v1").validate()

    def test_local_compatible_no_key(self):
        with patch.dict(os.environ, {}, clear=True):
            ModelConfig("openai-compatible", "local-model", "http://127.0.0.1:8080/v1").validate()

    def test_remote_compatible_requires_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "AGENT_LLM_API_KEY"):
                ModelConfig("openai-compatible", "remote-model", "https://example.org/v1").validate()

    def test_invalid_provider(self):
        with self.assertRaisesRegex(ValueError, "Unknown provider"):
            ModelConfig("no-such-provider", "anything").validate()

    def test_missing_model(self):
        with self.assertRaisesRegex(ValueError, "AGENT_LLM_MODEL"):
            ModelConfig("ollama", "").validate()

    def test_provider_not_loaded_until_factory(self):
        # Validate should need only stdlib.
        ModelConfig("ollama", "qwen3:8b").validate()

if __name__ == "__main__":
    unittest.main()
