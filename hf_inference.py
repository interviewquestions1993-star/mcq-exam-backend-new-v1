"""
Ollama local model wrapper using OpenAI-compatible API.
"""
from openai import OpenAI
from backendv1.config import OLLAMA_BASE_URL, OLLAMA_API_KEY, OLLAMA_MODEL


class OllamaInference:
    """Wrapper for Ollama local model access via OpenAI-compatible endpoint."""

    def __init__(self):
        self.client = OpenAI(
            base_url=f"{OLLAMA_BASE_URL.rstrip('/')}/v1",
            api_key=OLLAMA_API_KEY
        )
        self.model = OLLAMA_MODEL
        print(f"DEBUG: Initialized Ollama client")
        print(f"DEBUG: Model: {self.model}")
        print(f"DEBUG: Base URL: {OLLAMA_BASE_URL}")

    def text_generation(
        self,
        prompt: str,
        max_new_tokens: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate text using a local Ollama model.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating text with Ollama: {e}")
            raise Exception(f"Failed to generate text: {str(e)}")


# Create singleton instance
hf_client = OllamaInference()
