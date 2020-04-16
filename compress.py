#!/usr/bin/env python3
""""
Copyright 2020 Carles Garcia Cabot (github.com/carles-garcia/encrypt-and-zip)
Released under the GNU GPLv3 (see LICENSE)
""" ""
import argparse
import subprocess

from _utils.utils import *


def _parse_arguments(input_file, output_file=""):
    input_file = input_file.rstrip("/")
    output_file = output_file

    if not output_file:
        output_file = input_file + ".tgz"
    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    if not os.path.exists(input_file):
        fail(f"Input file '{input_file}' does not exist")

    return input_file, output_file


def _main(input_file, output_file):
    if output_file.endswith(".zip"):
        check_requirements("zip")
        command = ["zip", "-q", "--recurse-paths", output_file, input_file]

    else:
        for extension in TAR_EXTENSIONS:
            if output_file.endswith("." + extension):
                compression_option = "--auto-compress"
                break
        else:
            compression_option = "--gzip"
        command = [
            "tar",
            "--create",
            compression_option,
            "--file",
            output_file,
            input_file,
        ]

    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    info(f"Compressing file... {output_file}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        fail("Compression failed", ex)
    ok("Compression succeeded")


def run(input_file, output_file=""):
    """
    Starting point.
    Raises SystemExit if Exception is caught
    """
    try:
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
