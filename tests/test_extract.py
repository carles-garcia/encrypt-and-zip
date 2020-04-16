import os
import subprocess
from unittest.mock import Mock, call, patch

import pytest

import compress
import extract
from tests.conftest import assert_files_changes


def test_parse_input_not_exists(files):
    with pytest.raises(SystemExit):
        extract._parse_arguments("asdf.tar.gz")


def test_parse_empty_args(files):
    with pytest.raises(SystemExit):
        extract._parse_arguments("", "")


def test_parse_output_exists(files):
    with pytest.raises(SystemExit):
        extract._parse_arguments("file1", "file2")


def test_parse_output_not_specified(files):
    compress.run("file1", "new.zip")
    input_file, output_file = extract._parse_arguments("new.zip")
    assert output_file == "new"
    compress.run("file1", "new.tar.gz")
    input_file, output_file = extract._parse_arguments("new.tar.gz")
    assert output_file == "new"


def test_parse_input_cannot_deduct(files):
    with pytest.raises(SystemExit):
        input_file, output_file = extract._parse_arguments("file1")


def test_parse_ok(files):
    input_file, output_file = extract._parse_arguments("file1", "newfile")
    assert input_file == "file1"
    assert output_file == "newfile"


def test_main(files):
    compress.run("file1")
    extract._main("file1.tgz", "file1extracted")
    with open("file1", "r") as f1, open("file1extracted", "r") as f2:
        assert f1.read() == f2.read()
    files["f_root"].append("file1.tgz")
    files["f_root"].append("file1extracted")
    assert_files_changes(files)


def test_main_different_path(files):
    compress.run("file1")
    extract._main("file1.tgz", "dir2/file1")
    files["f_root"].append("file1.tgz")
    files["f_dir2"].append("file1")
    assert_files_changes(files)


def test_main_dir(files):
    compress.run("dir2", "zipped")
    extract._main("zipped", "dirnew")
    files["f_root"].append("zipped")
    files["f_root"].append("dirnew")
    assert os.listdir("dirnew") == os.listdir("dir2")
    assert_files_changes(files)


def test_main_dir_different_path(files):
    compress.run("dir2")
    extract._main("dir2.tgz", "dir1/dir2")
    files["f_root"].append("dir2.tgz")
    files["f_dir1"].append("dir2")
    assert os.listdir("dir1/dir2") == os.listdir("dir2")
    assert_files_changes(files)


def test_run(files):
    file = "file1"
    mock_parent = Mock()
    with patch(
        "extract._parse_arguments", return_value=(file + ".tgz", file)
    ) as mock_parse:
        with patch("extract._main") as mock_main:
            mock_parent.attach_mock(mock_parse, "mock_parse")
            mock_parent.attach_mock(mock_main, "mock_main")
            extract.run(file)
            """Check if method 1 is called before method 2"""
            mock_parent.assert_has_calls(
                [call.mock_parse(file, ""), call.mock_main(file + ".tgz", file)]
            )
