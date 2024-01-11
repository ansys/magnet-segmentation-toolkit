import pytest

from tests.tests_aedt.conftest import DESIGN_NAME
from tests.tests_aedt.conftest import PROJECT_NAME

pytestmark = [pytest.mark.aedt]


class TestAEDTMotorWorkflow:
    """Class defining a simple AEDT motor related workflow."""

    def test_00_connect_aedt(self, toolkit):
        """Connect aedt."""
        new_properties = {
            "active_design": {"Maxwell3d": f"{DESIGN_NAME}"},
            "designs_by_project_name": {f"{PROJECT_NAME}": [{"Maxwell3d": f"{DESIGN_NAME}"}]},
        }

        assert toolkit.set_properties(new_properties)
        assert toolkit.connect_aedt()
        assert toolkit.aedt_connected()

    def test_01_segmentation(self, toolkit):
        """Apply objects segmentation."""
        new_properties = {
            "is_skewed": False,
            "magnets_material": "N30UH_65C",
            "magnet_segments_per_slice": 2,
            "rotor_material": "M250-35A_20C",
            "rotor_slices": 2,
        }

        assert toolkit.set_properties(new_properties)
        assert toolkit.connect_aedt()
        assert toolkit.segmentation()

    def test_02_apply_skew(self, toolkit):
        """Apply skew angle to rotor slices."""
        assert toolkit.set_properties({"skew_angle": "2deg"})
        assert toolkit.apply_skew()
