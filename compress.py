#!/usr/bin/env python3
""""
Copyright 2020 Carles Garcia Cabot (github.com/carles-garcia/encrypt-and-zip)
Released under the GNU GPLv3 (see LICENSE)
"""""
import argparse
import subprocess

from _utils.utils import *


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file", nargs="?", default="")
    args = parser.parse_args()

    input_file = args.input_file.rstrip("/")
    output_file = args.output_file.rstrip("/")

    if not output_file:
        output_file = input_file + ".tgz"
    if os.path.exists(output_file):
        fail(f"Output file '{output_file}' already exists")
    return input_file, output_file


def main():
    input_file, output_file = parse_arguments()

    output_extension = output_file.split(".")[-1]
    if output_extension == "zip":
        check_requirements("zip")
        command = ["zip", "-q", "--recurse-paths", output_file, input_file]
    else:
        check_requirements("tar")
        if output_extension in [
            "tar",
            "tar.gz",
            "tgz",
            "tar.xz",
            "txz",
            "tar.bz2",
            "tbz",
        ]:
            compression_option = "--auto-compress"
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


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        fail("Unexpected error", ex)
