"""
Hugging Face Serverless Inference API Backend (ONLINE)
Uses the official InferenceClient for reliable online AI
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional
from huggingface_hub import InferenceClient
from config import HF_TOKEN

# Initialize Hugging Face Inference Client
# NOTE: For free Inference API, initialize without parameters
# The token is automatically loaded from environment (HF_TOKEN)
# Or it can be set via HfApi().whoami()
client = InferenceClient(api_key=HF_TOKEN) if HF_TOKEN else InferenceClient()

# Initialize FastAPI app
app = FastAPI(
    title="Hugging Face Serverless Inference Backend",
    description="Backend for text generation using Hugging Face Online API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class TextGenerationRequest(BaseModel):
    """Request model for text generation"""
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Which is the largest country?",
                "max_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
    )

class TextGenerationResponse(BaseModel):
    """Response model for text generation"""
    prompt: str
    generated_text: str
    model: str
    status: str = "success"

class ChatMessage(BaseModel):
    """Chat message model"""
    role: str  # "user", "assistant", "system"
    content: str

class ChatCompletionRequest(BaseModel):
    """Request model for chat completion"""
    messages: list[ChatMessage]
    model: Optional[str] = "mistralai/Mistral-7B-Instruct-v0.2"
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "messages": [
                    {"role": "user", "content": "What is the capital of France?"}
                ],
                "model": "mistralai/Mistral-7B-Instruct-v0.2",
                "max_tokens": 100
            }
        }
    )

class ChatCompletionResponse(BaseModel):
    """Response model for chat completion"""
    message: str
    model: str
    status: str = "success"

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    api_type: str = "Online (Hugging Face Serverless)"

# Routes
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Hugging Face Serverless Inference Backend is running",
        api_type="Online (Hugging Face Serverless)"
    )

@app.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest) -> TextGenerationResponse:
    """
    Generate text using Hugging Face Serverless Inference API
    
    Args:
        request: TextGenerationRequest with prompt and parameters
    
    Returns:
        TextGenerationResponse with generated text
    """
    try:
        print(f"\n📝 Text Generation Request")
        print(f"   Prompt: {request.prompt[:60]}...")
        print(f"   Max tokens: {request.max_tokens}")
        
        # Call Hugging Face text-generation API
        # Note: Do NOT specify model - let the API use its default text-generation model
        # The API will automatically route to an appropriate text-generation model
        # Note: text_generation returns a STRING directly, not an object
        generated_text = client.text_generation(
            prompt=request.prompt,
            # NOTE: NO model parameter - API uses default text-generation model
            max_new_tokens=request.max_tokens or 100,
            temperature=request.temperature or 0.7,
            top_p=request.top_p or 0.9
        )
        
        print(f"✅ Generated: {str(generated_text)[:80]}...")
        
        return TextGenerationResponse(
            prompt=request.prompt,
            generated_text=generated_text,  # ← Direct string from API
            model="default",  # API handles model selection
            status="success"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Text generation failed: {str(e)}"
        print(f"❌ Error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/chat", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """
    Chat completion using Hugging Face Serverless Inference API
    
    Supports chat models like Mistral, Llama, etc.
    
    Args:
        request: ChatCompletionRequest with messages and model
    
    Returns:
        ChatCompletionResponse with the model's response
    """
    try:
        print(f"\n💬 Chat Completion Request")
        print(f"   Model: {request.model}")
        print(f"   Messages: {len(request.messages)}")
        print(f"   First message: {request.messages[0].content[:60]}...")
        
        # Convert Pydantic models to dicts for API
        messages_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        # Call Hugging Face API
        # Note: chat_completion returns a ChatCompletionOutput object
        response = client.chat_completion(
            messages=messages_dict,
            model=request.model,
            max_tokens=request.max_tokens or 100,
            temperature=request.temperature or 0.7
        )
        
        # Extract message content from ChatCompletionOutput
        # Access pattern: response.choices[0].message.content
        message_content = response.choices[0].message.content
        
        print(f"✅ Response: {message_content[:80]}...")
        
        return ChatCompletionResponse(
            message=message_content,
            model=request.model,
            status="success"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Chat completion failed: {str(e)}"
        print(f"❌ Error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/text-to-text")
async def text_to_text(request: TextGenerationRequest):
    """
    Text-to-text generation (flexible endpoint)
    """
    try:
        result = client.text_generation(
            prompt=request.prompt,
            model="gpt2",
            max_new_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return TextGenerationResponse(
            prompt=request.prompt,
            generated_text=result,
            model="gpt2",
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """
    List recommended models
    """
    return {
        "status": "success",
        "models": [
            {
                "name": "gpt2",
                "description": "GPT2 - Fast, good quality",
                "use_case": "General text generation"
            },
            {
                "name": "mistralai/Mistral-7B-Instruct-v0.2",
                "description": "Mistral 7B - Fast, high quality",
                "use_case": "Chat, instruction following"
            },
            {
                "name": "meta-llama/Llama-2-7b-chat-hf",
                "description": "Llama 2 7B - Excellent quality",
                "use_case": "Chat, conversational"
            },
            {
                "name": "tiiuae/falcon-7b-instruct",
                "description": "Falcon 7B - Very fast, good quality",
                "use_case": "Chat, instructions"
            }
        ],
        "note": "Free tier may have rate limits. See /limits for details"
    }

@app.get("/limits")
async def rate_limits():
    """
    Rate limit information
    """
    return {
        "status": "success",
        "free_tier": {
            "requests_per_day": "~1000",
            "concurrent_requests": "Limited",
            "note": "Limits may vary based on demand"
        },
        "considerations": [
            "Shared infrastructure - speed varies",
            "Large models may require PRO account",
            "Rate limit errors possible at peak times",
            "Model may timeout if processing long text"
        ],
        "upgrade_options": [
            "HF Pro: $9/month",
            "Dedicated Endpoints: Custom pricing"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("HUGGING FACE SERVERLESS INFERENCE BACKEND (ONLINE)")
    print("="*60)
    print("Using: Hugging Face Serverless Inference API")
    print("API Type: Online (requires internet)")
    print("Starting server on http://0.0.0.0:8000")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
