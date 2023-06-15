import os

from pyaedt import Maxwell3d

from ansys.aedt.toolkits.motor.aedt_export import AedtExport
from ansys.aedt.toolkits.motor.common_settings import CommonSettings
from conftest import BasisTest

test_project_name = "e9_ANSYSEM_3D"


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.common_settings = CommonSettings(working_dir=self.local_scratch.path)
        self.aedtapp = BasisTest.add_app(
            self, application=Maxwell3d, project_name=test_project_name
        )
        self.aedt = AedtExport(self.common_settings.config_settings_path, m3d=self.aedtapp)

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_01_working_dir(self):
        assert self.aedt.working_dir == os.path.dirname(self.common_settings.config_settings_path)

    def test_02_maxwell(self):
        assert self.aedt.maxwell == self.aedtapp

    def test_03_set_model(self):
        self.aedt.aedt_dict["ModelParameters"]["NumberTorqueCycles"] = 1
        self.aedt.aedt_dict["ModelParameters"]["NumberPointsTorqueCycles"] = 2
        self.aedt.set_model()
        assert self.aedt.maxwell["HalfAxial"] == "1"
        assert self.aedt.maxwell["NumTorqueCycles"] == "1"
        assert self.aedt.maxwell["NumTorquePointsPerCycle"] == "2"
        assert [bound for bound in self.aedt.maxwell.boundaries if "Insulating" == bound.type]
        assert [bound for bound in self.aedt.maxwell.boundaries if "Symmetry" == bound.type]

    def test_04_mesh(self):
        self.aedt.aedt_dict["Mesh"]["Windings"]["Length"] = 5
        self.aedt.aedt_dict["Mesh"]["RotorAndStator"]["Length"] = 8
        self.aedt.aedt_dict["Mesh"]["Magnets"]["Length"] = 2
        self.aedt.mesh_settings()
        windings_mesh = [
            mesh for mesh in self.aedt.maxwell.mesh.meshoperations if mesh.name == "windings_mesh"
        ]
        assert windings_mesh[0].props["MaxLength"] == "5mm"
        rotor_and_stator_mesh = [
            mesh
            for mesh in self.aedt.maxwell.mesh.meshoperations
            if mesh.name == "rotor_and_stator_mesh"
        ]
        assert rotor_and_stator_mesh[0].props["MaxLength"] == "8mm"
        magnets_mesh = [
            mesh for mesh in self.aedt.maxwell.mesh.meshoperations if mesh.name == "magnets_mesh"
        ]
        assert magnets_mesh[0].props["MaxLength"] == "2mm"

    def test_05_reports(self):
        self.aedt.maxwell.setups[0].props["StopTime"] = "0.002s"
        self.aedt.maxwell.setups[0].props["TimeStep"] = "0.001s"
        self.aedt.maxwell.setups[0].props["SaveFieldsType"] = "None"
        self.aedt.analyze_model()
        reports = self.aedt.get_values_from_reports()
        assert reports
        assert isinstance(reports, dict)
        assert isinstance(reports["SolidLoss"]["Value"], float)
        assert isinstance(reports["SolidLoss"]["Unit"], str)
