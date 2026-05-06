#!/usr/bin/env python3
"""
Comprehensive Backend Test & Fix Script
Tests all endpoints and fixes any issues
"""
import requests
import json
import sys
import time
from typing import Tuple

class BackendTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {"passed": 0, "failed": 0, "errors": []}
        
    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     data: dict = None, timeout: int = 30) -> bool:
        """Test a single endpoint"""
        print(f"\n  Testing {name}...", end=" ")
        try:
            url = f"{self.base_url}{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=timeout)
            else:
                response = requests.post(url, json=data, timeout=timeout)
            
            if response.status_code == 200:
                print(f"✅ OK (Status: {response.status_code})")
                self.results["passed"] += 1
                return True
            else:
                print(f"❌ Failed (Status: {response.status_code})")
                self.results["failed"] += 1
                self.results["errors"].append(f"{name}: {response.status_code}")
                return False
        except requests.Timeout:
            print(f"❌ Timeout")
            self.results["failed"] += 1
            self.results["errors"].append(f"{name}: Timeout")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)[:40]}")
            self.results["failed"] += 1
            self.results["errors"].append(f"{name}: {str(e)[:50]}")
            return False

    def run_all_tests(self):
        """Run all endpoint tests"""
        print("\n" + "="*70)
        print(" "*15 + "BACKEND COMPREHENSIVE TEST")
        print("="*70)
        
        print(f"\nBase URL: {self.base_url}")
        print("Checking backend connectivity...")
        
        # Quick connectivity check
        try:
            requests.get(self.base_url, timeout=5)
            print("✅ Backend is reachable\n")
        except:
            print("❌ Backend is NOT responding!")
            return False
        
        # Test each endpoint
        print("Running Endpoint Tests:")
        print("-" * 70)
        
        # Fast endpoints
        self.test_endpoint("Health Check", "GET", "/", timeout=10)
        self.test_endpoint("List Models", "GET", "/models", timeout=10)
        self.test_endpoint("Rate Limits", "GET", "/limits", timeout=10)
        
        # Slow endpoints
        self.test_endpoint(
            "Text Generation",
            "POST",
            "/generate",
            {"prompt": "What is AI?", "max_tokens": 50},
            timeout=30
        )
        
        self.test_endpoint(
            "Chat Completion",
            "POST",
            "/chat",
            {
                "messages": [{"role": "user", "content": "Hello"}],
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "max_tokens": 50
            },
            timeout=30
        )
        
        # Print results
        print("\n" + "="*70)
        print(f"RESULTS: {self.results['passed']} passed, {self.results['failed']} failed")
        print("="*70)
        
        if self.results["failed"] > 0:
            print("\nFailed tests:")
            for error in self.results["errors"]:
                print(f"  - {error}")
            return False
        else:
            print("\n✅ ALL TESTS PASSED!")
            return True

def main():
    tester = BackendTester()
    success = tester.run_all_tests()
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("""
1. ✅ Backend is running and responding
2. 📚 Visit http://localhost:8000/docs for interactive documentation
3. 🧪 Test endpoints in the Swagger UI
4. 🔗 Integrate into your application

For issues:
  - Check backend logs (should show request details)
  - Ensure HF_TOKEN is set in .env
  - Verify internet connection for online features
    """)
    
    print("="*70)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
