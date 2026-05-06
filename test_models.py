#!/usr/bin/env python
"""Test with different models"""

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
token = os.getenv("HF_TOKEN")

client = InferenceClient(api_key=token, model="gpt2")

print("Testing with gpt2...")
try:
    response = client.text_generation("Hello world")
    print(f"✅ Success: {response}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\nTesting with distilgpt2...")
try:
    response = client.text_generation("Hello world", model="distilgpt2")
    print(f"✅ Success: {response}")
except Exception as e:
    print(f"❌ Error: {e}")
