import openai
from typing import List, Tuple
from langchain.docstore.document import Document
from tenacity import retry, stop_after_attempt, wait_random_exponential

from backend.openai import EMBEDDING_MODEL, setup_openai

setup_openai()

BATCH_SIZE = 1000

@retry(wait=wait_random_exponential(multiplier=10), stop=stop_after_attempt(6))
def create_embedding_batch(batch: List[str]) -> List[List[float]]:
    try:
        response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
        
        if len(response["data"]) != len(batch):
            print("Mismatch between number of embeddings and texts.")
            return []
        
        return [e["embedding"] for e in response["data"]]

    except Exception as e:
        print(f"API error: {e}")
        raise  # Re-raise the exception so that Tenacity knows to retry

def embed_chunks(processed_chunkfiles: List[Tuple[str, int, Document]]) -> List[Tuple[str, int, Document, List[float]]]:
    """
    Embeds the contents of each Document object using OpenAI's text-embedding model.
    
    Parameters:
        processed_chunkfiles (List[Tuple[str, int, Document]]): A list of tuples each containing the file path, chunk index, and Document object.
    
    Returns:
        List[Tuple[str, int, Document, List[float]]]: A list of tuples each containing the file path, chunk index, Document object, and its embedding.
    """

    if not processed_chunkfiles:
        return []

    # Initialize output list and batch buffer
    embedded_chunkfiles = []
    batch_buffer = []

    for file_path, chunk_index, doc in processed_chunkfiles:
        page_content = doc.page_content
        batch_buffer.append((file_path, chunk_index, page_content))

        # Check whether to process the batch
        should_process_batch = len(batch_buffer) == BATCH_SIZE or (file_path, chunk_index, doc) == processed_chunkfiles[-1]

        if should_process_batch:
            # Extract texts to be embedded from batch_buffer
            texts_to_embed = [text for _, _, text in batch_buffer]

            # Perform embedding
            embeddings = create_embedding_batch(texts_to_embed)

            # Add embeddings to the output list
            for i, (batch_file_path, batch_chunk_index, _) in enumerate(batch_buffer):
                embedded_chunkfiles.append((batch_file_path, batch_chunk_index, processed_chunkfiles[i][2], embeddings[i]))

            # Clear batch buffer
            batch_buffer.clear()

    return embedded_chunkfiles
