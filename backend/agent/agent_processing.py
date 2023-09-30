from typing import List, Dict

from backend.project_types import (
    LogMessage,
    TextMessage,
    TextMessageWithContext,
)

from backend.prompt_template import extract_context, fill_template, read_template

template = read_template("backend/templates/basic.md")


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
        content = get_message_content(message)
        print(content)
        converted_messages.append({"role": role, "content": content})
    return converted_messages


def get_message_content(message: LogMessage) -> str:
    if isinstance(message.message, TextMessageWithContext):
        context = extract_context(message.message)
        return fill_template(template, message.message.text, context)

    if isinstance(message.message, TextMessage):
        return message.message.text

    raise Exception("Invalid message type")
