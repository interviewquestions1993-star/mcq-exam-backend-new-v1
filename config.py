"""
Configuration module for Hugging Face API integration
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Hugging Face configuration
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_MODEL = os.getenv("HF_MODEL", "deepseek-ai/DeepSeek-V4-Flash")
HF_API_URL = "https://router.huggingface.co/v1"  # OpenAI-compatible endpoint

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Validation
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in environment variables. Please set it in .env file")
