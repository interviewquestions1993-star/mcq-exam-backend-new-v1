"""
Alternative FastAPI backend using local Transformers library
This works offline and doesn't rely on the Hugging Face Inference API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional
from transformers import pipeline
import threading

# Global pipeline instances (lazy loaded)
_pipelines = {}
_lock = threading.Lock()

def get_pipeline(task: str, model: str):
    """Get or create a pipeline instance"""
    key = f"{task}:{model}"
    if key not in _pipelines:
        print(f"Loading {task} pipeline with model {model}...")
        _pipelines[key] = pipeline(task, model=model, device='cpu')
        print(f"✓ {task} pipeline loaded")
    return _pipelines[key]

# Initialize FastAPI app
app = FastAPI(
    title="Hugging Face Local Backend",
    description="Backend for text generation using local Transformers library",
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
    max_new_tokens: Optional[int] = 50
    temperature: Optional[float] = 0.7
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Which is the largest country?",
                "max_new_tokens": 50,
                "temperature": 0.7
            }
        }
    )

class TextGenerationResponse(BaseModel):
    """Response model for text generation"""
    prompt: str
    generated_text: str
    status: str = "success"

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str

# Routes
@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Hugging Face Local Backend is running"
    )

@app.post("/generate", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest) -> TextGenerationResponse:
    """
    Generate text using local Transformers library
    
    Args:
        request: TextGenerationRequest with prompt and parameters
    
    Returns:
        TextGenerationResponse with generated text
    """
    try:
        print(f"\nGenerating text for prompt: {request.prompt[:50]}...")
        
        # Get the pipeline
        generator = get_pipeline("text-generation", "gpt2")
        
        # Generate text
        result = generator(
            request.prompt,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            do_sample=True
        )
        
        generated_text = result[0]["generated_text"]
        print(f"✓ Generation complete\n")
        
        return TextGenerationResponse(
            prompt=request.prompt,
            generated_text=generated_text,
            status="success"
        )
    
    except Exception as e:
        print(f"✗ Error: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=TextGenerationResponse)
async def chat_endpoint(request: TextGenerationRequest) -> TextGenerationResponse:
    """Chat endpoint (alias for generate)"""
    return await generate_text(request)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("HUGGING FACE LOCAL BACKEND")
    print("="*60)
    print("Starting server on http://0.0.0.0:8000")
    print("First generation will download and load the model...")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
