#!/usr/bin/env python3
""""
Copyright 2020 Carles Garcia Cabot (github.com/carles-garcia/encrypt-and-zip)
Released under the GNU GPLv3 (see LICENSE)
""" ""
import argparse
import pathlib
import subprocess

from _utils.utils import *


def _parse_arguments(input_file, output_file=""):
    input_file = input_file.rstrip("/")
    output_file = output_file.rstrip("/")

    if not output_file:
        if input_file.endswith(".zip"):
            output_file = input_file[: -len(".zip")]
        else:
            for extension in TAR_EXTENSIONS:
                if input_file.endswith("." + extension):
                    output_file = input_file[: -(len(extension) + 1)]
        if not output_file:
            fail("Can't deduct output file from input file. Specify an output file")
    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    if not os.path.exists(input_file):
        fail(f"Input file '{input_file}' does not exist")

    return input_file, output_file


def _main(input_file, output_file):
    """
    - Extract in a tmp dir
    - List tmp:
        - If multiple files, rename tmp dir to output file
        - If one file, rename this file to output file and remove tmp dir

    """

    tmp_dir = get_unique_tmpfile(output_file, ".extracted")
    try:
        os.mkdir(tmp_dir)
    except OSError as ex:
        fail("Failed to create temporary directory", ex)
    if input_file.endswith(".zip"):
        check_requirements("unzip")
        command = ["unzip", "-q", input_file, "-d", tmp_dir]
    else:
        check_requirements("tar")
        command = ["tar", "--extract", "--file", input_file, "-C", tmp_dir]
    info(f"Extracting file...: {tmp_dir}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as ex:
        fail("Extraction failed", ex)

    try:
        extracted_file_list = os.listdir(tmp_dir)
    except OSError as error:
        fail("Failed to list temporary directory", error)
    rm_tmp_dir = True
    if len(extracted_file_list) > 1:
        try:
            if os.path.exists(output_file):
                raise OSError(f"Output file '{output_file}' already exists")
            os.rename(tmp_dir, output_file)
            rm_tmp_dir = False
        except OSError as error:
            fail(
                f"Failed to rename extracted file. The file has been extracted in '{tmp_dir}'",
                error,
            )
        ok(f"Extraction succeeded: {output_file}")
    elif len(extracted_file_list) == 1:
        tmp_path = pathlib.Path(tmp_dir) / extracted_file_list[0]
        try:
            if os.path.exists(output_file):
                raise OSError(f"Output file '{output_file}' already exists")
            os.rename(tmp_path, output_file)
        except OSError as error:
            fail(
                f"Failed to rename extracted file. The file has been extracted in '{tmp_dir}'",
                error,
            )
        ok(f"Extraction succeeded: {output_file}")
    else:
        warn("Compressed file was empty")

    if rm_tmp_dir:
        try:
            os.rmdir(tmp_dir)
        except OSError as error:
            fail(f"Failed to remove temporary directory '{tmp_dir}''", error)


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
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file", nargs="?", default="")
    args = parser.parse_args()
    run(args.input_file, args.output_file)
