import os
import shutil
import tempfile

import pytest

f_root = ["file1", "file2", "file3", "dir1", "dir2"]
f_dir1 = []
f_dir2 = ["b1", "b2", "dir3"]
f_dir3 = ["c1"]


@pytest.fixture(autouse=True)
def files():
    """
    Create and yield dict with a list of files for each dir
    """
    old_cwd = os.getcwd()
    root = tempfile.mkdtemp()
    os.chdir(root)

    for f in f_root:
        if f.startswith("dir"):
            os.mkdir(f)
        else:
            with open(f, "w") as f_:
                f_.write(f)
    for f in f_dir2:
        full_f = "dir2/" + f
        if f.startswith("dir"):
            os.mkdir(full_f)
        else:
            with open(full_f, "w") as f_:
                f_.write(f)
    for f in f_dir3:
        full_f = "dir2/dir3/" + f
        if f.startswith("dir"):
            os.mkdir(full_f)
        else:
            with open(full_f, "w") as f_:
                f_.write(f)

    all_files = {
        "f_root": list(f_root),
        "f_dir1": list(f_dir1),
        "f_dir2": list(f_dir2),
        "f_dir3": list(f_dir3),
    }
    yield all_files

    os.chdir(old_cwd)
    shutil.rmtree(root)


def assert_files_changes(all_files):
    """
    assert the content of the directories is as expected
    assert that the content of the files is as expected
    """
    assert set(os.listdir(".")) == set(all_files["f_root"])
    assert set(os.listdir("dir1")) == set(all_files["f_dir1"])
    assert set(os.listdir("dir2")) == set(all_files["f_dir2"])
    assert set(os.listdir("dir2/dir3")) == set(all_files["f_dir3"])

    for f in f_root:
        if not f.startswith("dir"):
            with open(f, "r") as f_:
                assert f_.read() == f
    for f in f_dir2:
        full_f = "dir2/" + f
        if not f.startswith("dir"):
            with open(full_f, "r") as f_:
                assert f_.read() == f
    for f in f_dir3:
        full_f = "dir2/dir3/" + f
        if not f.startswith("dir"):
            print(full_f)
            with open(full_f, "r") as f_:
                assert f_.read() == f
