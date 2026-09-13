import os
from dotenv import load_dotenv
from supabase.client import Client, create_client
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

class Embeddings():

    def __init__(self):
        try:
            self.SUPABASE: Client = create_client(
                supabase_url=os.getenv("SUPABASE_URL"),
                supabase_key=os.getenv("SUPABASE_KEY")
            )
            self.EMBEDDINGS_MODEL = OpenAIEmbeddings(api_key=os.getenv("API_OPENAI"),
                                                     model="text-embedding-3-small")
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=150,
            )
        except Exception as e:
            print(f"Error LoadEmbeddings() initializing: {e}")
            raise

    def get_load_doc(self, file_path:str) -> list:
        try:
            loader = TextLoader(file_path=file_path,
                                encoding="utf-8")
            
            docs = loader.load()

            return docs
        except Exception as e:
            print(f"Error get_load_document(): {e}")
            raise

    def set_embeddings(self, file_path:str) -> SupabaseVectorStore:
        try:
            docs = self.get_load_doc(file_path)
            split_docs = self.text_splitter.split_documents(docs)

            vector_store = SupabaseVectorStore.from_documents(
                documents=split_docs,
                embedding=self.EMBEDDINGS_MODEL,
                client=self.SUPABASE,
                table_name="documents",
                query_name="match_documents"
            )
            print(f"{len(split_docs)} documents were embedded and stored in Supabase.")

            return vector_store
        except Exception as e:
            print(f"Error set_embeddings(): {e}")
            raise
    
    def get_supabase_vs(self):
        try:
            vector_store = SupabaseVectorStore(
                embedding=self.EMBEDDINGS_MODEL,
                client=self.SUPABASE,
                table_name="documents",
                query_name="match_documents"
            )
            return vector_store
        except Exception as e:
            print(f"Error get_supabase_vs(): {e}")
            raise

#    _____
#   ( \/ @\____
#   /           O
#  /   (_|||||_/
# /____/  |||
#       kimba