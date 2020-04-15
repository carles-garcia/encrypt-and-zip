#!/usr/bin/env python3
""""
Copyright 2020 Carles Garcia Cabot (github.com/carles-garcia/encrypt-and-zip)
Released under the GNU GPLv3 (see LICENSE)
"""""
import argparse
import pathlib
import subprocess

from _utils.utils import *


def _is_tar_file(file):
    file_command = ["file", "--mime-type", file]
    try:
        file_subprocess = subprocess.run(
            file_command, stdout=subprocess.PIPE, universal_newlines=True, check=True
        )
    except subprocess.CalledProcessError as ex:
        fail("Failed to check decrypted file type", ex)
    return "application/x-tar" in file_subprocess.stdout


def _parse_arguments(input_file, output_file=""):
    """
    Parse arguments:
    - Input file: must be file
    - Output file: optional, will be deducted from input
    Return validated arguments
    """
    input_file = input_file
    output_file = output_file.rstrip("/")

    if not output_file:
        gpg_extension = ".gpg"
        if input_file.endswith(gpg_extension):
            output_file = input_file[: -len(gpg_extension)]
        else:
            fail("Cannot deduct output file from input file.")
    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    if not os.path.exists(input_file):
        fail(f"Input file '{input_file}' does not exist")
    elif os.path.isdir(input_file):
        fail(f"Input file '{input_file}' is a directory")

    return input_file, output_file


def _decrypt(gpg_command):
    subprocess.run(gpg_command, check=True)


def _main(input_file, output_file):
    """
    - Decrypt.
    - If decrypted file is a tar:
        - Extract contents in a tmp dir.
        - If only one dir was extracted, assume
        it was a dir encrypted with encrypt.py and move it to the output_file.
    """
    tmp_file = get_unique_tmpfile(output_file, ".decrypted")
    gpg_command = ["gpg", "--decrypt", "--output", tmp_file, input_file]
    info(f"Decrypting... ({tmp_file})")
    try:
        _decrypt(gpg_command)
    except subprocess.CalledProcessError as ex:
        fail("Decryption failed", ex)

    if not _is_tar_file(tmp_file):
        try:
            if os.path.isfile(output_file):
                raise OSError(f"Output file '{output_file}' already exists")
            os.rename(tmp_file, output_file)
        except OSError as ex:
            fail("Failed to rename decrypted file", ex)
        else:
            ok(f"Decryption succeeded: {output_file}")
    else:
        output_directory = get_unique_tmpfile(output_file, ".extracted")
        try:
            os.mkdir(output_directory)
        except FileExistsError as ex:
            fail(
                f"Output directory {output_directory} already exists. The decrypted tar is not extracted",
                ex,
            )
        tar_command = [
            "tar",
            "--keep-old-files",
            "--extract",
            "--file",
            tmp_file,
            "-C",
            output_directory,
        ]
        info(f"Extracting... {output_directory}")
        try:
            subprocess.run(tar_command, check=True)
        except subprocess.CalledProcessError as ex:
            fail(f"Extraction failed", ex)

        try:
            os.remove(tmp_file)
        except OSError as ex:
            fail("Failed to remove intermediate archive", ex)

        try:
            extracted_file_list = os.listdir(output_directory)
        except OSError as ex:
            fail("Failed to list directory", ex)
        path = pathlib.Path(output_directory) / extracted_file_list[0]
        if len(extracted_file_list) == 1 and os.path.isdir(path):
            # If there's just 1 directory, we put it outside
            try:
                if os.path.isfile(output_file):
                    raise OSError(f"Output file '{output_file}' already exists")
                os.rename(path, output_file)
            except OSError as ex:
                fail(
                    f"Failed to rename extracted file. The file has been extracted at '{path}'",
                    ex,
                )
            else:
                ok(f"Decryption succeeded {output_file}")
            try:
                os.rmdir(output_directory)
            except OSError as ex:
                fail(f"Failed to remove temporary directory", ex)
        else:
            fail(f"File has been decrypted and extracted at {output_directory}")


def run(input_file, output_file=""):
    """
    Starting point.
    Raises SystemExit if Exception is caught
    """
    try:
        check_requirements("tar", "gpg")
        input_file, output_file = _parse_arguments(input_file, output_file)
        _main(input_file, output_file)
    except Exception as ex:
        fail("Unexpected error", ex)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("input_file")
        parser.add_argument("output_file", nargs="?", default="")
        args = parser.parse_args()
        run(args.input_file, args.output_file)
    except Exception as ex:
        fail(f"Unexpected error", ex)
