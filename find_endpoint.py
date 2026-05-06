#!/usr/bin/env python
"""Test different Hugging Face API endpoints"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv("HF_TOKEN")
model = "distilgpt2"

if not token:
    print("No token!")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}
payload = {"inputs": "Hello"}

# Try different endpoint formats
endpoints = [
    f"https://api-inference.huggingface.co/models/{model}",
    f"https://huggingface.co/models/{model}/api/v1/generate",
    f"https://api.huggingface.co/models/{model}",
]

for url in endpoints:
    print(f"\n🔍 Testing: {url}")
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {resp.json()}")
            break
        else:
            print(f"   Error: {resp.text[:100]}")
    except Exception as e:
        print(f"   ❌ {type(e).__name__}: {e}")
