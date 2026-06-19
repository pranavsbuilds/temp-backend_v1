import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="OpenAI Mock Server")

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int = 150
    temperature: float = 0.2
    response_format: Dict[str, Any] = None

@app.get("/v1/models")
def get_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "local-model",
                "object": "model",
                "created": 1686935002,
                "owned_by": "local"
            }
        ]
    }

@app.post("/v1/chat/completions")
def create_chat_completion(request: ChatCompletionRequest):
    # Check if this is the startup ping
    is_ping = False
    for msg in request.messages:
        if "ping" in msg.content.lower():
            is_ping = True
            break
            
    if is_ping:
        content = "pong"
    else:
        # Generate question fallback JSON
        content = '{"question": "Generated mock question: What is the primary advantage of virtual memory?", "explanation": "Virtual memory allows executing processes that are larger than physical memory by mapping it to disk space."}'
    
    return {
        "id": "chatcmpl-mock",
        "object": "chat.completion",
        "created": 1686935002,
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 10,
            "total_tokens": 20
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Mock OpenAI Server on http://127.0.0.1:3000")
    uvicorn.run(app, host="127.0.0.1", port=3000)
