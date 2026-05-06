#!/usr/bin/env python
"""Test Hugging Face REST API directly"""

import os
import requests
from dotenv import load_dotenv

# Load token
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
hf_model = os.getenv("HF_MODEL", "distilgpt2")

if not hf_token:
    print("❌ ERROR: HF_TOKEN not found")
    exit(1)

print(f"✅ Token loaded")
print(f"Model: {hf_model}")

# API URL
api_url = f"https://api-inference.huggingface.co/models/{hf_model}"
headers = {"Authorization": f"Bearer {hf_token}"}

# Test payload
payload = {
    "inputs": "Artificial intelligence is",
    "parameters": {
        "max_new_tokens": 50,
        "temperature": 0.7
    }
}

print(f"\nAPI URL: {api_url}")
print("Sending request...")

try:
    response = requests.post(api_url, json=payload, headers=headers, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Result: {result}")
    else:
        print(f"\n❌ Error {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ Request timeout (30s)")
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
