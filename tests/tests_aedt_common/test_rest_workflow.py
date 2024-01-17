# from dataclasses import asdict
import os
import time

import pytest
import requests

from ansys.aedt.toolkits.motor.backend.common.toolkit import ToolkitThreadStatus

# from ansys.aedt.toolkits.motor.backend.models import AEDTProperties
from ansys.aedt.toolkits.motor.backend.models import Properties
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
        expected_properties.non_graphical = True
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
            "use_grpc": True,
        }

        response = requests.put(self.url + "/properties", json=new_properties)
        assert response.ok

        # Should work as pydantic checking "allows" to convert 1 into True
        new_properties = {"use_grpc": 1}
        response = requests.put(self.url + "/properties", json=new_properties)
        assert response.ok

        # Should not work as pydantic checking "does not allow" to convert 2 into boolean
        new_properties = {"use_grpc": 2}
        response = requests.put(self.url + "/properties", json=new_properties)
        assert not response.ok

        response = requests.put(self.url + "/properties")
        assert not response.ok

    def test_03_installed_versions(self):
        response = requests.get(self.url + "/installed_versions")
        assert response.ok

    def test_04_aedt_sessions(self):
        response = requests.get(self.url + "/aedt_sessions")
        assert response.ok
        assert isinstance(response.json(), list)
        assert response.json()

    def test_05_connect_design(self):
        response = requests.post(self.url + "/connect_design", json={"aedtapp": "Icepak"})
        assert response.ok
        new_properties = {"use_grpc": False}
        response = requests.put(self.url + "/properties", json=new_properties)
        assert response.ok
        response = requests.post(self.url + "/connect_design", json={"aedtapp": "Icepak"})
        assert response.ok
        new_properties = {"use_grpc": True}
        response = requests.put(self.url + "/properties", json=new_properties)
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
