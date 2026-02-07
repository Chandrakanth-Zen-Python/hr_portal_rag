from src.rag_pipeline import RAGPipeline


if __name__ == "__main__":
    pipeline = RAGPipeline()
    result = pipeline.answer_query("What is the remote work policy?")
    print(result["answer"])
