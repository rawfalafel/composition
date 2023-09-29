from typing import List, Tuple, Union
import os

def read_from_watchlist(root_directory: str) -> List[Tuple[str, Union[str, Exception]]]:
    """
    Generate a list of tuples containing file path and content for each file specified in `.composition/watchfiles`.
    
    Parameters:
        root_directory (str): The root directory containing `.composition/watchfiles`.
        
    Returns:
        List[Tuple[str, Union[str, Exception]]]: A list of tuples. 
            Each tuple contains a relative file path and its content, or an exception if the file could not be read.
    """
    # Initialize an empty list to store tuples of file paths and their content.
    files_data: List[Tuple[str, Union[str, Exception]]] = []
    
    # Construct the path to `.composition/watchfiles` within the given root directory.
    watchfile_path = os.path.join(root_directory, '.composition/watchfiles')
    
    # Attempt to read the `.composition/watchfiles`.
    try:
        with open(watchfile_path, 'r') as f:
            # Read the file and split it by newlines to get the relative paths
            relative_paths = f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f".composition/watchfiles not found in {root_directory}")
    
    # Iterate through each relative path found in `.composition/watchfiles`.
    for relative_path in relative_paths:
        # Construct the full path to each file.
        full_path = os.path.join(root_directory, relative_path)
        
        try:
            # Attempt to read the file content.
            with open(full_path, 'r') as file:
                content = file.read()
            files_data.append((relative_path, content))
        except FileNotFoundError:
            files_data.append((relative_path, FileNotFoundError(f"File {relative_path} not found")))
        except Exception as e:
            files_data.append((relative_path, e))
    
    return files_data

