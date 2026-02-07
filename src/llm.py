import json

import boto3

from config import settings


class BedrockLLM:
    def __init__(self) -> None:
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        self.model_id = settings.llm_model

    def generate(self, prompt: str) -> str:
        if "anthropic.claude" in self.model_id:
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": settings.max_tokens,
                    "temperature": settings.temperature,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            payload = json.loads(response["body"].read())
            return payload["content"][0]["text"].strip()

        if "mistral." in self.model_id:
            body = json.dumps(
                {
                    "prompt": prompt,
                    "max_tokens": settings.max_tokens,
                    "temperature": settings.temperature,
                    "top_p": 0.9,
                }
            )
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            payload = json.loads(response["body"].read())
            return payload["outputs"][0]["text"].strip()

        raise ValueError(f"Unsupported LLM model: {self.model_id}")
