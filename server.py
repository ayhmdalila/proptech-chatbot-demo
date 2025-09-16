from fastapi import FastAPI
from pydantic import BaseModel
from generator import generate_response

app = FastAPI()

class ChatRequest(BaseModel):
    chat_history: list

@app.post("/chat/chat/completions")
def generate_llm_response(request: ChatRequest):
    chat_history = request.chat_history[-5:]

    return {"response": generate_response(chat_history)}
