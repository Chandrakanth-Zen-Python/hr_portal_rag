import uuid
from bedrock_agent_client import BedrockAgentClient

# Initialize client
client = BedrockAgentClient(region_name='us-east-1')

# Configuration
AGENT_ID = '6AX30AKPTC'
AGENT_ALIAS_ID = 'DFHPDQAD7L'  # Use 'TSTALIASID' for draft version
SESSION_ID = str(uuid.uuid4())  # Generate unique session ID

# Example 1: Simple invocation
print("Example 1: Simple invocation")
response = client.get_complete_response(
    agent_id=AGENT_ID,
    agent_alias_id=AGENT_ALIAS_ID,
    session_id=SESSION_ID,
    input_text="What is my order status ORDGT3516745 ?"
)
print(f"Response: {response}\n")

# # Example 2: Streaming response
# print("Example 2: Streaming response")
# for event in client.invoke_agent(
#     agent_id=AGENT_ID,
#     agent_alias_id=AGENT_ALIAS_ID,
#     session_id=SESSION_ID,
#     input_text="Tell me about AWS services"
# ):
#     if 'chunk' in event:
#         chunk = event['chunk']
#         if 'bytes' in chunk:
#             print(chunk['bytes'].decode('utf-8'), end='', flush=True)
# print("\n")

# # Example 3: With trace enabled (for debugging)
# print("Example 3: With trace enabled")
# result = client.invoke_agent_with_trace(
#     agent_id=AGENT_ID,
#     agent_alias_id=AGENT_ALIAS_ID,
#     session_id=SESSION_ID,
#     input_text="Help me find information"
# )
# print(f"Response: {result['response']}")
# print(f"Trace events: {len(result['trace'])} events captured\n")

# # Example 4: With session state
# print("Example 4: With session state")
# session_state = {
#     'sessionAttributes': {
#         'user_preference': 'detailed',
#         'language': 'en'
#     },
#     'promptSessionAttributes': {
#         'context': 'technical_support'
#     }
# }

# for event in client.invoke_agent(
#     agent_id=AGENT_ID,
#     agent_alias_id=AGENT_ALIAS_ID,
#     session_id=SESSION_ID,
#     input_text="Explain this concept",
#     session_state=session_state
# ):
#     if 'chunk' in event:
#         chunk = event['chunk']
#         if 'bytes' in chunk:
#             print(chunk['bytes'].decode('utf-8'), end='', flush=True)