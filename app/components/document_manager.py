from __future__ import annotations

from pathlib import Path

import streamlit as st

from config import settings
from src.document_loader import load_documents
from src.embeddings import EmbeddingsManager
from src.utils import chunk_documents
from src.vector_store import VectorStore

UPLOAD_DIR = Path("data/processed")


def _save_uploads(files: list) -> list[str]:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    saved_paths = []
    for file in files:
        dest = UPLOAD_DIR / file.name
        dest.write_bytes(file.getbuffer())
        saved_paths.append(str(dest))
    return saved_paths


def render_document_manager() -> None:
    st.subheader("Document Manager")
    st.caption("Upload PDF, DOCX, or TXT documents to expand the knowledge base.")

    uploads = st.file_uploader(
        "Upload documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
    )

    if st.button("Ingest Documents"):
        if not uploads:
            st.warning("Please upload at least one document.")
            return

        with st.spinner("Saving uploads..."):
            paths = _save_uploads(uploads)

        with st.spinner("Loading documents..."):
            documents = load_documents(paths)
            texts, metadatas = chunk_documents(documents)

        if not texts:
            st.warning("No text found in the uploaded documents.")
            return

        embeddings_manager = EmbeddingsManager()
        embeddings = []
        with st.spinner("Generating embeddings..."):
            for text in texts:
                embeddings.append(embeddings_manager.embed_text(text))

        store = VectorStore()
        store.ensure_schema(embedding_dim=len(embeddings[0]))

        with st.spinner("Writing to database..."):
            store.add_documents(texts, metadatas, embeddings)
        store.close()

        st.success(f"Ingested {len(texts)} chunks into the vector store.")

    st.markdown(
        f"**Current settings**: top_k={settings.similarity_top_k}, "
        f"threshold={settings.similarity_threshold}"
    )
