import os
from dotenv import load_dotenv

print("Step 1: Loading .env...")
load_dotenv()

print("Step 2: Getting token...")
hf_token = os.getenv("HF_TOKEN")
print(f"Token loaded: {bool(hf_token)}")

if not hf_token:
    print("ERROR: No token!")
    exit(1)

print("Step 3: Importing InferenceClient...")
from huggingface_hub import InferenceClient

print("Step 4: Creating client...")
client = InferenceClient(api_key=hf_token)

print("Step 5: Making request...")
try:
    response = client.text_generation(
        prompt="Hello world",
        max_new_tokens=20,
    )
    print(f"\n✅ SUCCESS!")
    print(f"Response: {response}")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
