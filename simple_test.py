"""
Simple test script for the backend
"""
import sys
import time
import subprocess
import requests
import json

def wait_for_backend(timeout=60):
    """Wait for backend to be ready"""
    print("Waiting for backend...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get("http://localhost:8000/", timeout=2)
            if r.status_code == 200:
                print("✓ Backend is ready!")
                return True
        except Exception as e:
            elapsed = int(time.time() - start)
            print(f"  ({elapsed}s) Waiting...", end="\r")
        time.sleep(1)
    print("\n✗ Backend did not start within timeout")
    return False

def test_generate():
    """Test generate endpoint"""
    print("\n" + "="*60)
    print("Testing Generate Endpoint")
    print("="*60)
    
    prompt = "Which is the largest country?"
    payload = {
        "prompt": prompt,
        "max_new_tokens": 50,
        "temperature": 0.7
    }
    
    print(f"Prompt: {prompt}\n")
    print("Sending request to http://localhost:8000/generate")
    print("This may take a minute on first request...\n")
    
    try:
        response = requests.post(
            "http://localhost:8000/generate",
            json=payload,
            timeout=300  # 5 minute timeout for first request
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓✓✓ SUCCESS! ✓✓✓\n")
            print(f"Generated Text:\n{result['generated_text']}")
            print(f"\n✓ Status: {result['status']}")
            return True
        else:
            print(f"\n✗ ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n✗ Exception: {e}")
        return False

if __name__ == "__main__":
    print("#"*60)
    print("# TESTING HUGGING FACE LOCAL BACKEND")
    print("#"*60)
    
    if not wait_for_backend(timeout=120):
        print("\nMake sure backend is running: python main_local.py")
        sys.exit(1)
    
    success = test_generate()
    sys.exit(0 if success else 1)
