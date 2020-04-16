import subprocess
from unittest.mock import Mock, call, patch

import pytest

import encrypt
from encrypt import _main, _parse_arguments
from tests.conftest import assert_files_changes, assert_file_type


def _encrypt_with_password(gpg_command):
    test_options = ["--batch", "--passphrase", "asdf1234"]
    gpg_command = gpg_command[0:1] + test_options + gpg_command[1:]
    subprocess.run(gpg_command, check=True)


@pytest.fixture(scope="module", autouse=True)
def mock_encrypt():
    with patch("encrypt._encrypt", new=_encrypt_with_password) as _fixture:
        yield _fixture


def test_parse_input_not_exists(files):
    with pytest.raises(SystemExit):
        _parse_arguments("asdf")


def test_parse_empty_args(files):
    with pytest.raises(SystemExit):
        _parse_arguments("", "")


def test_parse_output_exists(files):
    with pytest.raises(SystemExit):
        _parse_arguments("file1", "file2")


def test_parse_output_not_specified(files):
    input_file, output_file = _parse_arguments("file1")
    assert output_file == "file1" + ".gpg"


def test_parse_input_dir(files):
    input_file, output_file = _parse_arguments("dir2/")
    assert input_file == "dir2"
    assert output_file == "dir2.gpg"


def test_main(files):
    _main("file1", "file1.gpg")
    files["f_root"].append("file1.gpg")
    assert_files_changes(files)
    assert_file_type("file1.gpg", "GPG symmetrically encrypted data")


def test_main_different_path(files):
    _main("file1", "dir2/asdf.gpg")
    files["f_dir2"].append("asdf.gpg")
    assert_files_changes(files)


def test_main_dir(files):
    _main("dir2", "dir2.gpg")
    files["f_root"].append("dir2.gpg")
    assert_files_changes(files)
    assert_file_type("dir2.gpg", "GPG symmetrically encrypted data")



def test_main_dir_different_path(files):
    _main("dir2", "dir1/dir2.gpg")
    files["f_dir1"].append("dir2.gpg")
    assert_files_changes(files)


def test_run(files):
    file = "file1"
    mock_parent = Mock()
    with patch(
        "encrypt._parse_arguments", return_value=(file, file + ".gpg",)
    ) as mock_parse:
        with patch("encrypt._main") as mock_main:
            mock_parent.attach_mock(mock_parse, "mock_parse")
            mock_parent.attach_mock(mock_main, "mock_main")
            encrypt.run(file)
            """Check if method 1 is called before method 2"""
            mock_parent.assert_has_calls(
                [call.mock_parse(file, ""), call.mock_main(file, file + ".gpg")]
            )
