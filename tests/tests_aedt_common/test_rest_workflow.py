# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

import os
import time

from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus
import pytest
import requests

from ansys.aedt.toolkits.magnet_segmentation.backend.models import Properties
from tests.tests_aedt_common.conftest import config

pytestmark = [pytest.mark.aedt_common]


class TestRESTWorkflow:
    @classmethod
    def setup_class(cls):
        cls.test_config = config
        cls.url = f"http://{config['url']}:{config['port']}"

    def test_00_get_status(self):
        response = requests.get(self.url + "/status")
        assert response.ok
        assert response.json() == ToolkitThreadStatus.IDLE.value

    def test_01_get_properties(self):
        expected_properties = Properties()
        # NOTE: conftest.py sets non_graphical to True
        expected_properties.aedt_version = config["aedt_version"]
        expected_properties.non_graphical = config["non_graphical"]
        expected_properties.use_grpc = config["use_grpc"]
        response = requests.get(self.url + "/properties")
        data = response.json()

        # NOTE: removing specific data that cannot be reproduced at each test:
        # - log_file is overridden when temp directory is created
        # - selected_process is randomly generated since grpc is used by default
        assert response.ok
        assert expected_properties.log_file in data["log_file"]
        data.pop("log_file")
        data.pop("selected_process")
        assert data == expected_properties.model_dump(exclude=["log_file", "selected_process"])

    def test_02_set_properties(self):
        new_properties = {
            "aedt_version": self.test_config["aedt_version"],
            "non_graphical": self.test_config["non_graphical"],
        }
        response = requests.put(self.url + "/properties", json=new_properties)
        assert response.ok

    def test_03_installed_versions(self):
        response = requests.get(self.url + "/installed_versions")
        assert response.ok

    def test_04_aedt_sessions(self):
        response = requests.get(self.url + "/aedt_sessions")
        assert response.ok
        assert isinstance(response.json(), dict)
        assert response.json()

    def test_05_connect_design(self):
        response = requests.post(self.url + "/connect_design", json={"aedtapp": "Icepak"})
        assert response.ok

    def test_06_save_project(self, common_temp_dir):
        file_name = os.path.join(common_temp_dir, "Test.aedt")
        response = requests.post(self.url + "/save_project", json=file_name)
        assert response.ok
        response = requests.get(self.url + "/status")
        while response.json() != ToolkitThreadStatus.IDLE.value:
            time.sleep(1)
            response = requests.get(self.url + "/status")

    def test_07_get_design_names(self):
        response = requests.get(self.url + "/design_names")
        assert response.ok
        assert len(response.json()) == 1
        response = requests.get(self.url + "/status")
        while response.json() != ToolkitThreadStatus.IDLE.value:
            time.sleep(1)
            response = requests.get(self.url + "/status")
