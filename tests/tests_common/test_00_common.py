import os

from ansys.aedt.toolkits.motor.common_settings import CommonSettings
from tests.tests_aedt.conftest import BasisTest


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.common_settings = CommonSettings(working_dir=self.local_scratch.path)
        self.aedt_json = os.path.join(
            self.common_settings.config_settings_path, "aedt_parameters.json"
        )
        self.motorcad_json = os.path.join(
            self.common_settings.config_settings_path, "motorcad_parameters.json"
        )

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_json_files_exist(self):
        assert os.path.exists(self.common_settings.config_settings_path)
        assert os.path.exists(self.aedt_json)
        assert os.path.exists(self.motorcad_json)

    def test_02_json_content(self):
        aedt_json = self.common_settings.load_json(self.aedt_json)
        aedt_json["AEDT"]["AEDTVersion"] = "2023.1"
        assert aedt_json["AEDT"]["AEDTVersion"] == "2023.1"
        aedt_json["Materials"]["Windings"]["Temp"] = "130"
        assert aedt_json["Materials"]["Windings"]["Temp"] == "130"
        aedt_json["Mesh"]["Windings"]["Length"] = "1"
        assert aedt_json["Mesh"]["Windings"]["Length"] == "1"
        self.common_settings.update_dict_props(
            aedt_json, "Reports", {"Expression": "CoreLoss", "PlotName": "Losses"}
        )
        assert isinstance(aedt_json["Reports"], list)
        assert len(aedt_json["Reports"]) == 2
        assert aedt_json["Reports"][0]["Expression"] == "SolidLoss"
        assert aedt_json["Reports"][1]["Expression"] == "CoreLoss"
        self.common_settings.update_dict_props(
            aedt_json, "Reports", {"Expression": "CoreLoss", "PlotName": "Losses"}, remove=True
        )
        assert isinstance(aedt_json["Reports"], list)
        assert len(aedt_json["Reports"]) == 1
        assert not self.common_settings.update_dict_props(aedt_json, "Invalid", True, remove=True)
