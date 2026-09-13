import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.chatbot.chat import Chatbot

app = FastAPI(title="Chatbot API Banorte",
              version="1.0.0",
              description="Prueba Ali Campos (chatbot CV)")

chatbot = Chatbot()

# 1. Definir los modelos de entrada de Open Responses
class Message(BaseModel):
    role: str
    content: str

class OpenResponseRequest(BaseModel):
    model: Optional[str] = "default-model"
    input: List[Message]
    stream: Optional[bool] = False

# 2. Inyectar el modelo en el endpoint
@app.post("/v1/responses")
async def get_response(request: OpenResponseRequest):
    try:
        # Extraer el último mensaje del usuario del historial
        user_messages = [msg for msg in request.input if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No se encontró un mensaje de usuario en el input.")
        
        user_query = user_messages[-1].content

        # Llamar a tu función de Groq
        answer = chatbot.chat_with_groq(user_query)

        # 3. Retornar el formato exacto que espera Open Responses (síncrono)
        return {
            "status": "completed",
            "model": request.model,
            "output": [
                {
                    "role": "assistant",
                    "content": answer
                }
            ]
        }
        
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