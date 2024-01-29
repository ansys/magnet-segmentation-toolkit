"""
AEDT Motor Test Configuration Module
------------------------------------

Description
===========
This module contains the configuration and fixture for the pytest-based tests for AEDT.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.1",
  "non_graphical": false,
  "use_grpc": true
}

"""

import json
import os

# from pyaedt import generate_unique_folder_name
from pyaedt import settings
import pytest

from ansys.aedt.toolkits.motor.backend.api import Toolkit

# Constants
PROJECT_NAME = "e9_eMobility_IPM_3D"
DESIGN_NAME = "e9"
AEDT_DEFAULT_VERSION = "2023.2"

config = {
    "desktop_version": AEDT_DEFAULT_VERSION,
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

settings.enable_error_handler = False
settings.enable_desktop_logs = False
settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["non_graphical"]


@pytest.fixture(scope="class")
def toolkit(common_temp_dir):
    """Initialize the toolkit with a temporary AEDT file.
    The AEDT file is created at the beginning of each test and removed after each test.
    """
    aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedt")
    toolkit = Toolkit()
    new_properties = {
        "aedt_version": config["desktop_version"],
        "non_graphical": config["non_graphical"],
        "active_project": aedt_file,
        "use_grpc": config["use_grpc"],
    }
    toolkit.set_properties(new_properties)
    toolkit.launch_aedt()
    toolkit.wait_to_be_idle()

    yield toolkit

    toolkit.release_aedt(True, True)
    # shutil.rmtree(temp_folder, ignore_errors=True)
