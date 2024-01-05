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

# from pathlib import Path
# import shutil
import time

# from pyaedt import generate_unique_folder_name
from pyaedt import settings
import pytest

from ansys.aedt.toolkits.motor.backend.api import Toolkit
from ansys.aedt.toolkits.motor.backend.common.toolkit import ToolkitThreadStatus

# Constants
PROJECT_NAME = "e9_eMobility_IPM__ANSYSEM_3D"
DESIGN_NAME = "Motor-CAD e9"
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

# test_folder = "unit_test" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
# if not os.path.exists(scratch_path):
#     try:
#         os.makedirs(scratch_path)
#     except:
#         pass

# logger = pyaedt_logger
# local_scratch = Scratch(scratch_path)
# toolkit = Toolkit()

# class BasisTest(object):
#     def my_setup(self):
#         self.local_scratch = local_scratch
#         self._main = sys.modules["__main__"]
#         self.toolkit = toolkit

#     def my_teardown(self):
#         self.toolkit.connect_aedt()
#         if self.toolkit.desktop:
#             try:
#                 oDesktop = self._main.oDesktop
#                 proj_list = oDesktop.GetProjectList()
#             except Exception as e:
#                 oDesktop = None
#                 proj_list = []
#             if oDesktop and not settings.non_graphical:
#                 oDesktop.ClearMessages("", "", 3)
#             for proj in proj_list:
#                 oDesktop.CloseProject(proj)
#             self.toolkit.release_aedt(True, True)
#             del self.toolkit.desktop

#         logger.remove_all_project_file_logger()
#         shutil.rmtree(self.local_scratch.path, ignore_errors=True)

#     def teardown_method(self):
#         """
#         Could be redefined
#         """
#         pass

#     def setup_method(self):
#         """
#         Could be redefined
#         """
#         pass


@pytest.fixture(scope="class")
def toolkit(common_temp_dir):
    """Initialize the toolkit with a temporary AEDT file.
    The AEDT file is created at the beginning of each test and removed after each test.
    """
    # src_folder = os.path.join(Path(__file__).parents[1], "input_data")
    # temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))
    # aedt_file = os.path.join(temp_folder, f"{PROJECT_NAME}.aedt")
    # aedt_file = os.path.join(common_temp_dir, f"{PROJECT_NAME}.aedt")
    # src = os.path.join(Path(__file__).parents[1], "input_data", f"{PROJECT_NAME}.aedt")
    # aedt_file = shutil.copy(src, os.path.join(common_temp_dir, "input_data"))
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
    wait_toolkit(toolkit)

    yield toolkit

    toolkit.release_aedt(True, True)
    # shutil.rmtree(temp_folder, ignore_errors=True)


def wait_toolkit(toolkit):
    """Wait for the toolkit thread to be idle and ready to accept new task."""
    status = toolkit.get_thread_status()
    while status == ToolkitThreadStatus.BUSY:
        time.sleep(1)
        status = toolkit.get_thread_status()


# @pytest.fixture(scope="session", autouse=True)
# def desktop_init():
#     properties = {
#         "aedt_version": config["desktop_version"],
#         "non_graphical": config["non_graphical"],
#         "use_grpc": config["use_grpc"]
#     }
#     toolkit.set_properties(properties)
#     toolkit.launch_aedt()
#     status = toolkit.get_thread_status()
#     while status == ToolkitThreadStatus.BUSY:
#         time.sleep(1)
#         status = toolkit.get_thread_status()
#     yield
