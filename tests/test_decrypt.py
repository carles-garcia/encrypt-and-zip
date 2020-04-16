import os
import subprocess
from unittest.mock import Mock, call, patch

import pytest

import decrypt
import encrypt
from tests.conftest import assert_files_changes


def _encrypt_with_password(gpg_command):
    test_options = ["--batch", "--passphrase", "asdf1234"]
    gpg_command = gpg_command[0:1] + test_options + gpg_command[1:]
    subprocess.run(gpg_command, check=True)


def _decrypt_with_password(gpg_command):
    test_options = ["--batch", "--passphrase", "asdf1234"]
    gpg_command = gpg_command[0:1] + test_options + gpg_command[1:]
    subprocess.run(gpg_command, check=True)


@pytest.fixture(scope="module", autouse=True)
def mock_encrypt():
    with patch("encrypt._encrypt", new=_encrypt_with_password) as _fixture:
        yield _fixture


@pytest.fixture(scope="module", autouse=True)
def mock_decrypt():
    with patch("decrypt._decrypt", new=_decrypt_with_password) as _fixture:
        yield _fixture


def test_parse_input_not_exists(files):
    with pytest.raises(SystemExit):
        decrypt._parse_arguments("asdf.gpg")


def test_parse_empty_args(files):
    with pytest.raises(SystemExit):
        decrypt._parse_arguments("", "")


def test_parse_output_exists(files):
    with pytest.raises(SystemExit):
        decrypt._parse_arguments("file1", "file2")


def test_parse_output_not_specified(files):
    encrypt.run("file1", "new.gpg")
    input_file, output_file = decrypt._parse_arguments("new.gpg")
    assert output_file == "new"


def test_parse_input_dir(files):
    with pytest.raises(SystemExit):
        input_file, output_file = decrypt._parse_arguments("dir2/", "asdf")


def test_parse_input_cannot_deduct(files):
    with pytest.raises(SystemExit):
        input_file, output_file = decrypt._parse_arguments("file1")


def test_parse_ok(files):
    input_file, output_file = decrypt._parse_arguments("file1", "newfile")
    assert input_file == "file1"
    assert output_file == "newfile"


def test_main(files):
    encrypt.run("file1")
    decrypt._main("file1.gpg", "file1decrypted")
    with open("file1", "r") as f1, open("file1decrypted", "r") as f2:
        assert f1.read() == f2.read()
    files["f_root"].append("file1.gpg")
    files["f_root"].append("file1decrypted")
    assert_files_changes(files)


def test_main_different_path(files):
    encrypt.run("file1")
    decrypt._main("file1.gpg", "dir2/file1")
    files["f_root"].append("file1.gpg")
    files["f_dir2"].append("file1")
    assert_files_changes(files)


def test_main_dir(files):
    encrypt.run("dir2", "encrypted")
    decrypt._main("encrypted", "dirnew")
    files["f_root"].append("encrypted")
    files["f_root"].append("dirnew")
    assert os.listdir("dirnew") == os.listdir("dir2")
    assert_files_changes(files)


def test_main_dir_different_path(files):
    encrypt.run("dir2")
    decrypt._main("dir2.gpg", "dir1/dir2")
    files["f_root"].append("dir2.gpg")
    files["f_dir1"].append("dir2")
    assert os.listdir("dir1/dir2") == os.listdir("dir2")
    assert_files_changes(files)


def test_run(files):
    file = "file1"
    mock_parent = Mock()
    with patch(
        "decrypt._parse_arguments", return_value=(file + ".gpg", file)
    ) as mock_parse:
        with patch("decrypt._main") as mock_main:
            mock_parent.attach_mock(mock_parse, "mock_parse")
            mock_parent.attach_mock(mock_main, "mock_main")
            decrypt.run(file)
            """Check if method 1 is called before method 2"""
            mock_parent.assert_has_calls(
                [call.mock_parse(file, ""), call.mock_main(file + ".gpg", file)]
            )
