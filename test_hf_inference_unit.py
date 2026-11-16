import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch


os.environ.setdefault("NVIDIA_API_KEY", "test-key")

import hf_inference


def completion_with(content):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


class FakeCompletions:
    def __init__(self, results):
        self.results = iter(results)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        result = next(self.results)
        if isinstance(result, Exception):
            raise result
        return result


class NVIDIAInferenceTests(unittest.TestCase):
    def make_client(self, results):
        completions = FakeCompletions(results)
        fake_client = SimpleNamespace(
            chat=SimpleNamespace(completions=completions)
        )
        return fake_client, completions

    def test_fast_primary_has_no_hidden_retries_or_reasoning(self):
        fake_client, completions = self.make_client([
            completion_with('{"questions": []}')
        ])

        with patch.object(hf_inference, "OpenAI", return_value=fake_client) as factory:
            result = hf_inference.NVIDIAInference().text_generation(
                "Generate one question",
                800,
            )

        self.assertEqual(result, '{"questions": []}')
        self.assertEqual(factory.call_args.kwargs["max_retries"], 0)
        self.assertEqual(len(completions.calls), 1)
        call = completions.calls[0]
        self.assertEqual(call["model"], hf_inference.NVIDIA_MODELS[0])
        self.assertFalse(call["stream"])
        self.assertNotIn("extra_body", call)
        self.assertLessEqual(
            call["timeout"],
            hf_inference.NVIDIA_MODEL_TIMEOUT_SECONDS,
        )

    def test_uses_one_fallback_after_primary_failure(self):
        fake_client, completions = self.make_client([
            RuntimeError("primary unavailable"),
            completion_with('{"questions": [{"question": "fallback"}]}'),
        ])

        with patch.object(hf_inference, "OpenAI", return_value=fake_client):
            result = hf_inference.NVIDIAInference().text_generation(
                "Generate one question",
                800,
            )

        self.assertIn("fallback", result)
        self.assertEqual(
            [call["model"] for call in completions.calls],
            hf_inference.NVIDIA_MODELS[:2],
        )


if __name__ == "__main__":
    unittest.main()
