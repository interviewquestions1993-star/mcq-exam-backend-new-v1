"""
Test script for Hugging Face Online Backend
"""
import sys
import time
import requests
import json

BASE_URL = "http://localhost:8000"

def wait_for_backend(timeout=30):
    """Wait for backend to be ready"""
    print("Waiting for backend...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE_URL}/", timeout=2)
            if r.status_code == 200:
                print("✓ Backend is ready!\n")
                return True
        except:
            pass
        time.sleep(1)
    print("✗ Backend did not start within timeout")
    return False

def test_health():
    """Test health check"""
    print("="*60)
    print("Test 1: Health Check")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/")
        print(f"Status: {r.status_code}")
        result = r.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False

def test_models():
    """Test models endpoint"""
    print("="*60)
    print("Test 2: Available Models")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/models")
        print(f"Status: {r.status_code}")
        result = r.json()
        if result['status'] == 'success':
            print(f"Available models: {len(result['models'])}")
            for model in result['models'][:2]:  # Show first 2
                print(f"  - {model['name']}: {model['description']}")
            print("✓ PASSED\n")
            return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False

def test_limits():
    """Test rate limits info"""
    print("="*60)
    print("Test 3: Rate Limits Info")
    print("="*60)
    try:
        r = requests.get(f"{BASE_URL}/limits")
        print(f"Status: {r.status_code}")
        result = r.json()
        print(f"Free tier requests/day: {result['free_tier']['requests_per_day']}")
        print("✓ PASSED\n")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False

def test_generate():
    """Test text generation"""
    print("="*60)
    print("Test 4: Text Generation")
    print("="*60)
    prompt = "Which is the largest country?"
    payload = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    print(f"Prompt: {prompt}\n")
    print("Sending request (this may take a few seconds)...\n")
    
    try:
        r = requests.post(
            f"{BASE_URL}/generate",
            json=payload,
            timeout=30
        )
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            result = r.json()
            print(f"\n✓ Generated Text:\n{result['generated_text']}\n")
            print("✓ PASSED\n")
            return True
        else:
            print(f"\n✗ Error: {r.text}\n")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False

def test_chat():
    """Test chat completion"""
    print("="*60)
    print("Test 5: Chat Completion (Mistral)")
    print("="*60)
    payload = {
        "messages": [
            {"role": "user", "content": "What is the capital of France?"}
        ],
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "max_tokens": 50
    }
    
    print("Sending chat request (this may take a few seconds)...\n")
    
    try:
        r = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200:
            result = r.json()
            print(f"\n✓ Response:\n{result['message']}\n")
            print("✓ PASSED\n")
            return True
        else:
            print(f"\n✗ Error: {r.text}\n")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}\n")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# HUGGING FACE ONLINE BACKEND - TEST SUITE")
    print("#"*60 + "\n")
    
    results = {
        "Health Check": test_health(),
        "Models": test_models(),
        "Rate Limits": test_limits(),
        "Text Generation": test_generate(),
        "Chat Completion": test_chat()
    }
    
    print("="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    print("="*60 + "\n")
    
    return total_passed == total_tests

if __name__ == "__main__":
    print("Make sure the backend is running!")
    print("Start it with: python main_online.py\n")
    
    if not wait_for_backend():
        print("\n✗ Backend is not running!")
        sys.exit(1)
    
    success = run_all_tests()
    
    if success:
        print("🎉 All tests passed! Your backend is working!\n")
        sys.exit(0)
    else:
        print("⚠️ Some tests failed. Check the errors above.\n")
        sys.exit(1)
