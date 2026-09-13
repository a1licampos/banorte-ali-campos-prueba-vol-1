import time
import uuid
from typing import List, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.chatbot.chat import Chatbot

app = FastAPI(
    title="Chatbot API Banorte",
    version="1.0.0",
    description="Prueba Ali Campos (chatbot CV) - Compatible con OpenAI API"
)

chatbot = Chatbot()

# --- Modelos de Request (Entrada) ---
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "default-model"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False

# --- Modelos de Response (Salida) ---
class ChoiceMessage(BaseModel):
    role: str
    content: str

class Choice(BaseModel):
    index: int
    message: ChoiceMessage
    finish_reason: str

class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage

# --- Endpoint ---
# El estándar usa la ruta /v1/chat/completions
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    try:
        # Extraer el último mensaje del usuario del historial
        user_message = ""
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_message = msg.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No se encontró un mensaje de usuario.")

        # Obtener respuesta de tu lógica interna
        answer = chatbot.chat_with_groq(user_message)

        # Construir la respuesta con el formato de OpenAI
        return ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex}",
            object="chat.completion",
            created=int(time.time()),
            model=request.model,
            choices=[
                Choice(
                    index=0,
                    message=ChoiceMessage(role="assistant", content=answer),
                    finish_reason="stop"
                )
            ],
            usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0) # Valores mockeados, actualiza si tienes el conteo real
        )

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