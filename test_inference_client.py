#!/usr/bin/env python
"""
Test using the official Hugging Face InferenceClient
This is the recommended and most reliable way
"""

import os
from dotenv import load_dotenv
import time

print("\n" + "=" * 70)
print("TESTING WITH OFFICIAL HUGGING FACE INFERENCECLIENT")
print("=" * 70)

# Load environment
load_dotenv()
token = os.getenv("HF_TOKEN")
model = os.getenv("HF_MODEL", "gpt2")

if not token:
    print("❌ No token found")
    exit(1)

print(f"\n✅ Token: {token[:20]}...")
print(f"✅ Model: {model}")

# Test 1: Import and create client
print("\n1️⃣ Creating InferenceClient...")
try:
    from huggingface_hub import InferenceClient
    client = InferenceClient(api_key=token)
    print("✅ Client created successfully")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test 2: Generate text
print("\n2️⃣ Making Text Generation Request")
print("-" * 70)

prompt = "The future of artificial intelligence is"
print(f"Prompt: {prompt}")
print("\n⏳ Waiting for response (this may take 30-60 seconds)...")

start_time = time.time()
try:
    response = client.text_generation(
        prompt=prompt,
        max_new_tokens=50,
        model=model
    )
    elapsed = time.time() - start_time
    
    print(f"\n✅✅✅ SUCCESS! RESPONSE RECEIVED ✅✅✅")
    print(f"Response time: {elapsed:.1f} seconds")
    print(f"\nGenerated Text:\n{response}")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}")
    print(f"Details: {str(e)[:200]}")

print("\n" + "=" * 70)
