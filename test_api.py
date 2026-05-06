"""
Test script for the Hugging Face Inference Backend
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_text_generation():
    """Test text generation endpoint"""
    print("\n" + "="*60)
    print("Testing Text Generation Endpoint")
    print("="*60)
    
    payload = {
        "prompt": "What is machine learning?",
        "max_new_tokens": 100,
        "temperature": 0.7,
        "top_p": 0.9
    }
    
    print(f"Prompt: {payload['prompt']}")
    print("Sending request...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/generate",
            json=payload,
            timeout=120
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Generated Text:\n{result['generated_text']}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_summarization():
    """Test summarization endpoint"""
    print("\n" + "="*60)
    print("Testing Summarization Endpoint")
    print("="*60)
    
    text = """
    Hugging Face is a company that develops tools for building machine learning applications.
    The company is most notable for its Transformers library, which provides thousands of
    pretrained models. Founded in 2016, Hugging Face has grown into one of the most important
    platforms in the AI ecosystem, hosting over 800,000 models.
    """
    
    payload = {
        "text": text.strip(),
        "max_length": 50,
        "min_length": 20
    }
    
    print(f"Text to summarize: {text.strip()[:100]}...")
    print("Sending request...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json=payload,
            timeout=120
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Summary:\n{result['summary']}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def test_chat():
    """Test chat endpoint"""
    print("\n" + "="*60)
    print("Testing Chat Endpoint")
    print("="*60)
    
    payload = {
        "prompt": "Explain neural networks in simple terms.",
        "max_new_tokens": 150,
        "temperature": 0.7
    }
    
    print(f"Prompt: {payload['prompt']}")
    print("Sending request...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json=payload,
            timeout=120
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Response:\n{result['generated_text']}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# HUGGING FACE INFERENCE BACKEND - TEST SUITE")
    print("#"*60)
    
    results = {
        "Health Check": test_health_check(),
        "Text Generation": test_text_generation(),
        "Summarization": test_summarization(),
        "Chat": test_chat()
    }
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    print("="*60)


if __name__ == "__main__":
    print("\nMake sure the backend is running on http://localhost:8000")
    print("Start it with: python main.py\n")
    
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
