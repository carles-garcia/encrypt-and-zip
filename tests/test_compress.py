import os
from unittest.mock import Mock, call, patch

import pytest

import compress
from tests.conftest import assert_files_changes


def test_parse_input_not_exists(files):
    with pytest.raises(SystemExit):
        compress._parse_arguments("asdf")


def test_parse_empty_args(files):
    with pytest.raises(SystemExit):
        compress._parse_arguments("", "")


def test_parse_output_exists(files):
    with pytest.raises(SystemExit):
        compress._parse_arguments("file1", "file2")


def test_parse_output_not_specified(files):
    input_file, output_file = compress._parse_arguments("file1")
    assert output_file == "file1.tgz"
    input_file, output_file = compress._parse_arguments("dir2/")
    assert output_file == "dir2.tgz"


def test_parse_ok(files):
    input_file, output_file = compress._parse_arguments("file1", "newfile")
    assert input_file == "file1"
    assert output_file == "newfile"


def test_main(files):
    compress._main("file1", "file1compressed")
    files["f_root"].append("file1compressed")
    assert_files_changes(files)


def test_main_different_path(files):
    compress._main("file1", "dir2/file1")
    files["f_dir2"].append("file1")
    compress._main("file1", "dir1/file1.tar.xz")
    files["f_dir1"].append("file1.tar.xz")
    assert_files_changes(files)


def test_main_dir(files):
    compress._main("dir2", "dir2.zip")
    compress._main("dir2", "dir2.tar.gz")
    files["f_root"].append("dir2.zip")
    files["f_root"].append("dir2.tar.gz")
    assert_files_changes(files)


def test_main_dir_different_path(files):
    compress._main("dir2", "dir1/dir2.zip")
    compress._main("dir2", "dir1/dir2.tar.gz")
    files["f_dir1"].append("dir2.tar.gz")
    files["f_dir1"].append("dir2.zip")
    assert_files_changes(files)


def test_run(files):
    file = "file1"
    mock_parent = Mock()
    with patch(
        "compress._parse_arguments", return_value=(file, file + ".tgz")
    ) as mock_parse:
        with patch("compress._main") as mock_main:
            mock_parent.attach_mock(mock_parse, "mock_parse")
            mock_parent.attach_mock(mock_main, "mock_main")
            compress.run(file)
            """Check if method 1 is called before method 2"""
            mock_parent.assert_has_calls(
                [call.mock_parse(file, ""), call.mock_main(file, file + ".tgz")]
            )
