from typing import List, Dict

from backend.project_types import LogMessage, get_log_message_content


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
        role = "assistant" if message.source == "agent" else "user"
        content = get_log_message_content(message.message)
        converted_messages.append({"role": role, "content": content})
    return converted_messages
