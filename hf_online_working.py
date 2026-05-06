"""
Official Hugging Face InferenceClient Implementation - WORKING EXAMPLE
This uses the official huggingface_hub library for online inference
"""

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the official InferenceClient
HF_TOKEN = os.getenv("HF_TOKEN", "")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables")

# Create client with api_key parameter (official way)
client = InferenceClient(api_key=HF_TOKEN)

def text_generation_example():
    """
    Official example: Simple text generation
    This is exactly how it works in the Hugging Face documentation
    """
    print("=" * 60)
    print("EXAMPLE 1: Simple Text Generation (Official Way)")
    print("=" * 60)
    
    try:
        # Official InferenceClient text_generation method
        response = client.text_generation(
            prompt="The future of artificial intelligence is",
            model="gpt2",
            max_new_tokens=50,
            temperature=0.7,
        )
        
        # Returns string directly
        print(f"Prompt: The future of artificial intelligence is")
        print(f"Generated: {response}")
        print()
        return response
    except Exception as e:
        print(f"Error: {e}")
        print()


def text_generation_with_gemma():
    """
    Using a more powerful model - Gemma 2B
    """
    print("=" * 60)
    print("EXAMPLE 2: Text Generation with Gemma 2B")
    print("=" * 60)
    
    try:
        response = client.text_generation(
            prompt="Explain quantum computing in simple terms:",
            model="google/gemma-2-2b-it",
            max_new_tokens=100,
            temperature=0.7,
            top_p=0.95,
        )
        
        print(f"Prompt: Explain quantum computing in simple terms:")
        print(f"Generated: {response}")
        print()
        return response
    except Exception as e:
        print(f"Error: {e}")
        print()


def chat_completion_example():
    """
    Official example: Chat completion with system context
    Official Hugging Face method for chat-based models
    """
    print("=" * 60)
    print("EXAMPLE 3: Chat Completion (Official Way)")
    print("=" * 60)
    
    try:
        # Official InferenceClient chat_completion method
        response = client.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant specializing in exam preparation."
                },
                {
                    "role": "user",
                    "content": "What are the key concepts I should know about machine learning?"
                }
            ],
            model="mistralai/Mistral-7B-Instruct-v0.2",
            max_tokens=150,
            temperature=0.7,
        )
        
        # Response is a ChatCompletionOutput object
        answer = response.choices[0].message.content
        print(f"User: What are the key concepts I should know about machine learning?")
        print(f"Assistant: {answer}")
        print()
        return answer
    except Exception as e:
        print(f"Error: {e}")
        print()


def test_with_list_models():
    """
    List available models (requires inferencing capability)
    """
    print("=" * 60)
    print("EXAMPLE 4: Testing API Connection")
    print("=" * 60)
    
    try:
        # Simple check - can we make any inference request?
        response = client.text_generation(
            prompt="Hi",
            model="gpt2",
            max_new_tokens=10,
        )
        print(f"✓ API Connection: WORKING")
        print(f"✓ Token: VALID")
        print(f"✓ Response: {response}")
        print()
        return True
    except Exception as e:
        print(f"✗ API Error: {e}")
        print()
        return False


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " HUGGING FACE OFFICIAL InferenceClient - WORKING EXAMPLES ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # Run examples
    test_with_list_models()
    text_generation_example()
    text_generation_with_gemma()
    chat_completion_example()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)
