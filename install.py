#!/usr/bin/env python3
import os
import shutil
import sys


def recursive_chmod(path, mode):
    for dirpath, dirnames, filenames in os.walk(path):
        os.chmod(dirpath, mode)
        for filename in filenames:
            os.chmod(os.path.join(dirpath, filename), mode)


if __name__ == "__main__":
    target = "/usr/local/bin/"
    scripts = ["encrypt.py", "decrypt.py", "compress.py", "extract.py"]
    dirs = ["_utils"]

    for file in scripts:
        path = target + file
        shutil.copy(file, path)
        os.chmod(path, 0o755)
        print("Copied " + file + " to " + path, file=sys.stderr)

    for file in dirs:
        path = target + file
        if os.path.exists(path):
            shutil.rmtree(path)
        shutil.copytree(file, path)
        recursive_chmod(path, 0o755)
        print("Copied " + file + " to " + path, file=sys.stderr)
