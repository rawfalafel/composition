from typing import List

import openai
from backend.embedding_types import EmbeddingRecord
from backend.oai.setup import setup_openai

setup_openai()


def evaluate_context(question: str, context: List[EmbeddingRecord]) -> int:
    # Extract content from each EmbeddingRecord and concatenate
    extracted_content = "\n".join([record.content for record in context])

    # Create a message list to be passed to GPT-4
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Question: {question}"},
        {"role": "user", "content": f"Context: {extracted_content}"},
        {
            "role": "user",
            "content": "Based on the given question and context, please evaluate the relevance and succinctness of the context and give it a score between 1 and 5, where 5 is the highest. Score must be an integer.",
        },
    ]

    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

    score = int(response["choices"][0]["message"]["content"])
    return score
