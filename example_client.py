"""
Example client for the Hugging Face Inference Backend
Shows how to integrate with the API
"""
import requests
import json


class HFBackendClient:
    """Simple client for the Hugging Face Inference Backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """Generate text from a prompt"""
        response = requests.post(
            f"{self.base_url}/generate",
            json={
                "prompt": prompt,
                "max_new_tokens": max_tokens,
                "temperature": temperature
            }
        )
        response.raise_for_status()
        return response.json()["generated_text"]
    
    def summarize(self, text: str) -> str:
        """Summarize text"""
        response = requests.post(
            f"{self.base_url}/summarize",
            json={"text": text}
        )
        response.raise_for_status()
        return response.json()["summary"]
    
    def chat(self, message: str, max_tokens: int = 150) -> str:
        """Chat with the model"""
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "prompt": message,
                "max_new_tokens": max_tokens,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        return response.json()["generated_text"]
    
    def health_check(self) -> bool:
        """Check if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/")
            return response.status_code == 200
        except:
            return False


def example_usage():
    """Example usage of the client"""
    
    # Initialize client
    client = HFBackendClient()
    
    # Check if backend is running
    if not client.health_check():
        print("Error: Backend is not running!")
        print("Start it with: python main.py")
        return
    
    print("✓ Backend is running!\n")
    
    # Example 1: Generate text
    print("="*60)
    print("Example 1: Text Generation")
    print("="*60)
    prompt = "What are the benefits of machine learning?"
    print(f"Prompt: {prompt}\n")
    try:
        result = client.generate_text(prompt, max_tokens=100)
        print(f"Response:\n{result}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 2: Chat
    print("="*60)
    print("Example 2: Chat")
    print("="*60)
    message = "Explain quantum computing in simple terms"
    print(f"Message: {message}\n")
    try:
        result = client.chat(message)
        print(f"Response:\n{result}\n")
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Example 3: Summarize
    print("="*60)
    print("Example 3: Text Summarization")
    print("="*60)
    text = """
    Artificial intelligence (AI) is transforming industries worldwide. 
    From healthcare to finance, AI systems are learning patterns in data 
    and making decisions that were once reserved for humans. Machine learning, 
    a subset of AI, enables computers to learn from data without being explicitly 
    programmed. Deep learning takes this further, using neural networks to model 
    complex patterns in large amounts of data.
    """
    print(f"Text: {text.strip()[:100]}...\n")
    try:
        result = client.summarize(text.strip())
        print(f"Summary:\n{result}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def interactive_mode():
    """Interactive chat with the model"""
    client = HFBackendClient()
    
    if not client.health_check():
        print("Error: Backend is not running!")
        return
    
    print("\n" + "="*60)
    print("Interactive Chat Mode")
    print("="*60)
    print("Type 'exit' to quit, 'help' for commands\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if user_input.lower() == "help":
            print("\nCommands:")
            print("  exit - Quit the chat")
            print("  help - Show this help")
            print("  clear - Clear screen")
            print("\nOtherwise, type your prompt and press Enter\n")
            continue
        
        if user_input.lower() == "clear":
            import os
            os.system("cls" if os.name == "nt" else "clear")
            continue
        
        if not user_input:
            continue
        
        print("\nThinking...\n")
        try:
            response = client.chat(user_input, max_tokens=200)
            print(f"AI: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# HUGGING FACE INFERENCE BACKEND - CLIENT EXAMPLES")
    print("#"*60 + "\n")
    
    print("Choose mode:")
    print("1. Run examples")
    print("2. Interactive chat")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        example_usage()
    elif choice == "2":
        interactive_mode()
    else:
        print("Goodbye!")
