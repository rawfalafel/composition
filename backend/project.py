import os

COMPOSITION_DIRECTORY = ".composition"
PROJECT_JSON = "project.json"
EMBEDDINGS_CSV = "embeddings.csv"
WATCHFILES = "watchfiles"

def get_project_json_path(root_directory: str):
    return os.path.join(root_directory, COMPOSITION_DIRECTORY, PROJECT_JSON)

def get_embeddings_csv_path(root_directory: str):
    return os.path.join(root_directory, COMPOSITION_DIRECTORY, EMBEDDINGS_CSV)

def get_watchfiles_path(root_directory: str):
    return os.path.join(root_directory, COMPOSITION_DIRECTORY, WATCHFILES)

def get_ignore_path(root_directory: str):
    return os.path.join(root_directory, ".compositionignore")