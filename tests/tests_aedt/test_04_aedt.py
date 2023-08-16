import os
from pathlib import Path
import shutil

from conftest import BasisTest
from pyaedt import generate_unique_folder_name

test_project_name = "e9_eMobility_IPM__ANSYSEM_3D"
design_name = "Motor-CAD e9"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.toolkit = BasisTest.add_app(self)
        src_folder = os.path.join(Path(__file__).parents[1], "input_data")
        self.temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_1_init_aedt(self):
        aedt_file = os.path.join(self.temp_folder, "e9_eMobility_IPM__ANSYSEM_3D.aedt")
        vbs_file_path = os.path.join(self.temp_folder, "e9_eMobility_IPM_2D_UT.vbs")
        self.toolkit.set_properties({"vbs_file_path": vbs_file_path})
        self.toolkit.set_properties({"active_design": {"Maxwell2d": "Motor-CAD e9_eMobility_IPM_2D"}})
        assert self.toolkit.init_aedt()
        self.toolkit.release_aedt(True, False)
        self.toolkit.set_properties({"active_project": aedt_file})
        assert not self.toolkit.init_aedt()
        self.toolkit.set_properties({"vbs_file_path": ""})
        self.toolkit.set_properties({"active_design": {}})
        self.toolkit.set_properties({"active_design": {"Maxwell3d": "Motor-CAD e9"}})
        self.toolkit.set_properties({"design_list": {"e9_eMobility_IPM__ANSYSEM_3D": [{"Maxwell3d": "Motor-CAD e9"}]}})
        assert self.toolkit.init_aedt()

    def test_2_set_model(self):
        self.toolkit.set_properties({"MagnetsMaterial": "N30UH_139.999983577095C"})
        self.toolkit.set_properties({"MagnetsSegmentsPerSlice": "5"})
        self.toolkit.set_properties({"RotorMaterial": "M250-35A_20C"})
        self.toolkit.set_properties({"RotorSlices": "3"})
        assert self.toolkit.set_model()
        self.toolkit.set_properties({"MagnetsSegmentsPerSlice": 5})
        assert self.toolkit.set_model()

    def test_3_analyze_model(self):
        self.toolkit.set_properties({"SetupToAnalyze": "Setup1"})
        assert self.toolkit.analyze_model()

    def test_4_get_magnet_losses(self):
        magnet_losses = self.toolkit.get_losses_from_reports()
        assert isinstance(magnet_losses, tuple)
        assert magnet_losses[0]
        assert isinstance(magnet_losses[1], dict)
        assert isinstance(magnet_losses[1]["SolidLoss"]["Value"], float)
        assert isinstance(magnet_losses[1]["SolidLoss"]["Unit"], str)

    def test_5_segmentation(self):
        self.toolkit.set_properties({"design_list": {"e9_eMobility_IPM__ANSYSEM_3D": [{"Maxwell3d": "Motor-CAD e9"}]}})
        self.toolkit.set_properties({"active_design": {"Maxwell3d": "Motor-CAD e9"}})
        self.toolkit.connect_design()
        assert not self.toolkit.segmentation()
        self.toolkit.set_properties({"IsSkewed": False})
        self.toolkit.set_properties({"MagnetsMaterial": "N30UH_65C"})
        self.toolkit.set_properties({"MagnetsSegmentsPerSlice": "2"})
        self.toolkit.set_properties({"RotorMaterial": "M250-35A_20C"})
        self.toolkit.set_properties({"RotorSlices": "2"})
        assert self.toolkit.segmentation()

    def test_6_apply_skew(self):
        self.toolkit.set_properties({"SkewAngle": "2deg"})
        assert self.toolkit.apply_skew()
