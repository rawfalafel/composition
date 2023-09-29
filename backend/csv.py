from typing import List, Tuple, Union
from langchain.docstore.document import Document
import csv
import os

from backend.project import COMPOSITION_DIRECTORY, EMBEDDINGS_CSV, get_embeddings_csv_path

def write_to_csv(embedded_chunkfiles: List[Tuple[str, int, Document, List[float]]], root_directory: str) -> Union[None, Exception]:
    """
    Writes the list of tuples from `embed_chunks` to a CSV file.
    
    Parameters:
        embedded_chunkfiles (List[Tuple[str, int, Document, List[float]]]): The list of tuples returned from `embed_chunks`.
        root_directory (str): The root directory where the `.composition/embeddings.csv` will be saved.
        
    Returns:
        None if successful, otherwise returns an Exception.
    """

    # Build the file path
    file_path = get_embeddings_csv_path(root_directory)

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['file_path', 'chunk_index', 'page_content', 'embedding'])
            
            for file_path, chunk_index, doc, embedding in embedded_chunkfiles:
                # Convert embedding list to a string for CSV storage
                embedding_str = ','.join(map(str, embedding))
                writer.writerow([file_path, chunk_index, doc.page_content, embedding_str])
        
        return None

    except Exception as e:
        return e
