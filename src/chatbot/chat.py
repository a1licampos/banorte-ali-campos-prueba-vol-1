import os
from groq import Groq
from dotenv import load_dotenv
from src.core.llm.embeddings import Embeddings
from src.core.database.supabase import Supabase

load_dotenv()

class Chatbot:
    def __init__(self):
        self.embeddings = Embeddings()
        self.supabase = Supabase()
        self.vector_store = self.embeddings.get_supabase_vs()
        self.client_groq = Groq(api_key=os.getenv("API_GROQ"))

    def get_retrive(self, user_query: str):
        try:
            docs = self.vector_store.similarity_search(user_query,
                                                       k=2)
            context = "\n\n---\n\n".join([doc.page_content for doc in docs])

            return context
        except Exception as e:
            print(f"Error querying vector store: {e}")
            raise

    def chat_with_groq(self, user_query: str):
        try:
            system_prompt = (
                "Eres un asistente que responde preguntas sobre un CV."
                "Usa solo la información proporcionada del CV para responder a las preguntas."
                "Si la respuesta no está en el contexto, indica que no tienes esa información."
                "Responde de manera concisa, clara y habla en tercera persona para presentar la información del CV."
                "Responde simpre en español.\n\n"
                f"Contexto:\n{self.get_retrive(user_query)}"
            )

            messages = [{"role": "system", "content": system_prompt}]
            messages.append({"role": "user", "content": user_query})

            completion = self.client_groq.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                reasoning_effort="medium",
                stream=True,
                stop=None
            )

            response_content = ""
            for chunk in completion:
                response_content += chunk.choices[0].delta.content or ""

            self.supabase.set_save_interaction(user_query, response_content)

            return response_content
        except Exception as e:
            print(f"Error during chat with Groq: {e}")
            raise

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba