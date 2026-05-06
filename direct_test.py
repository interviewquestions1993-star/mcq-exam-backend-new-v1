#!/usr/bin/env python
"""
Direct test - no API server needed
Just demonstrates the model working locally
"""
print("Starting direct model test...")
print("This will download GPT2 (first time only) and generate text\n")

try:
    print("Step 1: Importing transformers library...")
    from transformers import pipeline
    print("✓ Imported successfully\n")
    
    print("Step 2: Loading GPT2 model (this may take 1-2 minutes on first run)...")
    generator = pipeline('text-generation', model='gpt2', device='cpu')
    print("✓ Model loaded\n")
    
    print("Step 3: Generating text from your prompt...")
    prompt = "Which is the largest country?"
    print(f"Prompt: {prompt}\n")
    
    result = generator(
        prompt,
        max_new_tokens=50,
        temperature=0.7,
        do_sample=True
    )
    
    generated_text = result[0]["generated_text"]
    
    print("="*60)
    print("✓✓✓ SUCCESS! ✓✓✓")
    print("="*60)
    print(f"\nGenerated Text:\n{generated_text}\n")
    print("="*60)
    print("\nNow you can use this with the FastAPI backend!")
    print("Run: python main_local.py")
    print("Then visit: http://localhost:8000/docs")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
