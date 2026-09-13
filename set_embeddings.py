from src.core.llm.embeddings import Embeddings

if __name__ == "__main__":
    file_path = "documents/resume.md"
    load_embeddings = Embeddings()
    vector_store = load_embeddings.set_embeddings(file_path)
    print(f"Vector store created: {vector_store}")