from src.embeddings import EmbeddingsManager
from src.vector_store import VectorStore


if __name__ == "__main__":
    embeddings = EmbeddingsManager()
    sample = embeddings.embed_text("Initialize schema")

    store = VectorStore()
    store.ensure_schema(embedding_dim=len(sample))
    store.close()
    print("Database initialized.")
