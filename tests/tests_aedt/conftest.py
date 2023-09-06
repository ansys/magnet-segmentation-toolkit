"""
Unit Test Configuration Module
-------------------------------

Description
===========

This module contains the configuration and fixture for the pytest-based unit tests for pyaedt.

The default configuration can be changed by placing a file called local_config.json in the same
directory as this module. An example of the contents of local_config.json
{
  "desktop_version": "2023.1",
  "non_graphical": false,
  "use_grpc": true
}

"""
import datetime
import json
import os
import shutil
import sys
import tempfile
import time

from pyaedt import settings
from pyaedt.aedt_logger import pyaedt_logger
from pyaedt.generic.filesystem import Scratch
import pytest

from ansys.aedt.toolkits.motor.backend.api import Toolkit

settings.enable_error_handler = False
settings.enable_desktop_logs = False

local_path = os.path.dirname(os.path.realpath(__file__))

test_project_name = "test_antenna"

sys.path.append(local_path)

# Initialize default desktop configuration
default_version = "2023.1"

config = {
    "desktop_version": default_version,
    "non_graphical": True,
    "use_grpc": True,
}

# Check for the local config file, override defaults if found
local_config_file = os.path.join(local_path, "local_config.json")
if os.path.exists(local_config_file):
    with open(local_config_file) as f:
        local_config = json.load(f)
    config.update(local_config)

settings.use_grpc_api = config.get("use_grpc", True)
settings.non_graphical = config["non_graphical"]

test_folder = "unit_test" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
if not os.path.exists(scratch_path):
    try:
        os.makedirs(scratch_path)
    except:
        pass

logger = pyaedt_logger
local_scratch = Scratch(scratch_path)
toolkit = Toolkit()


class BasisTest(object):
    def my_setup(self):
        self.local_scratch = local_scratch
        self._main = sys.modules["__main__"]
        self.toolkit = toolkit

    def my_teardown(self):
        self.toolkit.connect_aedt()
        if self.toolkit.desktop:
            try:
                oDesktop = self._main.oDesktop
                proj_list = oDesktop.GetProjectList()
            except Exception as e:
                oDesktop = None
                proj_list = []
            if oDesktop and not settings.non_graphical:
                oDesktop.ClearMessages("", "", 3)
            for proj in proj_list:
                oDesktop.CloseProject(proj)
            self.toolkit.release_aedt(True, True)
            del self.toolkit.desktop

        logger.remove_all_project_file_logger()
        shutil.rmtree(self.local_scratch.path, ignore_errors=True)

    def teardown_method(self):
        """
        Could be redefined
        """
        pass

    def setup_method(self):
        """
        Could be redefined
        """
        pass


@pytest.fixture(scope="session", autouse=True)
def desktop_init():
    toolkit.set_properties({"aedt_version": config["desktop_version"]})
    toolkit.set_properties({"non_graphical": config["non_graphical"]})
    toolkit.set_properties({"use_grpc": config["use_grpc"]})
    toolkit.launch_aedt()
    response = toolkit.get_thread_status()
    while response[0] == 0:
        time.sleep(1)
        response = toolkit.get_thread_status()
    yield
