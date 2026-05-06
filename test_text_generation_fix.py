#!/usr/bin/env python3
"""
Test the fixed text generation endpoint
"""
import requests
import json

print("\n" + "="*70)
print("TESTING FIXED TEXT GENERATION ENDPOINT")
print("="*70)

BASE_URL = "http://localhost:8000"

# Test 1: Health check first
print("\n[1] Testing health check...")
try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"✅ Health: {r.status_code}")
except Exception as e:
    print(f"❌ Health failed: {e}")
    exit(1)

# Test 2: Text generation with the exact error message's prompt
print("\n[2] Testing text generation with 'Which is the largest country?'...")
try:
    payload = {
        "prompt": "Which is the largest country?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    print(f"   Sending request...")
    r = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    
    print(f"   Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"   Prompt: {data['prompt']}")
        print(f"   Generated: {data['generated_text'][:100]}")
        print(f"   Model: {data['model']}")
    else:
        print(f"❌ FAILED")
        print(f"   Response: {r.text}")
        
except requests.Timeout:
    print(f"❌ Timeout")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Another text generation test
print("\n[3] Testing with 'What is AI?'...")
try:
    payload = {
        "prompt": "What is AI?",
        "max_tokens": 50,
        "temperature": 0.7
    }
    print(f"   Sending request...")
    r = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ SUCCESS!")
        print(f"   Generated: {data['generated_text'][:80]}")
    else:
        print(f"❌ FAILED: {r.status_code}")
        print(f"   Error: {r.text[:200]}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
