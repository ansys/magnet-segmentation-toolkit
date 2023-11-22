import os

import pytest

from tests.tests_mcad.conftest import PROJECT_NAME
from tests.tests_mcad.conftest import wait_toolkit

pytestmark = [pytest.mark.mcad]


class TestClass(object):
    def test_init_motorcad(self, basic_toolkit):
        assert basic_toolkit.init_motorcad()
        wait_toolkit(basic_toolkit)

    # def test_2_load_default_mcad_file(self, basic_toolkit):
    #     assert basic_toolkit.init_motorcad()
    #     wait_toolkit(basic_toolkit)

    #     assert basic_toolkit.load_mcad_file()
    #     value = basic_toolkit.mcad.get_variable("CurrentMotFilePath_MotorLAB")
    #     assert os.path.splitext(os.path.basename(value))[0] == "default"

    def test_2_load_mcad_file(self, toolkit):
        assert toolkit.init_motorcad()
        wait_toolkit(toolkit)

        assert toolkit.load_mcad_file()
        value = toolkit.mcad.get_variable("CurrentMotFilePath_MotorLAB")
        assert os.path.splitext(os.path.basename(value))[0] == f"{PROJECT_NAME}"

    # def test_4_set_emag_model(self, toolkit):
    #     assert toolkit.init_motorcad()
    #     wait_toolkit(toolkit)

    #     props = toolkit.get_properties()
    #     props["E_mag_settings"]["NumberOfCuboids"] = 4
    #     toolkit.set_properties(props)
    #     toolkit.set_emag_model()
    #     assert toolkit.mcad.get_variable("NumberOfCuboids") == 4

    # def test_5_lab_performance_calculation(self, toolkit):
    #     props = toolkit.get_properties()
    #     props["LAB_settings"]["MaxSpeed"] = 2000
    #     props["LAB_settings"]["SpeedStep"] = 1000
    #     props["LAB_settings"]["SpeedMin"] = 0
    #     toolkit.set_properties(props)
    #     toolkit.lab_performance_calculation()
    #     assert toolkit.mcad.get_variable("SpeedMax_MotorLAB") == 2000
    #     assert toolkit.mcad.get_variable("Speedinc_MotorLAB") == 1000
    #     assert toolkit.mcad.get_variable("SpeedMin_MotorLAB") == 0

    # def test_6_lab_operating_point(self, toolkit):
    #     props = toolkit.get_properties()
    #     props["LAB_settings"]["MaxTempMagnet"] = 150
    #     props["LAB_settings"]["MaxTempStatorWinding"] = 180
    #     props["LAB_settings"]["OPSpeed"] = 4500
    #     toolkit.set_properties(props)
    #     toolkit.lab_operating_point()
    #     assert toolkit.mcad.get_variable("MaxMagnet_MotorLAB") == 150
    #     assert toolkit.mcad.get_variable("StatorTempDemand_Lab") == 180

    # def test_7_emag_calculation(self, toolkit):
    #     toolkit.emag_calculation()
    #     assert not toolkit.mcad.get_variable("BackEMFCalculation")
    #     assert not toolkit.mcad.get_variable("CoggingTorqueCalculation")
    #     assert toolkit.mcad.get_variable("TorqueCalculation")

    # def test_8_set_thermal(self, toolkit):
    #     magnet_losses = {"SolidLoss": {"Value": 1.5}}
    #     toolkit.set_thermal(magnet_losses)
    #     assert toolkit.mcad.get_variable("ThermalCalcType") == 0
    #     assert toolkit.mcad.get_variable("Magnet_Iron_Loss_@Ref_Speed") == 1.5

    # def test_9_thermal_calculation(self, toolkit):
    #     assert isinstance(toolkit.thermal_calculation(), float)

    # def test_10_export(self, toolkit):
    #     toolkit.export_settings()

    #     wait_toolkit(toolkit)

    #     vbs_file_path = toolkit.get_properties()["vbs_file_path"]
    #     os.path.exists(vbs_file_path)
    #     assert toolkit.mcad.get_variable("AxialSegments") == 1

    # def test_11_save(self, toolkit):
    #     assert toolkit.save()

    # def test_12_close(self, toolkit):
    #     assert toolkit.close_motorcad()
    #     toolkit.mcad = None
