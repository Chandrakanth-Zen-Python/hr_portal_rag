import argparse

from src.document_loader import load_from_directory
from src.embeddings import EmbeddingsManager
from src.utils import chunk_documents
from src.vector_store import VectorStore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch ingest documents into PostgreSQL.")
    parser.add_argument("--data-dir", required=True, help="Directory containing documents.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing embeddings before ingesting.",
    )
    args = parser.parse_args()

    documents = load_from_directory(args.data_dir)
    texts, metadatas = chunk_documents(documents)
    if not texts:
        raise SystemExit("No documents loaded.")

    embeddings_manager = EmbeddingsManager()
    embeddings = [embeddings_manager.embed_text(text) for text in texts]

    store = VectorStore()
    store.ensure_schema(embedding_dim=len(embeddings[0]))
    if args.reset:
        store.clear_documents()
    store.add_documents(texts, metadatas, embeddings)
    store.close()
    print(f"Ingested {len(texts)} chunks.")
