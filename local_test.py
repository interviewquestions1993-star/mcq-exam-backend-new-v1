"""
Test Hugging Face Inference directly using local transformers
"""
from transformers import pipeline

print("Loading GPT2 model...")
generator = pipeline('text-generation', model='gpt2', device='cpu')

print("\nGenerating text...\n")
prompt = "Which is the largest country?"
result = generator(prompt, max_new_tokens=50)

generated_text = result[0]["generated_text"]
print(f"Prompt: {prompt}")
print(f"\nGenerated: {generated_text}")
