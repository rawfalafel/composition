import argparse
import os
from backend.context_retrieval import retrieve_context
from backend.embedding.csv import read_from_csv
from backend.eval.evaluate_context import evaluate_context

from backend.project import get_evals_directory_path


def read_questions_from_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        questions = content.strip().split("\n")
    return questions


# Main function
def main():
    # Initialize argparse for command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Read and process evaluation questions."
    )

    # Add command-line argument for specifying the root directory
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        help="Root directory containing the .composition/evals where questions are stored.",
    )

    # Parse command-line arguments
    args = parser.parse_args()
    root_directory = args.dir

    # Validate that the root directory has been specified
    if root_directory is None:
        print("Error: Please specify the root directory using the -d option.")
        return

    # Determine the path to the evals directory
    evals_directory_path = get_evals_directory_path(root_directory)

    # Validate that the evals directory exists
    if not os.path.exists(evals_directory_path):
        print(f"Error: The directory {evals_directory_path} does not exist.")
        return

    aggregated_questions = []
    # Read all files in the evals directory
    for file_name in os.listdir(evals_directory_path):
        file_path = os.path.join(evals_directory_path, file_name)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Read questions from each file and split by newline
        questions = read_questions_from_file(file_path)

        # Process questions (you can replace this print statement with actual logic)
        print(f"Questions from {file_name}: {questions}")

        aggregated_questions.extend(questions)

    print(f"Aggregated questions from all files: {aggregated_questions}")

    embeddings = read_from_csv(root_directory)

    aggregated_scores = []
    for question in aggregated_questions:
        (_, context) = retrieve_context(question, embeddings)
        score = evaluate_context(question, context)
        aggregated_scores.append((question, context, score))

        print(f"Question: {question}")
        for record in context:
            print(f"Context: {record.content[:100]}")
        print(f"Score: {score}")
