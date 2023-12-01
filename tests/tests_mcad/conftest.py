"""
"""
import json
import os
from pathlib import Path
import shutil
import time

from pyaedt import generate_unique_folder_name
from pyaedt import settings
import pytest

from ansys.aedt.toolkits.motor.backend.api import Toolkit

PROJECT_NAME = "e9_built"
DESIGN_NAME = "Motor-CAD e9"

# Initialize default desktop configuration
default_version = "2023.1"
config = {
    "desktop_version": default_version,
    "non_graphical": True,
    "use_grpc": True,
}

# Check for the local config file, override defaults if found
local_path = os.path.dirname(os.path.realpath(__file__))
local_config_file = os.path.join(local_path, "local_config.json")
if os.path.exists(local_config_file):
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

# Update pyaedt settings
settings.enable_error_handler = False
settings.enable_desktop_logs = False
settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["non_graphical"]


@pytest.fixture
def basic_toolkit():
    """Initialize the toolkit."""
    toolkit = Toolkit()

    yield toolkit

    toolkit.close_motorcad()


@pytest.fixture(scope="class")
def toolkit_mcad():
    src_folder = os.path.join(Path(__file__).parents[1], "input_data")
    temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))
    mot_file = os.path.join(temp_folder, "e9_built.mot")

    toolkit = Toolkit()
    toolkit.set_properties({"MotorCAD_filepath": mot_file})

    return toolkit


@pytest.fixture
def toolkit():
    """Initialize the toolkit with a temporary MOT file.
    The AEDT file is created at the beginning of each test and removed after each test.
    """
    src_folder = os.path.join(Path(__file__).parents[1], "input_data")
    temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))
    mot_file = os.path.join(temp_folder, "e9_built.mot")
    toolkit = Toolkit()
    toolkit.set_properties({"MotorCAD_filepath": mot_file})

    yield toolkit

    toolkit.close_motorcad()


def wait_toolkit(toolkit):
    """Wait for the backend to be running."""
    response = toolkit.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = toolkit.get_thread_status()
