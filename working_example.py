#!/usr/bin/env python
"""
✅ WORKING ONLINE EXAMPLE - Hugging Face Inference
This demonstrates the official working approach using the REST API
"""

import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
hf_model = os.getenv("HF_MODEL", "distilgpt2")

print("=" * 60)
print("WORKING HUGGING FACE ONLINE INFERENCE EXAMPLE")
print("=" * 60)

# Verify token
if not hf_token:
    print("❌ ERROR: HF_TOKEN not found in .env")
    exit(1)

print(f"✅ Token loaded: {hf_token[:20]}...")
print(f"✅ Model: {hf_model}")

# Build API endpoint - try different format
api_url = f"https://api-inference.huggingface.co/models/{hf_model}"
headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json"
}

# Build payload - correct format for text generation
payload = {
    "inputs": "Artificial intelligence is"
}

print(f"\n📡 Making request to: {api_url}")
print(f"📝 Payload: {json.dumps(payload, indent=2)}")

# Make the request
try:
    print("\n⏳ Waiting for response...")
    response = requests.post(
        api_url,
        json=payload,
        headers=headers,
        timeout=30
    )
    
    print(f"\n📥 Response Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Generated text:")
        print("=" * 60)
        
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get('generated_text', 'No text generated')
            print(f"\n{generated_text}\n")
        else:
            print(f"\n{result}\n")
            
    elif response.status_code == 503:
        print("⏳ Model is loading. Please try again in a moment.")
        print(f"Response: {response.text}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout: Request took too long (>30s)")
    
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    print("Check if you have internet connection")
    
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("EXAMPLE COMPLETE")
print("=" * 60)
