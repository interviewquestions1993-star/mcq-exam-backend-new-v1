#!/usr/bin/env python3
"""Test all backend endpoints"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"
print("\n" + "="*70)
print(" "*20 + "BACKEND TEST SUITE")
print("="*70)

tests_passed = 0
tests_failed = 0

# Test 1: Health Check
print("\n[1/5] Testing Health Check (GET /)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/", timeout=10)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    if response.status_code == 200:
        print("✅ PASSED")
        tests_passed += 1
    else:
        print("❌ FAILED")
        tests_failed += 1
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests_failed += 1

# Test 2: Models List
print("\n[2/5] Testing Models List (GET /models)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/models", timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Models available: {len(data.get('models', []))}")
        for model in data.get('models', [])[:2]:
            print(f"  - {model.get('name')}: {model.get('description', '')[:50]}")
        print("✅ PASSED")
        tests_passed += 1
    else:
        print(f"Response: {response.text[:200]}")
        print("❌ FAILED")
        tests_failed += 1
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests_failed += 1

# Test 3: Rate Limits
print("\n[3/5] Testing Rate Limits (GET /limits)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/limits", timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Free Tier: {data.get('free_tier', 'N/A')}")
        print("✅ PASSED")
        tests_passed += 1
    else:
        print(f"Response: {response.text[:200]}")
        print("❌ FAILED")
        tests_failed += 1
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests_failed += 1

# Test 4: Text Generation
print("\n[4/5] Testing Text Generation (POST /generate)")
print("-" * 70)
try:
    payload = {
        "prompt": "The largest planet in our solar system is",
        "max_tokens": 50,
        "temperature": 0.7
    }
    print(f"Prompt: {payload['prompt']}")
    print("Sending request (may take 5-15 seconds)...")
    response = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Generated: {data.get('generated_text', '')[:100]}")
        print("✅ PASSED")
        tests_passed += 1
    else:
        print(f"Response: {response.text[:200]}")
        print("❌ FAILED")
        tests_failed += 1
except requests.Timeout:
    print("❌ FAILED: Request timeout (backend may be slow)")
    tests_failed += 1
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests_failed += 1

# Test 5: Chat
print("\n[5/5] Testing Chat (POST /chat)")
print("-" * 70)
try:
    payload = {
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "max_tokens": 100
    }
    print(f"User: {payload['messages'][0]['content']}")
    print(f"Model: {payload['model']}")
    print("Sending request (may take 5-15 seconds)...")
    response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Assistant: {data.get('message', '')[:100]}")
        print("✅ PASSED")
        tests_passed += 1
    else:
        print(f"Response: {response.text[:200]}")
        print("❌ FAILED")
        tests_failed += 1
except requests.Timeout:
    print("❌ FAILED: Request timeout (backend may be slow)")
    tests_failed += 1
except Exception as e:
    print(f"❌ FAILED: {e}")
    tests_failed += 1

# Summary
print("\n" + "="*70)
print(f"RESULTS: {tests_passed} passed, {tests_failed} failed")
print("="*70)

if tests_failed == 0:
    print("✅ ALL TESTS PASSED!")
    sys.exit(0)
else:
    print("❌ Some tests failed")
    sys.exit(1)
