import argparse

from .embed_chunks import embed_chunks
from .chunk_files import process_chunkfiles
from .csv import write_to_csv
from .read_files import read_from_watchlist
from .watchfiles import list_files_in_directory


def main():
    parser = argparse.ArgumentParser(
        description="Generate and update embeddings from a root directory."
    )
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="Root directory containing the .composition/watchfiles and where .composition/embeddings.csv will be saved.",
    )

    args = parser.parse_args()
    root_directory = args.dir

    try:
        print("Listing files in watchlist...")
        watchlist = list_files_in_directory(root_directory)

        # Step 1: Read files listed in watchlist
        print("Reading files listed in watchlist...")
        file_data = read_from_watchlist(watchlist, root_directory)

        # Step 2: Process and chunk the files
        print("Processing and chunking files...")
        processed_files = process_chunkfiles(file_data)

        # Step 3: Calculate embeddings for each chunk
        print("Calculating embeddings for each chunk...")
        processed_chunks = embed_chunks(processed_files)

        # Step 4: Write the processed chunks and their embeddings to a CSV file
        print("Writing processed chunks and their embeddings to CSV...")
        write_to_csv_result = write_to_csv(processed_chunks, root_directory)
        if write_to_csv_result is not None:
            print(f"An error occurred while writing to CSV: {write_to_csv_result}")
        else:
            print("Successfully wrote to CSV.")

    except Exception as e:
        print(f"An error occurred: {e}")
