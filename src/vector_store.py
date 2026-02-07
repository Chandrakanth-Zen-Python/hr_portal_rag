from __future__ import annotations

import json
from typing import Iterable, List, Tuple

import psycopg2
from pgvector import Vector
from pgvector.psycopg2 import register_vector

from config import settings


class VectorStore:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            dbname=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
        )
        self._ensure_extension()
        register_vector(self.conn)

    def _ensure_extension(self) -> None:
        with self.conn, self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    def close(self) -> None:
        self.conn.close()

    def ensure_schema(self, embedding_dim: int) -> None:
        with self.conn, self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB,
                    embedding VECTOR(%s) NOT NULL
                );
                """,
                (embedding_dim,),
            )
            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS documents_embedding_idx
                ON documents USING ivfflat (embedding vector_cosine_ops);
                """
            )

    def add_documents(
        self, texts: Iterable[str], metadatas: Iterable[dict], embeddings: Iterable[List[float]]
    ) -> None:
        with self.conn, self.conn.cursor() as cur:
            for text, meta, embedding in zip(texts, metadatas, embeddings):
                cur.execute(
                    """
                    INSERT INTO documents (content, metadata, embedding)
                    VALUES (%s, %s, %s);
                    """,
                    (text, json.dumps(meta), embedding),
                )

    def clear_documents(self) -> None:
        with self.conn, self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE documents;")

    def similarity_search(
        self, query_embedding: List[float], top_k: int, threshold: float | None
    ) -> List[Tuple[str, dict, float]]:
        if not query_embedding:
            return []
        with self.conn.cursor() as cur:
            if threshold is None or threshold < 0:
                cur.execute(
                    """
                    SELECT content, metadata, 1 - (embedding <=> %s) AS similarity
                    FROM documents
                    ORDER BY embedding <=> %s
                    LIMIT %s;
                    """,
                    (Vector(query_embedding), Vector(query_embedding), top_k),
                )
            else:
                cur.execute(
                    """
                    SELECT content, metadata, 1 - (embedding <=> %s) AS similarity
                    FROM documents
                    WHERE 1 - (embedding <=> %s) >= %s
                    ORDER BY embedding <=> %s
                    LIMIT %s;
                    """,
                    (
                        Vector(query_embedding),
                        Vector(query_embedding),
                        threshold,
                        Vector(query_embedding),
                        top_k,
                    ),
                )
            rows = cur.fetchall()
        results = []
        for content, metadata, similarity in rows:
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except json.JSONDecodeError:
                    metadata = {"source": metadata}
            results.append((content, metadata or {}, float(similarity)))
        return results
