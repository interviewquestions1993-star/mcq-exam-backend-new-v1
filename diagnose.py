#!/usr/bin/env python
"""Diagnostic: Check what's causing the hang"""

import socket
import sys

print("DIAGNOSTIC: Network Connectivity Check")
print("=" * 50)

# Test 1: Can we resolve the hostname?
print("\n1. DNS Resolution Test:")
try:
    ip = socket.gethostbyname("api-inference.huggingface.co")
    print(f"   ✅ Resolved api-inference.huggingface.co to {ip}")
except socket.gaierror as e:
    print(f"   ❌ DNS failed: {e}")
    sys.exit(1)

# Test 2: Can we connect to HTTPS port?
print("\n2. HTTPS Connection Test (port 443):")
try:
    sock = socket.create_connection(("api-inference.huggingface.co", 443), timeout=5)
    sock.close()
    print(f"   ✅ Connected to port 443")
except socket.timeout:
    print(f"   ❌ Connection timeout (socket)")
except ConnectionRefusedError as e:
    print(f"   ❌ Connection refused: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Try requests with very short timeout
print("\n3. HTTP Request Test (with timeout):")
import requests
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("HF_TOKEN")

if not token:
    print("   ❌ No token found")
    sys.exit(1)

headers = {"Authorization": f"Bearer {token}"}

try:
    print("   Making test request... (2 second timeout)")
    response = requests.head(
        "https://api-inference.huggingface.co/models/distilgpt2",
        headers=headers,
        timeout=2
    )
    print(f"   ✅ Got response: {response.status_code}")
except socket.timeout:
    print(f"   ⏳ Socket timeout (network issue)")
except requests.exceptions.Timeout:
    print(f"   ⏳ Request timeout (too slow)")
except requests.exceptions.ConnectionError as e:
    print(f"   ❌ Connection error: {e}")
except Exception as e:
    print(f"   ❌ Other error ({type(e).__name__}): {e}")

print("\n" + "=" * 50)
print("DIAGNOSIS COMPLETE")
print("\nPossible Issues:")
print("1. Firewall blocking HTTPS to HF servers")
print("2. Proxy configuration needed")
print("3. Network is very slow")
print("4. ISP/Network blocks HF API")
