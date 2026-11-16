"""Fast NVIDIA-hosted text generation with a bounded fallback path."""

import logging
import time

from openai import OpenAI

try:
    from .config import (
        NVIDIA_API_KEY,
        NVIDIA_MODELS,
        NVIDIA_MODEL_TIMEOUT_SECONDS,
        NVIDIA_TOTAL_TIMEOUT_SECONDS,
    )
except ImportError:
    from config import (
        NVIDIA_API_KEY,
        NVIDIA_MODELS,
        NVIDIA_MODEL_TIMEOUT_SECONDS,
        NVIDIA_TOTAL_TIMEOUT_SECONDS,
    )


logger = logging.getLogger(__name__)


class NVIDIAInference:
    """Call a fast primary model and at most one bounded fallback."""

    def text_generation(
        self,
        prompt: str,
        max_new_tokens: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        if not NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY is not set")

        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY,
            max_retries=0,
        )
        deadline = time.monotonic() + NVIDIA_TOTAL_TIMEOUT_SECONDS
        last_error = None

        for current_model in NVIDIA_MODELS:
            remaining_seconds = deadline - time.monotonic()
            if remaining_seconds <= 0:
                break

            attempt_timeout = min(
                NVIDIA_MODEL_TIMEOUT_SECONDS,
                remaining_seconds,
            )
            try:
                logger.info(
                    "Attempting MCQ generation with %s (timeout %.1fs)",
                    current_model,
                    attempt_timeout,
                )
                completion = client.chat.completions.create(
                    model=current_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature,
                    top_p=top_p,
                    max_tokens=max_new_tokens,
                    stream=False,
                    timeout=attempt_timeout,
                )

                if not completion.choices:
                    raise ValueError("AI response contained no choices")

                content = completion.choices[0].message.content or ""
                if not content.strip():
                    raise ValueError("AI response contained no text")

                return content
            except Exception as exc:
                last_error = exc
                logger.warning("Model %s failed: %s", current_model, exc)

        if last_error is None:
            last_error = TimeoutError(
                f"AI generation exceeded {NVIDIA_TOTAL_TIMEOUT_SECONDS:.0f} seconds"
            )
        raise RuntimeError(f"AI generation failed after bounded fallbacks: {last_error}")


hf_client = NVIDIAInference()
