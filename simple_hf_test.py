#!/usr/bin/env python3
"""
Simple inline test - no dependencies on FastAPI
"""
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HF_TOKEN")

print("\n" + "="*70)
print("HF API DIRECT TEST")
print("="*70 + "\n")

if not token:
    print("ERROR: No HF_TOKEN found!")
    exit(1)

print(f"Token: {token[:30]}...")

client = InferenceClient(token=token)

# Test 1
print("\n[TEST 1] Simple text generation")
try:
    response = client.text_generation(
        prompt="The capital of France is",
        max_new_tokens=20
    )
    print(f"✅ SUCCESS: {response}")
except Exception as e:
    print(f"❌ FAILED: {e}")

# Test 2
print("\n[TEST 2] Chat completion")
try:
    response = client.chat_completion(
        messages=[{"role": "user", "content": "What is 2+2?"}],
        model="mistralai/Mistral-7B-Instruct-v0.2"
    )
    print(f"✅ SUCCESS: {response}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n" + "="*70)
