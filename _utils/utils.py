import os
import sys
from shutil import which


class Colors:
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


TAR_EXTENSIONS = ["tar", "tar.gz", "tgz", "tar.xz", "txz", "tar.bz2", "tbz"]


def info(message):
    print(Colors.OKBLUE + message + Colors.ENDC)


def ok(message):
    print(Colors.OKGREEN + message + Colors.ENDC)


def fail(message, exception=None, exit_code=1):
    """
    Print error message with optional exception AND EXIT
    """
    if exception:
        print(exception, file=sys.stderr)
    print(Colors.FAIL + message + Colors.ENDC, file=sys.stderr)
    sys.exit(exit_code)


def error(message, exception=None):
    """
    Print error message with optional exception
    """
    if exception:
        print(exception, file=sys.stderr)
    print(Colors.FAIL + message + Colors.ENDC, file=sys.stderr)


def warn(message, exception=None):
    if exception:
        print(exception, file=sys.stderr)
    print(Colors.WARNING + message + Colors.ENDC, file=sys.stderr)


def get_unique_tmpfile(file, extension):
    tmp_file = f"{file}{extension}"
    counter = 1
    while os.path.exists(tmp_file):
        tmp_file = f"{file}_{str(counter)}{extension}"
        counter += 1
    return tmp_file


def check_requirements(*args):
    for arg in args:
        if not which(arg):
            fail(
                f"{arg} is required. Check that it's installed, executable and in PATH"
            )
