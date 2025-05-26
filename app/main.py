from fastapi import FastAPI, HTTPException

from app.api.endpoints.chat import ChatRequest, ChatResponse, handle_message

app = FastAPI()

@app.get("/")
def main():
    return "Server Okay"

@app.post("/api/chat/message", response_model=ChatResponse)
def chat_with_user(request: ChatRequest):
    try:
        result = handle_message(request.message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    