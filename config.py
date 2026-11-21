"""
Configuration module for Hugging Face API integration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face configuration (optional compatibility)
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "deepseek-ai/DeepSeek-V4-Flash")
HF_API_URL = "https://router.huggingface.co/v1"  # OpenAI-compatible endpoint

# NVIDIA-hosted models used by the public MCQ generation endpoint.
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
NVIDIA_MODELS = [
    model.strip()
    for model in os.getenv(
        "NVIDIA_MODELS",
        "nvidia/nemotron-3.5-bolt-e4b,minimaxai/minimax-m3.1-flash",
    ).split(",")
    if model.strip()
]
NVIDIA_MODEL_TIMEOUT_SECONDS = float(os.getenv("NVIDIA_MODEL_TIMEOUT_SECONDS", "20"))
NVIDIA_TOTAL_TIMEOUT_SECONDS = float(os.getenv("NVIDIA_TOTAL_TIMEOUT_SECONDS", "45"))

# Ollama / local model configuration
# Ollama client libraries usually add /v1 automatically, so keep the base URL at the server root.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi4-mini")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "ncert_grade8")
PDF_FOLDER = os.getenv("PDF_FOLDER", "ncert_pdfs")

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Firebase / Firestore configuration
FIREBASE_ENABLED = os.getenv("FIREBASE_ENABLED", "false").strip().lower() == "true"
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "")
FIREBASE_CREDENTIALS_JSON = os.getenv("FIREBASE_CREDENTIALS_JSON", "")
FIREBASE_COLLECTION = os.getenv("FIREBASE_COLLECTION", "ai_responses")
FIRESTORE_HISTORY_COLLECTION = os.getenv("FIRESTORE_HISTORY_COLLECTION", "mcq_history")
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
