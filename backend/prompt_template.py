from backend.project_types import TextMessageWithContext


def read_template(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def fill_template(template: str, user_query: str, retrieved_context: str) -> str:
    print(template)
    return template.format(message=user_query, context=retrieved_context)


def extract_context(text_message_with_context: TextMessageWithContext) -> str:
    context_strs = []
    for record in text_message_with_context.context:
        context_strs.append(
            f"File: {record.file_path}, Chunk: {record.chunk_index}\nContent: {record.content}"
        )
    return "\n".join(context_strs)
