#!/usr/bin/env python
"""Test Hugging Face Online Inference with proper token loading"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
print("[1] Loading environment variables from .env...")
load_dotenv()

# Get token
hf_token = os.getenv("HF_TOKEN")
hf_model = os.getenv("HF_MODEL", "distilgpt2")

print(f"[2] Token found: {bool(hf_token)}")
print(f"[3] Token (first 20 chars): {hf_token[:20] if hf_token else 'NONE'}...")
print(f"[4] Model: {hf_model}")

if not hf_token:
    print("\n❌ ERROR: HF_TOKEN not found!")
    print("Make sure .env file exists with HF_TOKEN=your_token")
    exit(1)

# Create InferenceClient
print("\n[5] Creating InferenceClient...")
client = InferenceClient(api_key=hf_token)

# Test simple text generation
print("[6] Sending request to Hugging Face API...")
prompt = "Artificial intelligence is"

try:
    result = client.text_generation(
        prompt=prompt,
        max_new_tokens=50,
        temperature=0.7,
    )
    
    print("\n✅ SUCCESS! Response received:")
    print("-" * 50)
    print(f"Prompt: {prompt}")
    print(f"Generated: {result}")
    print("-" * 50)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Details: {str(e)}")
    import traceback
    traceback.print_exc()
