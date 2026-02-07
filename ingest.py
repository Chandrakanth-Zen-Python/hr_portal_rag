import argparse

from src.document_loader import load_from_directory
from src.embeddings import EmbeddingsManager
from src.utils import chunk_documents
from src.vector_store import VectorStore


def create_vector_store(data_dir: str) -> None:
    print(f"Loading documents from {data_dir} ...")
    documents = load_from_directory(data_dir)
    texts, metadatas = chunk_documents(documents)
    if not texts:
        raise SystemExit("No documents loaded.")

    print("Generating embeddings...")
    embeddings_manager = EmbeddingsManager()
    embeddings = [embeddings_manager.embed_text(text) for text in texts]

    print("Writing to PostgreSQL...")
    store = VectorStore()
    store.ensure_schema(embedding_dim=len(embeddings[0]))
    store.add_documents(texts, metadatas, embeddings)
    store.close()
    print(f"Ingested {len(texts)} chunks.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest documents into PostgreSQL.")
    parser.add_argument(
        "--data-dir",
        default="data/sample_documents",
        help="Directory containing documents to ingest.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing embeddings before ingesting.",
    )
    args = parser.parse_args()
    if args.reset:
        store = VectorStore()
        store.clear_documents()
        store.close()
    create_vector_store(args.data_dir)
