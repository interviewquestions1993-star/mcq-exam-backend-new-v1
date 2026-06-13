"""
Minimal test backend without langchain to verify uvicorn works.
"""
import os
import sys

# Ensure project root is on path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Test MCQ Generator")

class SimpleRequest(BaseModel):
    message: str = "test"

@app.post("/api/test")
def test_endpoint(request: SimpleRequest):
    return {"status": "ok", "message": request.message}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("Starting minimal test server on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
