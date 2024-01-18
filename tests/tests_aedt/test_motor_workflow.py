import pytest

from tests.tests_aedt.conftest import DESIGN_NAME
from tests.tests_aedt.conftest import PROJECT_NAME

pytestmark = [pytest.mark.aedt]

APP_NAME = "Maxwell3d"
DESIGN_PROPERTIES = {
    "active_design": {APP_NAME: DESIGN_NAME},
    "designs_by_project_name": {PROJECT_NAME: [{APP_NAME: DESIGN_NAME}]},
}


class TestAEDTMotorWorkflow:
    """Class defining a simple AEDT motor related workflow."""

    def test_00_installed_aedt_version(self, toolkit):
        """Check isntalled aedt version."""
        assert toolkit.installed_aedt_version() != []

    def test_01_set_properties(self, toolkit):
        """Set properties."""
        assert toolkit.set_properties(DESIGN_PROPERTIES)

    def test_02_get_properties(self, toolkit):
        """Get properties."""
        properties = toolkit.get_properties()
        assert DESIGN_PROPERTIES["active_design"] == properties["active_design"]
        assert DESIGN_PROPERTIES["designs_by_project_name"] == properties["designs_by_project_name"]

    def test_03_connect_aedt(self, toolkit):
        """Connect aedt."""
        assert toolkit.connect_aedt()
        assert toolkit.aedt_connected()

    def test_04_aedt_sessions(self, toolkit):
        """Check aedt sessions."""
        assert toolkit.aedt_sessions() != []

    def test_05_get_design_names(self, toolkit):
        """Check deisng names of the project."""
        res = toolkit.get_design_names()
        assert len(res) == 1
        assert res[0][APP_NAME] == DESIGN_NAME

    def test_06_segmentation(self, toolkit):
        """Apply objects segmentation."""
        properties = {
            "motor_type": "IPM",
            "is_skewed": False,
            "magnets_material": "N30UH_65C",
            "magnet_segments_per_slice": 2,
            "rotor_material": "M250-35A_20C",
            "stator_material": "M250-35A_20C",
            "rotor_slices": 2,
            "apply_mesh_sheets": True,
            "mesh_sheets_number": 2,
        }
        assert toolkit.set_properties(properties)
        # assert toolkit.connect_aedt()
        assert toolkit.segmentation()

    def test_07_apply_skew(self, toolkit):
        """Apply skew angle to rotor slices."""
        assert toolkit.set_properties({"skew_angle": "2deg"})
        assert toolkit.apply_skew()
