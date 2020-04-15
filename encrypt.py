#!/usr/bin/env python3

import argparse
import subprocess

from _utils.utils import *


def _parse_arguments(input_file, output_file=""):
    """
    Parse arguments:
    - Input file: must be file or directory
    - Output file: optional, will be deducted from input
    Returns validated arguments
    """
    input_file = input_file.rstrip("/")
    output_file = output_file.rstrip("/")

    if not output_file:
        output_file = input_file + ".gpg"
    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    if not os.path.exists(input_file):
        fail(f"Input file '{input_file}' does not exist")
    return input_file, output_file


def _encrypt(gpg_command):
    subprocess.run(gpg_command, check=True)


def _main(input_file, output_file):
    """
    - If the input file is a dir, create a tmp archive 
    - Encrypt
    - If a tmp archive was created, remove it.
    """
    input_file_is_dir = os.path.isdir(input_file)
    if input_file_is_dir:
        tmp_tar = get_unique_tmpfile(input_file, ".tar")
        tar_command = [
            "tar",
            "--keep-old-files",
            "--create",
            "--file",
            tmp_tar,
            input_file,
        ]
        info(f"Archiving directory... ({tmp_tar})")
        try:
            subprocess.run(tar_command, check=True)
        except subprocess.CalledProcessError as ex:
            fail("Archive failed", ex)
        input_file = tmp_tar

    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    gpg_command = ["gpg", "--symmetric", "--output", output_file, input_file]
    info(f"Encrypting...")
    try:
        _encrypt(gpg_command)
    except subprocess.CalledProcessError as ex:
        fail("Encryption failed", ex)
    ok(f"Encryption succeeded: {output_file}")

    if input_file_is_dir:
        try:
            os.remove(tmp_tar)
        except OSError as ex:
            fail(f"Failed to remove archive", ex)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file", nargs="?", default="")
    args = parser.parse_args()
    run(args.input_file, args.output_file)
