#!/usr/bin/env python
"""Debug: Check token and try different approaches"""

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")

print("Token info:")
print(f"  Present: {bool(token)}")
print(f"  Length: {len(token) if token else 0}")
print(f"  Starts with hf_: {token.startswith('hf_') if token else False}")

# Try with requests - check raw API response
import requests

print("\n" + "=" * 60)
print("Direct API Test")
print("=" * 60)

headers = {"Authorization": f"Bearer {token}"}

# Try to access the models endpoint
print("\n1. Checking if token is valid:")
try:
    r = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=10)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   ✅ Token is VALID")
        print(f"   User: {data.get('name')}")
    else:
        print(f"   ❌ Token issue: {r.status_code}")
        print(f"   Response: {r.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Try to list available models
print("\n2. Checking available models in inference API:")
try:
    r = requests.get("https://api-inference.huggingface.co/", headers=headers, timeout=10)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Try to use the correct API format - check gpt2 model directly
print("\n3. Testing gpt2 model with inference API:")
models_to_try = [
    "gpt2",
    "gpt2-medium",
    "gpt2-large",
    "distilgpt2",
    "EleutherAI/gpt-neo-125M",
    "meta-llama/Llama-2-7b-hf",
]

for model_id in models_to_try:
    try:
        url = f"https://api-inference.huggingface.co/models/{model_id}"
        payload = {"inputs": "Hello"}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   {model_id}: {r.status_code}")
        if r.status_code == 200:
            print(f"      ✅ WORKS! Response: {str(r.json())[:100]}")
            break
    except Exception as e:
        print(f"   {model_id}: Error - {type(e).__name__}")
