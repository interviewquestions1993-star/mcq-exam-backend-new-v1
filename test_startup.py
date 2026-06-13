#!/usr/bin/env python3
"""Test script to debug backend startup issues."""

import sys
import os
import time

# Ensure project root is on path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

print("=" * 60)
print("TESTING BACKEND STARTUP")
print("=" * 60)

# Test 1: Import modules
print("\n[1/5] Testing imports...")
try:
    from langchain_ollama import OllamaEmbeddings
    print("✓ OllamaEmbeddings imported")
except Exception as e:
    print(f"✗ Failed to import OllamaEmbeddings: {e}")
    sys.exit(1)

try:
    from langchain_chroma import Chroma
    print("✓ Chroma imported")
except Exception as e:
    print(f"✗ Failed to import Chroma: {e}")
    sys.exit(1)

try:
    from openai import OpenAI
    print("✓ OpenAI imported")
except Exception as e:
    print(f"✗ Failed to import OpenAI: {e}")
    sys.exit(1)

try:
    from backendv1.config import (
        OLLAMA_BASE_URL,
        OLLAMA_API_KEY,
        CHROMA_PERSIST_DIR,
        CHROMA_COLLECTION_NAME,
    )
    print("✓ Config imported")
    print(f"  - OLLAMA_BASE_URL: {OLLAMA_BASE_URL}")
    print(f"  - CHROMA_PERSIST_DIR: {CHROMA_PERSIST_DIR}")
    print(f"  - CHROMA_COLLECTION_NAME: {CHROMA_COLLECTION_NAME}")
except Exception as e:
    print(f"✗ Failed to import config: {e}")
    sys.exit(1)

# Test 2: Test Ollama connection
print("\n[2/5] Testing Ollama connection...")
try:
    import requests
    resp = requests.get(f"{OLLAMA_BASE_URL.rstrip('/')}/v1/models", timeout=5)
    print(f"✓ Ollama is reachable (status: {resp.status_code})")
except Exception as e:
    print(f"✗ Failed to reach Ollama: {e}")
    sys.exit(1)

# Test 3: Initialize embeddings (with timeout)
print("\n[3/5] Initializing OllamaEmbeddings...")
start = time.time()
try:
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=OLLAMA_BASE_URL,
        validate_model_on_init=False,
    )
    elapsed = time.time() - start
    print(f"✓ OllamaEmbeddings initialized in {elapsed:.2f}s")
except Exception as e:
    print(f"✗ Failed to initialize OllamaEmbeddings: {e}")
    sys.exit(1)

# Test 4: Initialize Chroma vectorstore
print("\n[4/5] Initializing Chroma vectorstore...")
start = time.time()
try:
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION_NAME
    )
    elapsed = time.time() - start
    print(f"✓ Chroma initialized in {elapsed:.2f}s")
    
    # Check if collection has documents
    collection_count = vectorstore._collection.count()
    print(f"  - Collection has {collection_count} documents")
except Exception as e:
    print(f"✗ Failed to initialize Chroma: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Initialize OpenAI client
print("\n[5/5] Initializing OpenAI client...")
start = time.time()
try:
    client = OpenAI(
        base_url=f"{OLLAMA_BASE_URL.rstrip('/')}/v1",
        api_key=OLLAMA_API_KEY
    )
    elapsed = time.time() - start
    print(f"✓ OpenAI client initialized in {elapsed:.2f}s")
except Exception as e:
    print(f"✗ Failed to initialize OpenAI client: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL STARTUP TESTS PASSED!")
print("=" * 60)
