import pytest

from tests.tests_aedt.conftest import DESIGN_NAME
from tests.tests_aedt.conftest import PROJECT_NAME
from tests.tests_aedt.conftest import wait_toolkit

pytestmark = [pytest.mark.aedt]


class TestClass(object):
    """"""

    def test_launch_aedt(self, toolkit):
        """Launch aedt."""
        toolkit.set_properties({"vbs_file_path": ""})
        toolkit.set_properties({"active_design": {"Maxwell3d": f"{DESIGN_NAME}"}})
        toolkit.set_properties({"design_list": {f"{PROJECT_NAME}": [{"Maxwell3d": f"{DESIGN_NAME}"}]}})
        assert toolkit.launch_aedt()

        wait_toolkit(toolkit)

    # def test_3_analyze_model(self):
    #     self.toolkit.set_properties({"SetupToAnalyze": "Setup1"})
    #     assert self.toolkit.analyze_model()
    #
    # def test_4_get_magnet_losses(self):
    #     magnet_losses = self.toolkit.get_losses_from_reports()
    #     assert isinstance(magnet_losses, tuple)
    #     assert magnet_losses[0]
    #     assert isinstance(magnet_losses[1], dict)
    #     assert isinstance(magnet_losses[1]["SolidLoss"]["Value"], float)
    #     assert isinstance(magnet_losses[1]["SolidLoss"]["Unit"], str)

    def test_segmentation(self, toolkit):
        """Apply objects segmentation."""
        toolkit.set_properties({"active_design": {"Maxwell3d": f"{DESIGN_NAME}"}})
        toolkit.set_properties({"design_list": {f"{PROJECT_NAME}": [{"Maxwell3d": f"{DESIGN_NAME}"}]}})
        assert toolkit.launch_aedt()

        wait_toolkit(toolkit)

        toolkit.set_properties({"IsSkewed": False})
        toolkit.set_properties({"MagnetsMaterial": "N30UH_65C"})
        toolkit.set_properties({"MagnetsSegmentsPerSlice": "2"})
        toolkit.set_properties({"RotorMaterial": "M250-35A_20C"})
        toolkit.set_properties({"RotorSlices": "2"})
        assert toolkit.segmentation()

    def test_apply_skew(self, toolkit):
        """Apply skew to rotor slices."""
        toolkit.set_properties({"active_design": {"Maxwell3d": f"{DESIGN_NAME}"}})
        toolkit.set_properties({"design_list": {f"{PROJECT_NAME}": [{"Maxwell3d": f"{DESIGN_NAME}"}]}})
        assert toolkit.launch_aedt()

        wait_toolkit(toolkit)

        toolkit.set_properties({"IsSkewed": False})
        toolkit.set_properties({"MagnetsMaterial": "N30UH_65C"})
        toolkit.set_properties({"MagnetsSegmentsPerSlice": "2"})
        toolkit.set_properties({"RotorMaterial": "M250-35A_20C"})
        toolkit.set_properties({"RotorSlices": "2"})
        assert toolkit.segmentation()

        toolkit.set_properties({"SkewAngle": "2deg"})
        assert toolkit.apply_skew()
