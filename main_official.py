"""
FastAPI Backend using Official Hugging Face InferenceClient
This follows the exact recommended approach from Hugging Face documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional
from huggingface_hub import InferenceClient
from config import API_HOST, API_PORT, HF_TOKEN

# Initialize FastAPI app
app = FastAPI(
    title="Hugging Face Inference Backend (Official)",
    description="Backend for AI inference using official InferenceClient",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize official InferenceClient with api_key
client = InferenceClient(api_key=HF_TOKEN)


# Request/Response models
class TextGenerationRequest(BaseModel):
    """Request model for text generation"""
    prompt: str
    max_new_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    model: Optional[str] = "google/gemma-2-2b-it"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Explain what a neural network is in two sentences.",
                "max_new_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "model": "google/gemma-2-2b-it"
            }
        }
    )


class TextGenerationResponse(BaseModel):
    """Response model for text generation"""
    prompt: str
    model: str
    generated_text: str
    tokens_used: int


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # "user" or "assistant"
    content: str


class ChatCompletionRequest(BaseModel):
    """Request model for chat completion"""
    messages: list[ChatMessage]
    max_tokens: Optional[int] = 200
    temperature: Optional[float] = 0.7
    model: Optional[str] = "mistralai/Mistral-7B-Instruct-v0.2"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "What is machine learning?"
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.7,
                "model": "mistralai/Mistral-7B-Instruct-v0.2"
            }
        }
    )


class ChatCompletionResponse(BaseModel):
    """Response model for chat completion"""
    model: str
    message: str
    tokens_used: int


# Health check endpoint
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Hugging Face Inference Backend (Official InferenceClient) is running",
        "version": "2.0.0"
    }


# Text generation endpoint
@app.post("/generate", response_model=TextGenerationResponse, tags=["Generation"])
async def generate_text(request: TextGenerationRequest):
    """
    Generate text using Hugging Face model
    
    Official InferenceClient method: client.text_generation()
    
    Returns:
        TextGenerationResponse with generated text
    """
    try:
        # Use official InferenceClient text_generation method
        response = client.text_generation(
            prompt=request.prompt,
            model=request.model,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
        )
        
        # Response is a string directly from official InferenceClient
        return TextGenerationResponse(
            prompt=request.prompt,
            model=request.model,
            generated_text=response,
            tokens_used=len(response.split())  # Approximate token count
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        )


# Chat completion endpoint
@app.post("/chat", response_model=ChatCompletionResponse, tags=["Chat"])
async def chat_completion(request: ChatCompletionRequest):
    """
    Chat completion endpoint using official InferenceClient
    
    Official InferenceClient method: client.chat_completion()
    
    Returns:
        ChatCompletionResponse with assistant message
    """
    try:
        # Convert message models to dicts for the client
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Use official InferenceClient chat_completion method
        response = client.chat_completion(
            messages=messages,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        
        # Extract content from official response object
        assistant_message = response.choices[0].message.content
        
        return ChatCompletionResponse(
            model=request.model,
            message=assistant_message,
            tokens_used=len(assistant_message.split())  # Approximate token count
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat completion failed: {str(e)}"
        )


# Summarization endpoint
@app.post("/summarize", response_model=TextGenerationResponse, tags=["Summarization"])
async def summarize_text(request: TextGenerationRequest):
    """
    Summarize text using a model
    
    Uses text generation with a summarization prompt
    """
    try:
        # Create summarization prompt
        summary_prompt = f"Summarize the following text:\n\n{request.prompt}\n\nSummary:"
        
        response = client.text_generation(
            prompt=summary_prompt,
            model=request.model,
            max_new_tokens=request.max_new_tokens or 100,
            temperature=request.temperature,
            top_p=request.top_p,
        )
        
        return TextGenerationResponse(
            prompt=request.prompt,
            model=request.model,
            generated_text=response,
            tokens_used=len(response.split())
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )


# Run the server
if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║    HUGGING FACE OFFICIAL InferenceClient Backend         ║
    ║                    Version 2.0.0                         ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Starting FastAPI server...
    - API Documentation: http://localhost:{}/docs
    - Alternative docs: http://localhost:{}/redoc
    """.format(API_PORT, API_PORT))
    
    uvicorn.run(
        "main_official:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
        log_level="info"
    )
