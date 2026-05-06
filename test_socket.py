#!/usr/bin/env python
import sys
print("Test 1: Importing socket...", flush=True)
import socket
print("✅ Done", flush=True)

print("Test 2: gethostbyname...", flush=True)
try:
    ip = socket.gethostbyname("api-inference.huggingface.co")
    print(f"✅ IP: {ip}", flush=True)
except Exception as e:
    print(f"❌ Error: {e}", flush=True)
    sys.exit(1)
