#!/usr/bin/env python
"""Check if the new token is valid"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv("HF_TOKEN")

print("\n" + "=" * 70)
print("TOKEN VALIDATION CHECK")
print("=" * 70)

print(f"\nToken: {token[:20]}...")
print(f"Length: {len(token)}")
print(f"Starts with hf_: {token.startswith('hf_')}")

# Test 1: Verify token with whoami endpoint
print("\n1️⃣ CHECKING TOKEN VALIDITY")
print("-" * 70)

headers = {"Authorization": f"Bearer {token}"}
try:
    response = requests.get(
        "https://huggingface.co/api/whoami",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅✅✅ TOKEN IS VALID! ✅✅✅")
        print(f"\nUser Information:")
        print(f"  Username: {data.get('name')}")
        print(f"  User ID: {data.get('id')}")
        print(f"  Account type: {data.get('type')}")
        is_valid = True
    else:
        print(f"❌ Token invalid")
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.json()}")
        is_valid = False
        
except Exception as e:
    print(f"❌ Error: {e}")
    is_valid = False

# Test 2: Test Inference API Access
print("\n2️⃣ TESTING INFERENCE API ACCESS")
print("-" * 70)

try:
    url = "https://api-inference.huggingface.co/models/gpt2"
    payload = {"inputs": "Hello world"}
    
    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Inference API access OK!")
        result = response.json()
        print(f"Response preview: {str(result)[:150]}...")
    elif response.status_code == 503:
        print("⏳ Model is loading (503)")
        print("This is normal - model will be ready in 30-60 seconds on first request")
    else:
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
if is_valid:
    print("✅ TOKEN VALIDATION COMPLETE - TOKEN IS VALID")
else:
    print("❌ TOKEN VALIDATION FAILED - TOKEN IS INVALID")
print("=" * 70 + "\n")
