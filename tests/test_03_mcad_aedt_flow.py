import os
from pathlib import Path
import shutil

from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.motor.backend.api import Toolkit
from conftest import BasisTest


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.toolkit = Toolkit()
        self.mcad = self.toolkit.mcad
        src_folder = os.path.join(Path(__file__).parents[0], "input_data")
        self.temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))
        self.maxwell = self.toolkit.maxwell

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_1_init_motorcad(self):
        assert self.toolkit.init_motorcad()

    def test_2_load_mcad_file(self):
        mot_file = os.path.join(self.temp_folder, "e9_built.mot")
        assert self.toolkit.load_mcad_file()
        assert (
            os.path.splitext(os.path.basename(self.toolkit.mcad.get_variable("CurrentMotFilePath_MotorLAB")))[0]
            == "default"
        )
        self.toolkit.set_properties({"MotorCAD_filepath": mot_file})
        assert self.toolkit.load_mcad_file()
        assert (
            os.path.splitext(os.path.basename(self.toolkit.mcad.get_variable("CurrentMotFilePath_MotorLAB")))[0]
            == "e9_built"
        )

    def test_3_vbs_file_path(self):
        assert (os.path.splitext(os.path.basename(self.toolkit.mcad.get_variable("CurrentMotFilePath_MotorLAB"))))[
            0
        ] + ".vbs" == "e9_built.vbs"

    def test_4_set_emag_model(self):
        self.toolkit.set_properties({"E_mag_settings": {"NumberOfCuboids": 6}})
        self.toolkit.set_properties({"Geometry": {"MagnetAxialSegments": 8}})
        self.toolkit.set_emag_model()
        assert self.toolkit.mcad.get_variable("AxialSegments") == 8
        assert self.toolkit.mcad.get_variable("NumberOfCuboids") == 6

    def test_5_lab_performance_calculation(self):
        self.toolkit.set_properties({"LAB_settings": {"MaxSpeed": 12000, "SpeedStep": 1000, "SpeedMin": 0}})
        self.toolkit.lab_performance_calculation()
        assert self.toolkit.mcad.get_variable("SpeedMax_MotorLAB") == 12000
        assert self.toolkit.mcad.get_variable("Speedinc_MotorLAB") == 1000
        assert self.toolkit.mcad.get_variable("SpeedMin_MotorLAB") == 0

    def test_6_lab_operating_point(self):
        self.toolkit.set_properties(
            {"LAB_settings": {"MaxTempMagnet": 150, "MaxTempStatorWinding": 180, "OPSpeed": 4500}}
        )
        self.toolkit.lab_operating_point()
        assert self.toolkit.mcad.get_variable("MaxMagnet_MotorLAB") == 150
        assert self.toolkit.mcad.get_variable("StatorTempDemand_Lab") == 180

    def test_7_emag_calculation(self):
        self.toolkit.emag_calculation()
        assert not self.toolkit.mcad.get_variable("BackEMFCalculation")
        assert not self.toolkit.mcad.get_variable("CoggingTorqueCalculation")
        assert self.toolkit.mcad.get_variable("TorqueCalculation")

    def test_8_set_thermal(self):
        magnet_losses = {"SolidLoss": {"Value": 1.5}}
        self.toolkit.set_thermal(magnet_losses)
        assert self.toolkit.mcad.get_variable("ThermalCalcType") == 0
        assert self.toolkit.mcad.get_variable("Magnet_Iron_Loss_@Ref_Speed") == 1.5

    def test_9_thermal_calculation(self):
        assert isinstance(self.toolkit.thermal_calculation(), float)

    def test_10_export(self):
        self.toolkit.export_settings()
        vbs_file_path = self.toolkit.get_properties()["vbs_file_path"]
        os.path.exists(vbs_file_path)

    def test_11_init_aedt(self):
        aedt_file = os.path.join(self.temp_folder, "e9_ANSYSEM_3D.aedt")
        vbs_file_path = os.path.join(self.temp_folder, "e9_built.vbs")
        self.toolkit.set_properties({"active_project": aedt_file})
        self.toolkit.set_properties({"vbs_file_path": vbs_file_path})
        assert not self.toolkit.init_aedt()
        self.toolkit.set_properties({"vbs_file_path": ""})
        self.toolkit.set_properties({"selected_process": 1})
        self.toolkit.set_properties({"active_design": {"Maxwell3d": "Motor-CAD e9"}})
        self.toolkit.set_properties({"design_list": {"e9_ANSYSEM_3D": [{"Maxwell3d": "Motor-CAD e9"}]}})
        assert self.toolkit.init_aedt()

    def test_12_set_model(self):
        assert not self.toolkit.set_model(mcad_magnets_material=None)
        assert self.toolkit.set_model(mcad_magnets_material="N30UH")
        self.toolkit.set_properties({"HalfAxial": 1})
        assert not self.toolkit.set_model(mcad_magnets_material="Invalid")
        assert self.toolkit.set_model(mcad_magnets_material="N30UH")

    def test_13_set_mesh(self):
        assert not self.toolkit.mesh_settings(mcad_magnets_material=None)
        assert self.toolkit.mesh_settings(mcad_magnets_material="N30UH")
        assert not self.toolkit.mesh_settings(mcad_magnets_material="Invalid")

    def test_14_analyze_model(self):
        self.toolkit.set_properties({"SetupToAnalyze": "Setup1"})
        assert self.toolkit.analyze_model()

    def test_15_get_magnet_losses(self):
        magnet_losses = self.toolkit.get_losses_from_reports()
        assert isinstance(magnet_losses, tuple)
        assert magnet_losses[0]
        assert isinstance(magnet_losses[1], dict)
        assert isinstance(magnet_losses[1]["SolidLoss"]["Value"], float)
        assert isinstance(magnet_losses[1]["SolidLoss"]["Unit"], str)

    def test_16_magnets_segmentation(self):
        aedt_file = os.path.join(Path(__file__).parents[1], "input_data", "Motor3D_obj_segments.aedt")
        self.toolkit.set_properties({"active_project": aedt_file})
        self.toolkit.set_properties(
            {
                "Magnets": [
                    {
                        "Material": "Arnold_Magnetics_N30UH_80C_new",
                        "MeshLength": 1,
                        "MeshName": "magnets_mesh_test",
                        "Name": "PM_I1",
                        "NumberOfSegments": 10,
                    },
                    {
                        "Material": "Arnold_Magnetics_N30UH_80C_new",
                        "MeshLength": 1,
                        "MeshName": "magnets_mesh_test_1",
                        "Name": "PM_I1_1",
                        "NumberOfSegments": 10,
                    },
                ]
            }
        )
        assert self.toolkit.magnets_segmentation()
