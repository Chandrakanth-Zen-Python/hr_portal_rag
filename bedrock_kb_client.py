import boto3
import json
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class KnowledgeBaseResult:
    """Data class to hold knowledge base query results"""
    content: str
    score: float
    source: str
    metadata: Dict


class BedrockKnowledgeBaseClient:
    """Client for interacting with AWS Bedrock Knowledge Base"""
    
    def __init__(
        self, 
        knowledge_base_id: str,
        region_name: str = "us-east-1",
        profile_name: Optional[str] = None
    ):
        """
        Initialize the Bedrock Knowledge Base client
        
        Args:
            knowledge_base_id: The ID of your Bedrock Knowledge Base
            region_name: AWS region (default: us-east-1)
            profile_name: AWS profile name (optional)
        """
        self.knowledge_base_id = knowledge_base_id
        
        session_kwargs = {"region_name": region_name}
        if profile_name:
            session_kwargs["profile_name"] = profile_name
            
        session = boto3.Session(**session_kwargs)
        
        # Client for Knowledge Base operations
        self.bedrock_agent_runtime = session.client(
            service_name="bedrock-agent-runtime"
        )
        
    def query(
        self,
        query_text: str,
        max_results: int = 5,
        model_arn: Optional[str] = None
    ) -> List[KnowledgeBaseResult]:
        """
        Query the knowledge base
        
        Args:
            query_text: The query string
            max_results: Maximum number of results to return
            model_arn: Optional model ARN for retrieval
            
        Returns:
            List of KnowledgeBaseResult objects
        """
        try:
            # Build retrieval configuration
            retrieval_config = {
                "vectorSearchConfiguration": {
                    "numberOfResults": max_results
                }
            }
            
            response = self.bedrock_agent_runtime.retrieve(
                knowledgeBaseId=self.knowledge_base_id,
                retrievalQuery={
                    "text": query_text
                },
                retrievalConfiguration=retrieval_config
            )
            
            # Parse results
            results = []
            for item in response.get("retrievalResults", []):
                result = KnowledgeBaseResult(
                    content=item.get("content", {}).get("text", ""),
                    score=item.get("score", 0.0),
                    source=item.get("location", {}).get("s3Location", {}).get("uri", "Unknown"),
                    metadata=item.get("metadata", {})
                )
                results.append(result)
                
            return results
            
        except Exception as e:
            print(f"Error querying knowledge base: {str(e)}")
            raise
    
    def retrieve_and_generate(
        self,
        query_text: str,
        model_id: str = "amazon.nova-pro-v1:0",
        max_results: int = 5
    ) -> Dict:
        """
        Retrieve from knowledge base and generate response using AWS Nova model
        
        Args:
            query_text: The query string
            model_id: The Nova model ID to use for generation
                     Options:
                     - amazon.nova-micro-v1:0 (fastest, most cost-effective)
                     - amazon.nova-lite-v1:0 (balanced performance)
                     - amazon.nova-pro-v1:0 (most capable, default)
            max_results: Maximum number of results to retrieve
            
        Returns:
            Dictionary with generated text and citations
        """
        try:
            response = self.bedrock_agent_runtime.retrieve_and_generate(
                input={
                    "text": query_text
                },
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": self.knowledge_base_id,
                        "modelArn": f"arn:aws:bedrock:{self.bedrock_agent_runtime.meta.region_name}::foundation-model/{model_id}",
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {
                                "numberOfResults": max_results
                            }
                        }
                    }
                }
            )
            
            # Extract the generated text and citations
            output = response.get("output", {}).get("text", "")
            citations = response.get("citations", [])
            
            return {
                "generated_text": output,
                "citations": citations,
                "session_id": response.get("sessionId")
            }
            
        except Exception as e:
            print(f"Error in retrieve and generate: {str(e)}")
            raise


def main():
    """Example usage of the Bedrock Knowledge Base client with AWS Nova models"""
    
    # Configuration
    KNOWLEDGE_BASE_ID = "3GAFZTOGU9"  # Replace with your KB ID
    REGION = "us-east-1"  # Replace with your region
    
    # Initialize client
    client = BedrockKnowledgeBaseClient(
        knowledge_base_id=KNOWLEDGE_BASE_ID,
        region_name=REGION
    )
    
    # Example 1: Simple retrieval
    print("=== Example 1: Retrieve documents ===")
    query = "What types of leave are available to employees?"
    results = client.query(query, max_results=3)
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Score: {result.score:.4f}")
        print(f"Source: {result.source}")
        print(f"Content: {result.content[:200]}...")
        print(f"Metadata: {result.metadata}")
    
    # Example 2: Retrieve and generate with Nova Pro (most capable)
    print("\n\n=== Example 2: Retrieve and Generate with Nova Pro ===")
    response = client.retrieve_and_generate(
        query_text="What types of leave are available to employees?",
        model_id="amazon.nova-pro-v1:0",
        max_results=5
    )
    
    print(f"\nGenerated Response:")
    print(response["generated_text"])
    
    print(f"\n\nCitations ({len(response['citations'])}):")
    for i, citation in enumerate(response["citations"], 1):
        print(f"\nCitation {i}:")
        references = citation.get("retrievedReferences", [])
        for ref in references:
            location = ref.get("location", {}).get("s3Location", {}).get("uri", "Unknown")
            content = ref.get("content", {}).get("text", "")
            print(f"  Source: {location}")
            print(f"  Content: {content[:150]}...")
    
    # # Example 3: Using Nova Lite for faster, cost-effective responses
    # print("\n\n=== Example 3: Using Nova Lite ===")
    # response_lite = client.retrieve_and_generate(
    #     query_text="What are the benefits of cloud computing?",
    #     model_id="amazon.nova-lite-v1:0",
    #     max_results=3
    # )
    
    # print(f"\nGenerated Response (Nova Lite):")
    # print(response_lite["generated_text"])
    
    # # Example 4: Using Nova Micro for quick queries
    # print("\n\n=== Example 4: Using Nova Micro (fastest) ===")
    # response_micro = client.retrieve_and_generate(
    #     query_text="Define artificial intelligence in one sentence",
    #     model_id="amazon.nova-micro-v1:0",
    #     max_results=2
    # )
    
    # print(f"\nGenerated Response (Nova Micro):")
    # print(response_micro["generated_text"])


if __name__ == "__main__":
    main()