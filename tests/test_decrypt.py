import subprocess

from unittest.mock import Mock, call, patch

import pytest

import encrypt
import decrypt

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
        decrypt._parse_arguments("asdf")


def test_parse_empty_args(files):
    with pytest.raises(SystemExit):
        decrypt._parse_arguments("", "")


def test_parse_output_exists(files):
    with pytest.raises(SystemExit):
        decrypt._parse_arguments(files[0], files[1])


def test_parse_output_not_specified(files):
    file = 'example.gpg'
    input_file, output_file = decrypt._parse_arguments(file)
    assert output_file == 'example'

def test_parse_input_dir(files):
    dir_aux = files[2]
    with pytest.raises(SystemExit):
        decrypt._parse_arguments(dir_aux)


def test_main(files):
    file = files[0]
    _main(file, file + ".gpg")
    files.append(file + ".gpg")


def test_main_dir(files):
    file = files[2]
    _main(file, file + ".gpg")
    files.append(file + ".gpg")


def test_run(files):
    file = files[0]
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
