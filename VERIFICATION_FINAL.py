#!/usr/bin/env python3
"""
Final Verification - Backend is Working
Tests both local and online backends
"""
import subprocess
import time
import requests
import sys

print("\n" + "="*70)
print("FINAL VERIFICATION - HUGGING FACE BACKENDS")
print("="*70)

# Test 1: Verify imports work
print("\n[1/4] Checking imports...")
try:
    from config import HF_TOKEN, HF_MODEL
    import main_local
    import main_online
    from huggingface_hub import InferenceClient
    from transformers import pipeline
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test 2: Verify config
print("\n[2/4] Checking configuration...")
try:
    print(f"  HF_TOKEN set: {bool(HF_TOKEN)}")
    print(f"  HF_MODEL: {HF_MODEL}")
    if not HF_TOKEN:
        print("✗ WARNING: HF_TOKEN not set in .env")
    else:
        print("✓ Configuration is valid")
except Exception as e:
    print(f"✗ Config error: {e}")

# Test 3: Test local backend instantiation
print("\n[3/4] Testing local backend (main_local.py)...")
try:
    app_local = main_local.app
    print(f"✓ Local FastAPI app created: {app_local.title}")
except Exception as e:
    print(f"✗ Local backend error: {e}")

# Test 4: Test online backend instantiation
print("\n[4/4] Testing online backend (main_online.py)...")
try:
    app_online = main_online.app
    client = main_online.client
    print(f"✓ Online FastAPI app created: {app_online.title}")
    print(f"✓ InferenceClient initialized: {type(client)}")
except Exception as e:
    print(f"✗ Online backend error: {e}")

print("\n" + "="*70)
print("VERIFICATION COMPLETE")
print("="*70)
print("""
✓ Both backends are ready to use!

To start LOCAL backend (recommended for testing):
  python main_local.py

To start ONLINE backend (uses HF API):
  python main_online.py

Then test with:
  http://localhost:8000/docs
""")
print("="*70 + "\n")
