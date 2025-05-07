# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

from ansys.aedt.core import settings
import pytest

from ansys.aedt.toolkits.magnet_segmentation.backend.api import ToolkitBackend

# Constants
PROJECT_NAME = "e9_eMobility_IPM_3D"
PROJECT_NAME_SEGMENTED = "e9_eMobility_IPM_3D_segmented"
PROJECT_NAME_SKEWED = "e9_eMobility_IPM_3D_skewed"
PROJECT_NAME_ANALYZED = "e9_eMobility_IPM_3D_analyzed"
DESIGN_NAME = "e9"
AEDT_DEFAULT_VERSION = "2025.1"

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
settings.use_grpc_api = config["use_grpc"]
settings.non_graphical = config["non_graphical"]


@pytest.fixture(scope="class")
def aedtapp(common_temp_dir):
    aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME}.aedt")
    toolkit = ToolkitBackend()
    new_properties = {
        "aedt_version": config["desktop_version"],
        "non_graphical": config["non_graphical"],
        "active_project": aedt_file,
        "active_design": DESIGN_NAME,
        "design_list": {PROJECT_NAME: [DESIGN_NAME]},
        "use_grpc": config["use_grpc"],
    }
    toolkit.set_properties(new_properties)
    toolkit.launch_aedt()
    toolkit.open_project(aedt_file)
    toolkit.connect_design("Maxwell3D")
    toolkit.wait_to_be_idle()

    yield toolkit

    toolkit.release_aedt(True, True)


@pytest.fixture(scope="class")
def aedtapp_segmented(common_temp_dir):
    aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME_SEGMENTED}.aedt")
    toolkit = ToolkitBackend()
    new_properties = {
        "aedt_version": config["desktop_version"],
        "non_graphical": config["non_graphical"],
        "active_project": aedt_file,
        "active_design": DESIGN_NAME,
        "design_list": {PROJECT_NAME_SEGMENTED: [DESIGN_NAME]},
        "use_grpc": config["use_grpc"],
    }
    toolkit.set_properties(new_properties)
    toolkit.launch_aedt()
    toolkit.open_project(aedt_file)
    toolkit.connect_design("Maxwell3D")
    toolkit.wait_to_be_idle()

    yield toolkit

    toolkit.release_aedt(True, True)


@pytest.fixture(scope="class")
def aedtapp_skewed(common_temp_dir):
    aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME_SKEWED}.aedt")
    toolkit = ToolkitBackend()
    new_properties = {
        "aedt_version": config["desktop_version"],
        "non_graphical": config["non_graphical"],
        "active_project": aedt_file,
        "active_design": DESIGN_NAME,
        "design_list": {PROJECT_NAME_SKEWED: [DESIGN_NAME]},
        "use_grpc": config["use_grpc"],
    }
    toolkit.set_properties(new_properties)
    toolkit.launch_aedt()
    toolkit.open_project(aedt_file)
    toolkit.connect_design("Maxwell3D")
    toolkit.wait_to_be_idle()

    yield toolkit

    toolkit.release_aedt(True, True)


@pytest.fixture(scope="class")
def aedtapp_analyzed(common_temp_dir):
    aedt_file = os.path.join(common_temp_dir, "input_data", f"{PROJECT_NAME_ANALYZED}.aedtz")
    toolkit = ToolkitBackend()
    new_properties = {
        "aedt_version": config["desktop_version"],
        "non_graphical": config["non_graphical"],
        "active_project": aedt_file,
        "active_design": DESIGN_NAME,
        "design_list": {PROJECT_NAME_ANALYZED: [DESIGN_NAME]},
        "use_grpc": config["use_grpc"],
    }
    toolkit.set_properties(new_properties)
    toolkit.launch_aedt()
    toolkit.open_project(aedt_file)
    toolkit.connect_design("Maxwell3D")
    toolkit.wait_to_be_idle()

    yield toolkit

    toolkit.release_aedt(True, True)
