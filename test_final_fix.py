#!/usr/bin/env python3
"""Test text generation with the FIXED endpoint (no model specified)"""
import requests

print("\n" + "="*70)
print("TESTING TEXT GENERATION - FIXED VERSION")
print("="*70)

BASE_URL = "http://localhost:8000"

# Test 1: Health first
print("\n[Test 1] Health check...")
try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    if r.status_code == 200:
        print(f"✅ OK")
    else:
        print(f"❌ Failed: {r.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: The exact failing prompt
print("\n[Test 2] Text Generation: 'Which is the largest country?'")
print("   (Using API default model - NO explicit model specified)")
try:
    payload = {
        "prompt": "Which is the largest country?",
        "max_tokens": 100
    }
    print(f"   Sending...")
    r = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"   Generated: {data['generated_text'][:120]}")
    else:
        print(f"❌ Failed: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
except requests.Timeout:
    print(f"❌ Timeout (HF API slow)")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Another test
print("\n[Test 3] Text Generation: 'What is the capital of France?'")
try:
    payload = {
        "prompt": "What is the capital of France?",
        "max_tokens": 50
    }
    print(f"   Sending...")
    r = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"   Generated: {data['generated_text'][:100]}")
    else:
        print(f"❌ Failed: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
except requests.Timeout:
    print(f"❌ Timeout")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("If both tests above show ✅, then the fix works!")
print("="*70)
