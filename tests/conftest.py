"""
"""
import os
from pathlib import Path
import shutil

import pytest


@pytest.fixture(scope="session")
def common_temp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("test_motor_workflows", numbered=True)
    src_folder = os.path.join(Path(__file__).parent, "input_data")
    shutil.copytree(src_folder, os.path.join(tmp_dir, "input_data"))

    yield tmp_dir

    shutil.rmtree(str(tmp_dir), ignore_errors=True)
