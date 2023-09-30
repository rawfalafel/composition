import pytest
from unittest.mock import patch, mock_open
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern
from backend.embedding.watchfiles import list_files_in_directory, read_ignore_patterns


# Test read_ignore_patterns function
def test_read_ignore_patterns():
    with patch(
        "builtins.open", mock_open(read_data="# Comment\n\n*.txt\n/dir/")
    ), patch("os.path.exists", return_value=True):
        patterns = read_ignore_patterns("root")
        assert isinstance(patterns, PathSpec)
        assert patterns.match_file("test.txt")
        assert patterns.match_file("dir/some_file")
        assert not patterns.match_file("test.pdf")


# Test list_files_in_directory function
def test_list_files_in_directory():
    mock_files = [
        ["root", ["dir1"], [".compositionignore", "file1.pdf", "text1.txt"]],
        ["root/dir1", [], ["file2.pdf"]],
    ]

    def mock_os_walk(root_directory):
        for dirpath, _, filenames in mock_files:
            yield dirpath, [], filenames

    with patch("os.walk", mock_os_walk), patch(
        "backend.watchfiles.read_ignore_patterns",
        return_value=PathSpec.from_lines(GitWildMatchPattern, ["*.txt"]),
    ):
        result = list_files_in_directory("root")
        assert result == [".compositionignore", "file1.pdf", "dir1/file2.pdf"]
