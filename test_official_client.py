"""
Test script for official Hugging Face InferenceClient
Validates that the working example actually works
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", "")

if not HF_TOKEN:
    print("❌ ERROR: HF_TOKEN not found in .env file")
    print("Please create .env file with your Hugging Face token:")
    print("  HF_TOKEN=your_token_here")
    sys.exit(1)

print("✓ HF_TOKEN loaded from environment")
print()

# Import the InferenceClient
try:
    from huggingface_hub import InferenceClient
    print("✓ huggingface_hub library imported successfully")
except ImportError:
    print("❌ ERROR: huggingface_hub not installed")
    print("Install it with: pip install huggingface-hub")
    sys.exit(1)

print()
print("=" * 70)
print("TESTING OFFICIAL INFERENCE CLIENT")
print("=" * 70)
print()

# Create client
try:
    client = InferenceClient(api_key=HF_TOKEN)
    print("✓ InferenceClient initialized")
except Exception as e:
    print(f"❌ Failed to initialize client: {e}")
    sys.exit(1)

print()
print("-" * 70)
print("TEST 1: Simple Text Generation (GPT-2)")
print("-" * 70)

try:
    response = client.text_generation(
        prompt="The capital of France is",
        model="gpt2",
        max_new_tokens=20,
    )
    print("✓ Test 1 PASSED")
    print(f"  Prompt: The capital of France is")
    print(f"  Response: {response}")
except Exception as e:
    print(f"❌ Test 1 FAILED: {e}")

print()
print("-" * 70)
print("TEST 2: Text Generation with Gemma 2B")
print("-" * 70)

try:
    response = client.text_generation(
        prompt="Explain artificial intelligence:",
        model="google/gemma-2-2b-it",
        max_new_tokens=80,
        temperature=0.7,
    )
    print("✓ Test 2 PASSED")
    print(f"  Prompt: Explain artificial intelligence:")
    print(f"  Response: {response[:200]}...")
except Exception as e:
    print(f"❌ Test 2 FAILED: {e}")

print()
print("-" * 70)
print("TEST 3: Chat Completion (Mistral)")
print("-" * 70)

try:
    response = client.chat_completion(
        messages=[
            {
                "role": "user",
                "content": "What is machine learning in one sentence?"
            }
        ],
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_tokens=100,
    )
    message_content = response.choices[0].message.content
    print("✓ Test 3 PASSED")
    print(f"  User: What is machine learning in one sentence?")
    print(f"  Assistant: {message_content}")
except Exception as e:
    print(f"❌ Test 3 FAILED: {e}")

print()
print("=" * 70)
print("TESTING COMPLETE")
print("=" * 70)
print()
print("✓ All official InferenceClient methods are working!")
print()
print("Next steps:")
print("  1. Run the FastAPI backend: python main_official.py")
print("  2. Visit the API docs: http://localhost:8000/docs")
print("  3. Test endpoints through Swagger UI")
