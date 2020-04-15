import os
import shutil
import tempfile

import pytest


@pytest.fixture
def files():
    """
    Create and yield tmp dir with some files.
    After yield, check that the dir contains the files (and some extra if
     a test added them in files_in_dir) and that the original files haven't changed.
    """
    files_in_dir = ["file1", "file2", "dir1"]
    files_in_subdir = ["file1", "file2"]
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    for fname in files_in_dir:
        if fname.startswith("file"):
            with open(fname, "w") as file:
                file.write(fname)
        else:
            os.mkdir(fname)
            for subfname in files_in_subdir:
                subpath = fname + "/" + subfname
                with open(subpath, "w") as file:
                    file.write(subfname)
    original_files = list(files_in_dir)
    yield files_in_dir
    assert set(os.listdir(newpath)) == set(files_in_dir)
    for fname in original_files:
        if fname.startswith("file"):
            with open(fname, "r") as file:
                assert file.read() == fname
        else:
            assert set(os.listdir(fname)) == set(files_in_subdir)
    os.chdir(old_cwd)
    shutil.rmtree(newpath)

