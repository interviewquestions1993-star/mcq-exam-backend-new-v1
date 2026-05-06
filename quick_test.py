#!/usr/bin/env python3
"""Quick test of the online backend"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🔍 HUGGING FACE ONLINE BACKEND - LIVE TEST")
print("=" * 60)
print()

# Test 1: Health Check
print("✓ Test 1: Health Check")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 2: List Models
print("✓ Test 2: Available Models")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/models", timeout=5)
    print(f"Status: {response.status_code}")
    data = response.json()
    for model in data.get('models', []):
        print(f"  - {model['name']}: {model['description']}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 3: Rate Limits
print("✓ Test 3: Rate Limits")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/limits", timeout=5)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 4: Generate Text
print("✓ Test 4: Text Generation")
print("-" * 60)
try:
    payload = {
        "prompt": "What is the largest planet in our solar system?",
        "max_tokens": 100,
        "temperature": 0.7
    }
    print(f"Prompt: {payload['prompt']}")
    print("Sending request...")
    response = requests.post(f"{BASE_URL}/generate", json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Generated: {result['generated_text']}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 5: Chat
print("✓ Test 5: Chat Completion")
print("-" * 60)
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
    print("Sending request...")
    response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Assistant: {result['message']}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

print("=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print()
print("📍 Backend running at: http://localhost:8000")
print("📚 Swagger UI at: http://localhost:8000/docs")
print("🔗 ReDoc at: http://localhost:8000/redoc")
