#!/usr/bin/env python
"""Working Hugging Face Online Inference Example"""

import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
hf_token = os.getenv("HF_TOKEN")

if not hf_token:
    print("❌ ERROR: HF_TOKEN not found in .env file")
    sys.exit(1)

print(f"✅ Token loaded: {hf_token[:20]}...")

# Import with timeout handling
try:
    print("Importing InferenceClient...")
    from huggingface_hub import InferenceClient
    print("✅ Import successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Create client
print("Creating client...")
client = InferenceClient(api_key=hf_token)
print("✅ Client created")

# Test with a simple prompt
print("\nMaking API request...")
prompt = "The future of AI is"

try:
    print(f"Prompt: {prompt}")
    print("Waiting for response...")
    
    result = client.text_generation(
        prompt=prompt,
        max_new_tokens=50,
    )
    
    print(f"\n✅ SUCCESS!")
    print(f"Result: {result}")
    
except ConnectionError as e:
    print(f"❌ Connection Error: {e}")
    sys.exit(1)
except TimeoutError as e:
    print(f"❌ Timeout Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error ({type(e).__name__}): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
