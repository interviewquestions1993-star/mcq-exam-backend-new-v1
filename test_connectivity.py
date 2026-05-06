#!/usr/bin/env python
"""Test basic connectivity"""

import socket
import sys

print("Testing basic network connectivity...")

try:
    print("1. Testing DNS resolution for api-inference.huggingface.co...")
    ip = socket.gethostbyname("api-inference.huggingface.co")
    print(f"   ✅ Resolved to: {ip}")
except socket.gaierror as e:
    print(f"   ❌ DNS error: {e}")
    sys.exit(1)

try:
    print("2. Testing socket connection to api-inference.huggingface.co:443...")
    sock = socket.create_connection(("api-inference.huggingface.co", 443), timeout=5)
    sock.close()
    print(f"   ✅ Connected successfully")
except socket.timeout:
    print(f"   ❌ Connection timeout")
    sys.exit(1)
except ConnectionRefusedError as e:
    print(f"   ❌ Connection refused: {e}")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print("\n✅ Network connectivity OK")
print("\nNow testing with requests library...")

import requests
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HF_TOKEN")

if not token:
    print("❌ No token")
    sys.exit(1)

print("3. Testing with requests.get()...")
try:
    response = requests.get(
        "https://api-inference.huggingface.co/models/distilgpt2",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response (first 200 chars): {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")
