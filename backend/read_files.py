from typing import List, Tuple, Union
import os

from backend.project import get_watchfiles_path


def get_watchlist_paths(root_directory: str) -> List[str]:
    """
    Read the `.composition/watchfiles` and return a list of relative file paths.

    Parameters:
        root_directory (str): The root directory containing `.composition/watchfiles`.

    Returns:
        List[str]: A list of relative file paths found in `.composition/watchfiles`.

    Raises:
        FileNotFoundError: Raised when `.composition/watchfiles` is not found.
    """
    watchfile_path = get_watchfiles_path(root_directory)

    try:
        with open(watchfile_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(
            f".composition/watchfiles not found in {root_directory}"
        )


def read_from_watchlist(
    relative_paths: List[str], root_directory: str
) -> List[Tuple[str, Union[str, Exception]]]:
    """
    Read the files based on the list of relative paths and return their data.

    Parameters:
        relative_paths (List[str]): The relative file paths to read.
        root_directory (str): The root directory.

    Returns:
        List[Tuple[str, Union[str, Exception]]]: A list of tuples containing the relative file path and its content or exception.
    """
    files_data: List[Tuple[str, Union[str, Exception]]] = []

    for relative_path in relative_paths:
        full_path = os.path.join(root_directory, relative_path)

        try:
            with open(full_path, "r", encoding="utf-8") as file:
                content = file.read()
            files_data.append((relative_path, content))
        except FileNotFoundError:
            files_data.append(
                (relative_path, FileNotFoundError(f"File {relative_path} not found"))
            )
        except Exception as e:
            files_data.append((relative_path, e))

    return files_data
