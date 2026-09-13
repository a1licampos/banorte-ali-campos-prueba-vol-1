import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chatbot.chat import Chatbot

app = FastAPI(title="Chatbot API Banorte",
              version="1.0.0",
              description="Prueba Ali Campos (chatbot CV)")

chatbot = Chatbot()

class ChatRequest(BaseModel):
    query: str

@app.post("/v1/responses")
async def get_response(request: ChatRequest):
    try:
        answer = chatbot.chat_with_groq(request.query)
        return {"response": answer}
    except Exception as e:
        print(f"Error retrieving context: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

def main():
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == '__main__':
    main()

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba