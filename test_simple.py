import requests
import json

print("\n" + "="*70)
print("BACKEND QUICK TEST")
print("="*70)

# Test 1: Health
print("\n✓ Test 1: Health Check")
try:
    r = requests.get('http://localhost:8000/', timeout=10)
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.json()}")
    if r.status_code == 200:
        print("  ✅ PASSED")
    else:
        print("  ❌ FAILED")
except Exception as e:
    print(f"  ❌ FAILED: {str(e)[:80]}")

# Test 2: Models
print("\n✓ Test 2: List Models")
try:
    r = requests.get('http://localhost:8000/models', timeout=10)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  Models: {len(data.get('models', []))} available")
        print("  ✅ PASSED")
    else:
        print(f"  Response: {r.text[:80]}")
        print("  ❌ FAILED")
except Exception as e:
    print(f"  ❌ FAILED: {str(e)[:80]}")

# Test 3: Limits
print("\n✓ Test 3: Rate Limits")
try:
    r = requests.get('http://localhost:8000/limits', timeout=10)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"  Free Tier: {data.get('free_tier', 'N/A')}")
        print("  ✅ PASSED")
    else:
        print(f"  Response: {r.text[:80]}")
        print("  ❌ FAILED")
except Exception as e:
    print(f"  ❌ FAILED: {str(e)[:80]}")

# Test 4: Generate
print("\n✓ Test 4: Text Generation")
try:
    r = requests.post('http://localhost:8000/generate', json={
        'prompt': 'What is AI?',
        'max_tokens': 50
    }, timeout=30)
    print(f"  Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        text = data.get('generated_text', '')
        print(f"  Generated: {text[:60]}...")
        print("  ✅ PASSED")
    else:
        print(f"  Response: {r.text[:80]}")
        print("  ❌ FAILED")
except Exception as e:
    print(f"  ❌ FAILED: {str(e)[:80]}")

print("\n" + "="*70)
print("Tests complete!")
print("="*70)
