import boto3
import json
from typing import Dict, Any, Iterator

class BedrockAgentClient:
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize Bedrock Agent Runtime client"""
        self.client = boto3.client(
            'bedrock-agent-runtime',
            region_name=region_name
        )
    
    def invoke_agent(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        input_text: str,
        enable_trace: bool = False,
        session_state: Dict[str, Any] = None
    ) -> Iterator[Dict[str, Any]]:
        """
        Invoke a Bedrock Agent and stream the response
        
        Args:
            agent_id: The unique identifier of the agent
            agent_alias_id: The alias ID (use 'TSTALIASID' for draft)
            session_id: Unique session identifier
            input_text: User's input/question
            enable_trace: Whether to enable trace for debugging
            session_state: Optional session state to maintain context
        """
        request_params = {
            'agentId': agent_id,
            'agentAliasId': agent_alias_id,
            'sessionId': session_id,
            'inputText': input_text,
            'enableTrace': enable_trace
        }
        
        if session_state:
            request_params['sessionState'] = session_state
        
        response = self.client.invoke_agent(**request_params)
        
        # Stream the response
        for event in response['completion']:
            yield event
    
    def get_complete_response(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        input_text: str
    ) -> str:
        """Get the complete text response from the agent"""
        full_response = ""
        
        for event in self.invoke_agent(agent_id, agent_alias_id, session_id, input_text):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    full_response += chunk['bytes'].decode('utf-8')
        
        return full_response
    
    def invoke_agent_with_trace(
        self,
        agent_id: str,
        agent_alias_id: str,
        session_id: str,
        input_text: str
    ) -> Dict[str, Any]:
        """Invoke agent and capture both response and trace"""
        response_text = ""
        trace_events = []
        
        for event in self.invoke_agent(
            agent_id, agent_alias_id, session_id, input_text, enable_trace=True
        ):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    response_text += chunk['bytes'].decode('utf-8')
            
            if 'trace' in event:
                trace_events.append(event['trace'])
        
        return {
            'response': response_text,
            'trace': trace_events
        }