#!/usr/bin/env python
"""
✅ OFFICIAL WORKING SOLUTION - Using HuggingFace InferenceClient
This is the recommended approach from Hugging Face
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("HUGGING FACE INFERENCE CLIENT - OFFICIAL APPROACH")
print("=" * 60)

# Load environment
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
hf_model = os.getenv("HF_MODEL", "gpt2")

if not hf_token:
    print("❌ ERROR: HF_TOKEN not found in .env")
    exit(1)

print(f"✅ Token loaded")
print(f"✅ Model: {hf_model}")

# Import and create client
try:
    from huggingface_hub import InferenceClient
    print("✅ InferenceClient imported")
    
    client = InferenceClient(api_key=hf_token)
    print("✅ Client created")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Make inference request
print(f"\n📡 Making inference request...")
prompt = "The future of artificial intelligence is"

try:
    print(f"Prompt: {prompt}")
    print("⏳ Waiting for response...")
    
    response = client.text_generation(
        prompt=prompt,
        max_new_tokens=50,
    )
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Generated text:")
    print("=" * 60)
    print(f"\n{response}\n")
    
except Exception as e:
    print(f"\n❌ Error ({type(e).__name__}): {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
