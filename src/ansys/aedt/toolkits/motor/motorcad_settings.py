import os

import ansys.motorcad.core as pymotorcad
from pyaedt import generate_unique_folder_name


class MotorCADSettings:
    """Creates a MotorCAD instance and load a predefined template.

    Provides a Motor-CAD instance to set geometry,
    LAB and electromagnetic settings in order to export the model.

    Parameters
    ----------
    working_dir : str, optional
        Working directory to store results and .mot file.
        If nothing is provided a new temp folder is created.
        Default value is ``None``.

    Examples
    --------
    >>>> mcad = MotorCADSettings()
    Set the geometry model
    >>>> mcad.set_geometry_model()
    Set LAB module, build LAB model, calculate Emag performance,
    Set continuous performance operating points
    >>>> mcad.set_lab_model()
    Set and run emag calculation
    >>>> mcad.emag_calculation()
    Set export settings to get .vbs script
    >>>> mcad.export_settings()
    """

    def __init__(self, working_dir=None):
        """Init."""
        self.mcad = pymotorcad.MotorCAD()
        self.mcad.set_variable("MessageDisplayState", 2)
        if working_dir:
            self.working_dir = working_dir
        else:
            self.working_dir = generate_unique_folder_name(folder_name="pymotorcad_pyaedt_toolkit")
        self.mcad_name = "e9"
        self.mcad_file_path = os.path.join(self.working_dir, "{}.mot".format(self.mcad_name))
        self.vbs_file_path = os.path.join(self.working_dir, "{}.vbs".format(self.mcad_name))

    def set_geometry_model(self):
        """Set geometry model."""
        self.mcad.load_template(self.mcad_name)
        self.mcad.show_magnetic_context()
        self.mcad.display_screen("Scripting")
        self.mcad.set_variable("ProximityLossModel", 1)
        self.mcad.set_variable("NumberOfCuboids", 6)
        self.mcad.set_variable("AxialSegments", 6)

        self.mcad.save_to_file(self.mcad_file_path)

    def set_lab_model(self):
        """Set lab model build parameters and build the model."""
        # LAB Module
        self.mcad.set_motorlab_context()
        self.mcad.set_variable("ModelType_MotorLAB", 2)
        self.mcad.set_variable("SatModelPoints_MotorLAB", 1)
        self.mcad.set_variable("LossModel_Lab", 1)
        self.mcad.set_variable("ACLossMethod_Lab", 0)
        self.mcad.set_variable("ModelBuildSpeed_MotorLAB", 10000)
        self.mcad.set_variable("MaxModelCurrent_MotorLAB", 480)
        self.mcad.set_variable("BuildSatModel_MotorLAB", True)
        self.mcad.set_variable("BuildLossModel_MotorLAB", True)

        # Build the model.
        self.mcad.clear_model_build_lab()
        self.mcad.build_model_lab()

        # self.mcad.load_template("Test_e9_built")

    def lab_performance_calculation(self):
        """Calculate lab electromagnetic performance curves-
           Maximum Torque-speed and Efficiency Map ."""
        # Peak performance Torque-Speed curve
        self.mcad.set_variable("EmagneticCalcType_Lab", 0)
        self.mcad.set_variable("SpeedMax_MotorLAB", 10000)
        self.mcad.set_variable("SpeedMin_MotorLAB", 0)
        self.mcad.set_variable("Speedinc_MotorLAB", 500)
        self.mcad.set_variable("OperatingMode_Lab", 0)
        self.mcad.calculate_magnetic_lab()

    def lab_operating_point(self):
        """Set lab operating point based on given input conditions."""
        # Continuous performance operating points
        self.mcad.set_variable("LabMagneticCoupling", 1)
        self.mcad.set_variable("OpPointSpec_MotorLAB", 2)
        self.mcad.set_variable("ThermCalcType_MotorLAB", 0)
        self.mcad.set_variable("ThermalMapType_Lab", 0)
        self.mcad.set_variable("MaxWindTemp_MotorLAB", 140)
        self.mcad.set_variable("StatorTempDemand_Lab", 140)
        self.mcad.set_variable("MaxMagnet_MotorLAB", 160)
        self.mcad.set_variable("RotorTempDemand_Lab", 160)
        self.mcad.set_variable("SpeedDemand_MotorLAB", 4500)
        self.mcad.calculate_operating_point_lab()
        shaft_power = self.mcad.get_variable("LabOpPoint_ShaftPower")
        efficiency = self.mcad.get_variable("LabOpPoint_Efficiency")
        print("Shaft Power", round(shaft_power / 1000, 2), "kW")
        print("Efficiency", round(efficiency, 2), "%")

    def emag_calculation(self):
        """Set Emag calculation."""
        self.mcad.show_magnetic_context()

        self.mcad.set_variable("BackEMFCalculation", False)
        self.mcad.set_variable("CoggingTorqueCalculation", False)
        self.mcad.set_variable("ElectromagneticForcesCalc_OC", False)
        self.mcad.set_variable("TorqueSpeedCalculation", False)
        self.mcad.set_variable("DemagnetizationCalc", False)
        self.mcad.set_variable("ElectromagneticForcesCalc_Load", False)
        self.mcad.set_variable("InductanceCalc", False)
        self.mcad.set_variable("BPMShortCircuitCalc", False)
        self.mcad.set_variable("TorqueCalculation", True)
        self.mcad.set_variable("MagneticThermalCoupling", 1)
        self.mcad.do_magnetic_calculation()

    def losses_emag_to_thermal(self):
        """Transfers emag losses to thermal module"""
        self.mcad.set_variable("MagneticThermalCoupling", 1)
        self.mcad.show_thermal_context()

    def export_settings(self):
        """Set export settings."""
        self.mcad.show_magnetic_context()
        self.mcad.set_variable("AnsysExportFormat", 1)
        # 3D export
        self.mcad.set_variable("AnsysModelType", 1)
        self.mcad.set_variable("AnsysSolve", 1)
        self.mcad.set_variable("AnsysArcSegmentMethod", 0)
        self.mcad.set_variable("Ansys_MergeEntities", 0)
        self.mcad.set_variable("Ansys_WindingGroups", 0)
        self.mcad.set_variable("AnsysRotationDirection", 0)
        self.mcad.export_to_ansys_electronics_desktop(self.vbs_file_path)

    def mcad_save(self):
        """Save the motorcad file """
        self.mcad.save_to_file(self.mcad_file_path)


    def mcad_close(self):
        """Closes the motorcad instance"""
        self.mcad.quit()

    def set_thermal(self):
        """Set the motorcad thermal calculations, cooling and losses ."""
        self.mcad.show_thermal_context()
        self.mcad.set_variable("ThermalCalcType", 0)

    def thermal_calculation(self):
        """Perform thermal calculation."""
        print("input wind temp",self.mcad.get_variable("Winding_Temperature_at_which_Pcu_Input"))
        self.mcad.do_steady_state_analysis()
        print("output avg wind 13859",self.mcad.get_variable("Temp_Winding_Average"))


    def load_mcad_file(self):
        self.mcad.load_from_file(self.mcad_file_path)
