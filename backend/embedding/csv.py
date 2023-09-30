import csv
import os
from typing import Union, List
from backend.embedding_types import EmbeddingRecord
from backend.project import get_embeddings_csv_path


def write_to_csv(
    embedded_chunkfiles: List[EmbeddingRecord], root_directory: str
) -> Union[None, Exception]:
    """
    Writes the list of EmbeddingRecord objects to a CSV file.

    Parameters:
        embedded_chunkfiles (List[EmbeddingRecord]): The list of EmbeddingRecord objects.
        root_directory (str): The root directory where `.composition/embeddings.csv` will be saved.

    Returns:
        None if successful, otherwise returns an Exception.
    """

    # Build the file path
    file_path = get_embeddings_csv_path(root_directory)

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Write the header
            writer.writerow(
                ["file_path", "chunk_index", "document_content", "embedding"]
            )

            for record in embedded_chunkfiles:
                # Convert embedding list to a string for CSV storage
                embedding_str = ",".join(map(str, record.embedding))
                writer.writerow(
                    [
                        record.file_path,
                        record.chunk_index,
                        record.content,
                        embedding_str,
                    ]
                )  # Assuming 'content' is the relevant field in Document

        return None

    except Exception as e:
        return e


def read_from_csv(root_directory: str) -> List[EmbeddingRecord]:
    """
    Reads the EmbeddingRecord objects from a CSV file.

    Parameters:
        root_directory (str): The root directory where `.composition/embeddings.csv` is saved.

    Returns:
        List[EmbeddingRecord] if successful, otherwise returns an Exception.
    """

    file_path = get_embeddings_csv_path(root_directory)

    # Check if the file exists
    if not os.path.exists(file_path):
        return Exception(f"The file {file_path} does not exist.")

    records = []

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        # Skip header
        next(csv_reader, None)

        for row in csv_reader:
            # Unpack the row
            file_path, chunk_index, document_content, embedding_str = row

            # Convert the embedding back to list of floats
            embedding = list(map(float, embedding_str.split(",")))

            # Create an EmbeddingRecord object and add it to the list
            record = EmbeddingRecord(
                file_path=file_path,
                chunk_index=int(chunk_index),
                content=document_content,
                embedding=embedding,
            )
            records.append(record)

    return records
