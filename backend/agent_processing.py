from typing import List, Dict, Union

from backend.project_types import LogMessage

def convert_messages_format(messages: List[LogMessage]) -> List[Dict[str, str]]:
    """
    Convert a list of messages from one format to another.
    
    Parameters:
        messages (List[Dict]): List of messages with the format { source: <"agent" or "user">, message: { text: <string> }}.
        
    Returns:
        List[Dict]: A list of messages with the format { role: <"assistant" or "user">, content: <string> }.
    """
    converted_messages = []
    for message in messages:
        role = 'assistant' if message.source == 'agent' else 'user'
        content = message.message.text
        converted_messages.append({'role': role, 'content': content})
    return converted_messages
