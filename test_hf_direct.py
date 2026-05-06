#!/usr/bin/env python3
"""
Direct Hugging Face API Test
Tests the token and API connectivity without the FastAPI layer
"""
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")

print("\n" + "="*70)
print("DIRECT HUGGING FACE API TEST")
print("="*70)

print(f"\nToken found: {bool(token)}")
if token:
    print(f"Token (first 30 chars): {token[:30]}...")
else:
    print("❌ NO TOKEN FOUND IN .env!")

print("\n" + "-"*70)

if not token:
    print("❌ CANNOT PROCEED - NO TOKEN")
else:
    try:
        print("\n[1] Creating InferenceClient...")
        client = InferenceClient(token=token)
        print("✅ Client created successfully\n")
        
        # Test 1: Text generation with gpt2
        print("[2] Testing text_generation (gpt2)...")
        print("   Prompt: 'What is the largest planet in our solar system?'")
        print("   Sending request...")
        
        result = client.text_generation(
            prompt="What is the largest planet in our solar system?",
            model="gpt2",
            max_new_tokens=50
        )
        
        print(f"✅ SUCCESS!")
        print(f"   Response type: {type(result)}")
        print(f"   Response: {str(result)[:120]}")
        
    except Exception as e:
        print(f"❌ FAILED!")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        print("\nFull traceback:")
        import traceback
        traceback.print_exc()

print("\n" + "="*70)
print("END OF TEST")
print("="*70)
