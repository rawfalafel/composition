from typing import List
import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

def read_ignore_patterns(root_directory: str) -> PathSpec:
    """Read ignore patterns from .compositionignore file and return a PathSpec object."""
    ignore_file_path = os.path.join(root_directory, '.compositionignore')
    
    # Fallback to an empty PathSpec object if any exception occurs
    try:
        if os.path.exists(ignore_file_path):
            with open(ignore_file_path, 'r') as f:
                lines = f.read().splitlines()
                cleaned_lines = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
                if cleaned_lines:
                    return PathSpec.from_lines(GitWildMatchPattern, cleaned_lines)
    except Exception as e:
        print(f"An error occurred while reading .compositionignore: {e}")
    
    return PathSpec.from_lines(GitWildMatchPattern, [])

def list_files_in_directory(root_directory: str) -> List[str]:
    """List files in the directory considering the ignore patterns."""
    file_list = []
    ignore_spec = read_ignore_patterns(root_directory)
    
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            absolute_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(absolute_path, root_directory)
            
            # Use the PathSpec object to determine if a file should be ignored
            if not ignore_spec.match_file(relative_path):
                file_list.append(relative_path)
                
    return file_list

def save_file_list(file_list: List[str], root_directory: str) -> None:
    """Saves the list of files to a .composition/watchfiles file in the given root directory."""
    # Construct the full path to the watchfiles
    watchfile_path = os.path.join(root_directory, '.composition', 'watchfiles')

    # Ensure the .composition directory exists
    os.makedirs(os.path.dirname(watchfile_path), exist_ok=True)

    try:
        # Write each filename to the watchfiles, separated by newlines
        with open(watchfile_path, 'w') as f:
            f.write('\n'.join(file_list))
    except IOError as e:
        print(f"An I/O error occurred while saving the file list: {e}")
    except Exception as e:
        print(f"An unspecified error occurred: {e}")

