import sys
import os

print("=== STARTING TEST ===", file=sys.stderr, flush=True)

from dotenv import load_dotenv
print("Step 1: Importing dotenv", file=sys.stderr, flush=True)

load_dotenv()
print("Step 2: Loaded .env", file=sys.stderr, flush=True)

hf_token = os.getenv("HF_TOKEN")
print(f"Step 3: Token exists: {bool(hf_token)}", file=sys.stderr, flush=True)

if not hf_token:
    print("ERROR: No token!", file=sys.stderr, flush=True)
    sys.exit(1)

from huggingface_hub import InferenceClient
print("Step 4: Imported InferenceClient", file=sys.stderr, flush=True)

client = InferenceClient(api_key=hf_token)
print("Step 5: Created client", file=sys.stderr, flush=True)

print("Step 6: Calling text_generation...", file=sys.stderr, flush=True)

try:
    response = client.text_generation(
        prompt="Hello",
        max_new_tokens=20,
    )
    print(f"✅ SUCCESS: {response}", file=sys.stderr, flush=True)
    print(response)
except Exception as e:
    print(f"❌ ERROR: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=== TEST COMPLETE ===", file=sys.stderr, flush=True)
