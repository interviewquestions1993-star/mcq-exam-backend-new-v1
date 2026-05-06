"""
Hugging Face Inference Providers API wrapper using OpenAI-compatible endpoint
Uses the new unified endpoint: https://router.huggingface.co/v1
"""
from openai import OpenAI
from config import HF_TOKEN, HF_MODEL


class HuggingFaceInference:
    """Wrapper for Hugging Face Inference Providers (OpenAI-compatible API)"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=HF_TOKEN
        )
        self.model = HF_MODEL
        print(f"DEBUG: Initialized Inference Client")
        print(f"DEBUG: Model: {self.model}")
        print(f"DEBUG: Token provided: {bool(HF_TOKEN)}")
    
    def text_generation(
        self,
        prompt: str,
        max_new_tokens: int = 100,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate text using Hugging Face Inference Providers
        
        Args:
            prompt: Input text prompt
            max_new_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0.0 = deterministic, 1.0+ = random)
            top_p: Nucleus sampling parameter
        
        Returns:
            Generated text
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
            print(f"Error generating text: {e}")
            raise Exception(f"Failed to generate text: {str(e)}")


# Create singleton instance
hf_client = HuggingFaceInference()
