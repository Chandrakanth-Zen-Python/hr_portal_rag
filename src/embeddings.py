import json
from typing import List

import boto3

from config import settings


class EmbeddingsManager:
    def __init__(self) -> None:
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.model_id = settings.embeddings_model

    def embed_text(self, text: str, is_query: bool = False) -> List[float]:
        if not text:
            return []

        if "titan-embed" in self.model_id:
            body = json.dumps({"inputText": text})
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            payload = json.loads(response["body"].read())
            return payload["embedding"]

        if "cohere.embed" in self.model_id:
            input_type = "search_query" if is_query else "search_document"
            body = json.dumps({"texts": [text], "input_type": input_type})
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            payload = json.loads(response["body"].read())
            return payload["embeddings"][0]

        raise ValueError(f"Unsupported embeddings model: {self.model_id}")
