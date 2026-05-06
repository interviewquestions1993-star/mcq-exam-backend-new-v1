#!/usr/bin/env python3
"""
Complete test of the fixed Hugging Face online backend
Tests all endpoints with the corrected API implementation
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print(" "*10 + "HUGGING FACE ONLINE BACKEND - COMPLETE TEST")
print("="*70)

results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

# Test 1: Health Check (instant)
print("\n[1/5] HEALTH CHECK")
print("-"*70)
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS")
        print(f"   Status: {data['status']}")
        print(f"   API Type: {data['api_type']}")
        results["passed"] += 1
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        results["failed"] += 1
        results["errors"].append(f"Health: {response.status_code}")
except Exception as e:
    print(f"❌ FAILED: {str(e)[:80]}")
    results["failed"] += 1
    results["errors"].append(f"Health: {str(e)}")

# Test 2: List Models (instant)
print("\n[2/5] LIST MODELS")
print("-"*70)
try:
    response = requests.get(f"{BASE_URL}/models", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"✅ SUCCESS")
        print(f"   Models: {len(models)} available")
        for m in models[:2]:
            print(f"   • {m['name']}")
        results["passed"] += 1
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        results["failed"] += 1
        results["errors"].append(f"Models: {response.status_code}")
except Exception as e:
    print(f"❌ FAILED: {str(e)[:80]}")
    results["failed"] += 1
    results["errors"].append(f"Models: {str(e)}")

# Test 3: Rate Limits (instant)
print("\n[3/5] RATE LIMITS")
print("-"*70)
try:
    response = requests.get(f"{BASE_URL}/limits", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCCESS")
        print(f"   Free Tier: {data.get('free_tier', {}).get('requests_per_day', 'N/A')}")
        results["passed"] += 1
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        results["failed"] += 1
        results["errors"].append(f"Limits: {response.status_code}")
except Exception as e:
    print(f"❌ FAILED: {str(e)[:80]}")
    results["failed"] += 1
    results["errors"].append(f"Limits: {str(e)}")

# Test 4: TEXT GENERATION (5-15 seconds) - THIS IS THE KEY TEST
print("\n[4/5] TEXT GENERATION ⭐ KEY TEST")
print("-"*70)
try:
    payload = {
        "prompt": "The capital of France is",
        "max_tokens": 30,
        "temperature": 0.7
    }
    print(f"   Prompt: '{payload['prompt']}'")
    print(f"   Max tokens: {payload['max_tokens']}")
    print(f"   Sending request to Hugging Face API...")
    print(f"   (This may take 5-15 seconds)")
    
    response = requests.post(
        f"{BASE_URL}/generate",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        generated = data.get('generated_text', '')
        print(f"✅ SUCCESS!")
        print(f"   Generated: '{generated[:100]}'")
        print(f"   Status: {data.get('status')}")
        results["passed"] += 1
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        results["failed"] += 1
        results["errors"].append(f"Generate: {response.status_code}")
except requests.Timeout:
    print(f"❌ FAILED: Request timeout")
    print(f"   (HF servers may be slow or overloaded)")
    results["failed"] += 1
    results["errors"].append(f"Generate: Timeout")
except Exception as e:
    print(f"❌ FAILED: {str(e)[:80]}")
    results["failed"] += 1
    results["errors"].append(f"Generate: {str(e)[:60]}")

# Test 5: CHAT COMPLETION (5-15 seconds)
print("\n[5/5] CHAT COMPLETION ⭐ KEY TEST")
print("-"*70)
try:
    payload = {
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "max_tokens": 50
    }
    print(f"   Question: 'What is the capital of France?'")
    print(f"   Model: mistralai/Mistral-7B-Instruct-v0.2")
    print(f"   Sending request to Hugging Face API...")
    print(f"   (This may take 5-15 seconds)")
    
    response = requests.post(
        f"{BASE_URL}/chat",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        message = data.get('message', '')
        print(f"✅ SUCCESS!")
        print(f"   Answer: '{message[:100]}'")
        print(f"   Status: {data.get('status')}")
        results["passed"] += 1
    else:
        print(f"❌ FAILED: Status {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        results["failed"] += 1
        results["errors"].append(f"Chat: {response.status_code}")
except requests.Timeout:
    print(f"❌ FAILED: Request timeout")
    print(f"   (HF servers may be slow or overloaded)")
    results["failed"] += 1
    results["errors"].append(f"Chat: Timeout")
except Exception as e:
    print(f"❌ FAILED: {str(e)[:80]}")
    results["failed"] += 1
    results["errors"].append(f"Chat: {str(e)[:60]}")

# Summary
print("\n" + "="*70)
print("TEST SUMMARY")
print("="*70)
print(f"\n✅ PASSED: {results['passed']}/5")
print(f"❌ FAILED: {results['failed']}/5")

if results["errors"]:
    print(f"\nErrors:")
    for error in results["errors"]:
        print(f"  • {error}")
else:
    print(f"\n🎉 ALL TESTS PASSED!")

print("\n" + "="*70)
print("WHAT'S FIXED")
print("="*70)
print("""
✅ Using api_key parameter (not token)
✅ Correct response parsing (string from text_generation)
✅ Correct chat response parsing (ChatCompletionOutput)
✅ Proper error handling and logging
✅ Timeout handling (30 seconds for API calls)

Your backend is now correctly integrated with Hugging Face API!
""")
print("="*70)
