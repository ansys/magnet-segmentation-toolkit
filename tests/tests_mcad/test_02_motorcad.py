import os

from ansys.aedt.toolkits.motor.common_settings import CommonSettings
from ansys.aedt.toolkits.motor.motorcad_settings import MotorCADSettings
from conftest import BasisTest
from pathlib import Path


class TestClass(BasisTest, object):
    def setup_class(self):
        BasisTest.my_setup(self)
        self.common_settings = CommonSettings(working_dir=self.local_scratch.path)
        self.mcad = BasisTest.add_app(self)
        self.mcad_settings = MotorCADSettings(
            self.common_settings.config_settings_path, motorcad=self.mcad
        )

    def teardown_class(self):
        BasisTest.my_teardown(self)

    def test_1_working_dir(self):
        assert self.mcad_settings.working_dir == os.path.dirname(
            self.common_settings.config_settings_path
        )

    def test_2_mcadapp(self):
        assert self.mcad_settings.mcad == self.mcad

    def test_3_file_name(self):
        mot_file = os.path.join(Path(__file__).parents[1], "input_data", "e9_built.mot")
        self.mcad_settings.mcad_dict["MotorCAD_filepath"] = mot_file
        self.mcad_settings.load_mcad_file()
        assert (
            os.path.splitext(
                os.path.basename(
                    self.mcad_settings.mcad.get_variable("CurrentMotFilePath_MotorLAB")
                )
            )[0]
            == "e9_built"
        )

    def test_4_vbs_file_path(self):
        assert (
            os.path.splitext(
                os.path.basename(
                    self.mcad_settings.mcad.get_variable("CurrentMotFilePath_MotorLAB")
                )
            ))[0] + ".vbs" == "e9_built.vbs"

    def test_5_set_geometry_model(self):
        self.mcad_settings.mcad_dict["Geometry"]["Magnet_Axial_Segments"] = 8
        self.mcad_settings.mcad_dict["E_mag_settings"]["Number_of_Cuboids"] = 8
        self.mcad_settings.set_geometry_model()
        assert self.mcad_settings.mcad.get_variable("AxialSegments") == 8
        assert self.mcad_settings.mcad.get_variable("NumberOfCuboids") == 8

    def test_6_set_lab_model(self):
        self.mcad_settings.mcad_dict["LAB_settings"]["Max_Speed"] = 12000
        self.mcad_settings.mcad_dict["LAB_settings"]["Speed_Step"] = 1000
        self.mcad_settings.mcad_dict["LAB_settings"]["Speed_Min"] = 0
        self.mcad_settings.lab_performance_calculation()
        assert self.mcad_settings.mcad.get_variable("SpeedMax_MotorLAB") == 12000
        assert self.mcad_settings.mcad.get_variable("Speedinc_MotorLAB") == 1000
        assert self.mcad_settings.mcad.get_variable("SpeedMin_MotorLAB") == 0

    def test_7_lab_operating_point(self):
        self.mcad_settings.mcad_dict["LAB_settings"]["Lab_Max_Temp_Magnet"] = 150
        self.mcad_settings.mcad_dict["LAB_settings"]["Lab_Max_Temp_St_Wind"] = 180
        self.mcad_settings.lab_operating_point()
        assert self.mcad_settings.mcad.get_variable("MaxMagnet_MotorLAB") == 150
        assert self.mcad_settings.mcad.get_variable("StatorTempDemand_Lab") == 180

    def test_8_emag_calculation(self):
        self.mcad_settings.mcad_dict["E_mag_settings"]["Test_Back_EMF"] = False
        self.mcad_settings.mcad_dict["E_mag_settings"]["Test_Cogging"] = False
        self.mcad_settings.mcad_dict["E_mag_settings"]["Test_Torque"] = True
        self.mcad_settings.emag_calculation()
        assert not self.mcad_settings.mcad.get_variable("BackEMFCalculation")
        assert not self.mcad_settings.mcad.get_variable("CoggingTorqueCalculation")
        assert self.mcad_settings.mcad.get_variable("TorqueCalculation")

    def test_9_set_thermal(self):
        magnet_losses = {"SolidLoss": {"Value": 1.5}}
        self.mcad_settings.set_thermal(magnet_losses)
        assert self.mcad_settings.mcad.get_variable("ThermalCalcType") == 0

    def test_10_export(self):
        self.mcad_settings.export_settings()
        os.path.exists(self.mcad_settings.vbs_file_path)
