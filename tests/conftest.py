import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def private_dir(tmp_path_factory):
    basetemp = Path.cwd() / "temp_dir"
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(basetemp)
    basetemp.mkdir(parents=True, exist_ok=True)
    dir = tmp_path_factory.mktemp("private", numbered=False)
    print(dir)
    return dir


@pytest.fixture(scope="session")
def archive_dir(tmp_path_factory):
    basetemp = Path.cwd() / "temp_dir"
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(basetemp)
    basetemp.mkdir(parents=True, exist_ok=True)
    dir = tmp_path_factory.mktemp("archive", numbered=False)
    print(dir)
    return dir
