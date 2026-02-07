"""
Configuration example for AWS Bedrock Knowledge Base with Nova Models

Before running, make sure you have:
1. Created a Knowledge Base in AWS Bedrock
2. Configured AWS credentials (via AWS CLI or environment variables)
3. Set appropriate IAM permissions for Bedrock access
4. Enabled Nova models in your AWS account
"""

# Your Bedrock Knowledge Base configuration
CONFIG = {
    # Replace with your actual Knowledge Base ID
    "KNOWLEDGE_BASE_ID": "3GAFZTOGU9",
    
    # AWS Region where your Knowledge Base is deployed
    "REGION": "us-east-1",
    
    # Optional: AWS profile name if using named profiles
    "PROFILE_NAME": None,  # or "my-profile"
    
    # AWS Nova model options
    "MODEL_ID": "amazon.nova-pro-v1:0",  # Default model
    
    # Default retrieval settings
    "MAX_RESULTS": 5,
}

# AWS Nova Model Options
NOVA_MODELS = {
    # Nova Micro - Fastest and most cost-effective for simple tasks
    "micro": "amazon.nova-micro-v1:0",
    
    # Nova Lite - Balanced performance and cost, supports text and images
    "lite": "amazon.nova-lite-v1:0",
    
    # Nova Pro - Most capable, supports text, images, and video
    "pro": "amazon.nova-pro-v1:0",
}

# Model comparison guide:
MODEL_COMPARISON = """
Nova Micro:
- Best for: Simple Q&A, text classification, basic summarization
- Speed: Fastest
- Cost: Lowest
- Capabilities: Text only

Nova Lite:
- Best for: General purpose RAG, document analysis, multi-turn conversations
- Speed: Fast
- Cost: Low-Medium
- Capabilities: Text and image understanding

Nova Pro:
- Best for: Complex reasoning, detailed analysis, multi-modal tasks
- Speed: Moderate
- Cost: Medium-High
- Capabilities: Text, image, and video understanding
"""

# Required IAM permissions:
REQUIRED_PERMISSIONS = [
    "bedrock:Retrieve",
    "bedrock:RetrieveAndGenerate",
    "bedrock:InvokeModel",
]