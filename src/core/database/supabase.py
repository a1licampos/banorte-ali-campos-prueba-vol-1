import os
from supabase.client import Client, create_client

class Supabase():
    def __init__(self):
        try:
            self.SUPABASE: Client = create_client(
                supabase_url=os.getenv("SUPABASE_URL"),
                supabase_key=os.getenv("SUPABASE_KEY")
            )
        except Exception as e:
            print(f"Error LoadEmbeddings() initializing: {e}")
            raise

    def set_save_interaction(self, user_query: str, ai_response: str):
        try:
            data = {
                "user_query": user_query,
                "ai_response": ai_response
            }
            self.SUPABASE.table("chat_history").insert(data).execute()
        except Exception as e:
            print(f"Error guardando el historial en Supabase: {e}")
            raise

    def get_recent_history(self, limit: int = 2) -> list:
        try:
            response = self.SUPABASE.table("chat_history").select("*").order("created_at", desc=True).limit(limit).execute()
            history = response.data[::-1]
            return history
        except Exception as e:
            print(f"Error obteniendo el historial: {e}")
            return []