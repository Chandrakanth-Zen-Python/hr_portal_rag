from __future__ import annotations

from typing import Dict, List

from config import settings
from src.embeddings import EmbeddingsManager
from src.llm import BedrockLLM
from src.vector_store import VectorStore


PROMPT_TEMPLATE = """
You are an internal policy assistant. Answer the question using ONLY the provided context.
If the answer is not in the context, say you do not have enough information.

Question:
{question}

Context:
{context}

Answer with concise bullet points and include sources in brackets like [source].
""".strip()


class RAGPipeline:
    def __init__(self) -> None:
        self.embeddings = EmbeddingsManager()
        self.llm = BedrockLLM()
        self.store = VectorStore()

    def _build_context(self, results: List[tuple]) -> str:
        context_parts = []
        for content, metadata, similarity in results:
            source = metadata.get("source") if isinstance(metadata, dict) else metadata
            context_parts.append(f"Source: {source}\nSimilarity: {similarity:.3f}\n{content}")
        return "\n\n".join(context_parts)

    def answer_query(self, question: str) -> Dict:
        query_embedding = self.embeddings.embed_text(question, is_query=True)
        results = self.store.similarity_search(
            query_embedding=query_embedding,
            top_k=settings.similarity_top_k,
            threshold=settings.similarity_threshold,
        )
        if not results:
            results = self.store.similarity_search(
                query_embedding=query_embedding,
                top_k=settings.similarity_top_k,
                threshold=-1,
            )
        context = self._build_context(results)
        prompt = PROMPT_TEMPLATE.format(question=question, context=context)
        answer = self.llm.generate(prompt)
        sources = [r[1] for r in results]
        return {"answer": answer, "sources": sources}
