import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.chatbot.chat import Chatbot

app = FastAPI(title="Chatbot API Banorte",
              version="1.0.0",
              description="Prueba Ali Campos (chatbot CV)")

chatbot = Chatbot()

class ChatRequest(BaseModel):
    query: str

@app.post("/v1/responses")
async def get_response(request: Request):
    try:
        payload = await request.json()

        user_query = payload.get("query") or payload.get("message") or payload.get("input") or str(payload)

        answer = chatbot.chat_with_groq(user_query)


        return JSONResponse(
            content={
                "response": answer,
                "message": answer,
                "text": answer,
                "output": answer
            },
            headers={"Content-Type": "application/json"}
        )
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Error interno del servidor"}
        )
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