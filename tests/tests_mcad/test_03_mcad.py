import os
from pathlib import Path
import shutil
import gc
from pyaedt import generate_unique_folder_name

from ansys.aedt.toolkits.motor.backend.api import Toolkit


class TestClass(object):
    def setup_class(self):
        self.toolkit = Toolkit()
        src_folder = os.path.join(Path(__file__).parents[1], "input_data")
        self.temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))

    def teardown_class(self):
        if self.toolkit.mcad:
            self.toolkit.mcad.quit()
        # Register the cleanup function to be called on script exit
        gc.collect()
        shutil.rmtree(self.temp_folder, ignore_errors=True)

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

    def test_11_save(self):
        assert self.toolkit.save()

    def test_12_close(self):
        assert self.toolkit.close_motorcad()
        self.toolkit.mcad = None
