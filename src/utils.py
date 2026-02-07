from __future__ import annotations

from typing import List, Tuple

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except Exception:  # pragma: no cover
    from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import settings
from src.document_loader import Document


def chunk_documents(documents: List[Document]) -> Tuple[List[str], List[dict]]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    texts: List[str] = []
    metadatas: List[dict] = []
    for doc in documents:
        chunks = splitter.split_text(doc.text)
        texts.extend(chunks)
        metadatas.extend([{"source": doc.source}] * len(chunks))
    return texts, metadatas
