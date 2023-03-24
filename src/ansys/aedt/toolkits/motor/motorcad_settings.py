import os

import ansys.motorcad.core as pymotorcad

from ansys.aedt.toolkits.motor.common_settings import CommonSettings


class MotorCADSettings:
    """Creates a MotorCAD instance and load a predefined template.

    Provides a Motor-CAD instance to set geometry,
    LAB and electromagnetic settings in order to export the model.

    Examples
    --------
    >>> mcad = MotorCADSettings()
    Set the geometry model
    >>> mcad.set_geometry_model()
    Set LAB module, build LAB model, calculate Emag performance,
    Set continuous performance operating points
    >>> mcad.set_lab_model()
    Set and run emag calculation
    >>> mcad.emag_calculation()
    Set export settings to get .vbs script
    >>> mcad.export_settings()
    """

    def __init__(self, settings_path, motorcad=None):
        """Init."""
        self.mcad = motorcad
        self.working_dir = os.path.dirname(settings_path)
        self.mcad_dict = CommonSettings(settings_path).load_json(
            os.path.join(settings_path, "motorcad_parameters.json")
        )
        self.mcad_file_path = self.mcad_dict["MotorCAD_filepath"]
        self.vbs_file_path = os.path.join(
            self.working_dir, "{}.vbs".format(os.path.splitext(self.mcad_file_path)[0])
        )

    def init_motorcad(self):
        """Initialize MotorCAD."""
        if not self.mcad:
            self.mcad = pymotorcad.MotorCAD()
        self.mcad.set_variable("MessageDisplayState", 2)

    def load_mcad_file(self):
        """Load a .mot file."""
        self.mcad.load_from_file(self.mcad_file_path)

    def set_geometry_model(self):
        """Set geometry model."""
        self.mcad.show_magnetic_context()
        self.mcad.display_screen("Scripting")
        self.mcad.set_variable(
            "ProximityLossModel", self.mcad_dict["E_mag_settings"]["AC_Winding_Loss_Model"]
        )
        self.mcad.set_variable(
            "NumberOfCuboids", self.mcad_dict["E_mag_settings"]["Number_of_Cuboids"]
        )
        self.mcad.set_variable("AxialSegments", self.mcad_dict["Geometry"]["Magnet_Axial_Segments"])

        self.mcad.save_to_file(self.mcad_file_path)

    def set_lab_model(self):
        """Set lab model build parameters and build the model."""
        self.mcad.set_motorlab_context()
        self.mcad.set_variable(
            "ModelType_MotorLAB", self.mcad_dict["LAB_settings"]["Saturation_Full_cycle"]
        )
        self.mcad.set_variable(
            "SatModelPoints_MotorLAB", self.mcad_dict["LAB_settings"]["Model_Res_Fine"]
        )
        self.mcad.set_variable("LossModel_Lab", self.mcad_dict["LAB_settings"]["Loss_Model_FEAMap"])
        self.mcad.set_variable("ACLossMethod_Lab", self.mcad_dict["LAB_settings"]["AC_Loss_Hybrid"])
        self.mcad.set_variable(
            "ModelBuildSpeed_MotorLAB", self.mcad_dict["LAB_settings"]["Max_Speed"]
        )
        self.mcad.set_variable(
            "MaxModelCurrent_MotorLAB", self.mcad_dict["LAB_settings"]["Max_Stator_Current"]
        )
        self.mcad.set_variable(
            "BuildSatModel_MotorLAB", self.mcad_dict["LAB_settings"]["Build_Sat_Model"]
        )
        self.mcad.set_variable(
            "BuildLossModel_MotorLAB", self.mcad_dict["LAB_settings"]["Build_Loss_Model"]
        )

        # Build the model.
        self.mcad.clear_model_build_lab()
        self.mcad.build_model_lab()

        # self.mcad.load_template("Test_e9_built")

    def lab_performance_calculation(self):
        """Calculate lab performance curves-Maximum Torque-speed and Efficiency Map."""
        self.mcad.set_variable("EmagneticCalcType_Lab", 0)
        self.mcad.set_variable("SpeedMax_MotorLAB", self.mcad_dict["LAB_settings"]["Max_Speed"])
        self.mcad.set_variable("SpeedMin_MotorLAB", self.mcad_dict["LAB_settings"]["Speed_Min"])
        self.mcad.set_variable("Speedinc_MotorLAB", self.mcad_dict["LAB_settings"]["Speed_Step"])
        self.mcad.set_variable("OperatingMode_Lab", self.mcad_dict["LAB_settings"]["Max_TS_Curve"])
        self.mcad.calculate_magnetic_lab()

    def lab_operating_point(self):
        """Set lab operating point based on given input conditions."""
        self.mcad.set_variable(
            "OpPointSpec_MotorLAB", self.mcad_dict["LAB_settings"]["OP_Def_Max_Temp"]
        )
        self.mcad.set_variable(
            "LabMagneticCoupling", self.mcad_dict["LAB_settings"]["OP_Link_Lab_Emag"]
        )
        self.mcad.set_variable(
            "ThermCalcType_MotorLAB", self.mcad_dict["LAB_settings"]["OP_Link_Lab_Thermal"]
        )
        self.mcad.set_variable(
            "ThermalMapType_Lab", self.mcad_dict["LAB_settings"]["Thermal_Envelop"]
        )
        self.mcad.set_variable(
            "MaxWindTemp_MotorLAB", self.mcad_dict["LAB_settings"]["Lab_Max_Temp_St_Wind"]
        )
        self.mcad.set_variable(
            "StatorTempDemand_Lab", self.mcad_dict["LAB_settings"]["Lab_Max_Temp_St_Wind"]
        )
        self.mcad.set_variable(
            "MaxMagnet_MotorLAB", self.mcad_dict["LAB_settings"]["Lab_Max_Temp_Magnet"]
        )
        self.mcad.set_variable(
            "RotorTempDemand_Lab", self.mcad_dict["LAB_settings"]["Lab_Max_Temp_Magnet"]
        )
        self.mcad.set_variable("SpeedDemand_MotorLAB", self.mcad_dict["LAB_settings"]["OP_Speed"])
        self.mcad.calculate_operating_point_lab()
        shaft_power = self.mcad.get_variable("LabOpPoint_ShaftPower")
        efficiency = self.mcad.get_variable("LabOpPoint_Efficiency")
        print("Shaft Power", round(shaft_power / 1000, 2), "kW")
        print("Efficiency", round(efficiency, 2), "%")

    def emag_calculation(self):
        """Set Emag calculation."""
        self.mcad.show_magnetic_context()

        self.mcad.set_variable(
            "BackEMFCalculation", self.mcad_dict["E_mag_settings"]["Test_Back_EMF"]
        )
        self.mcad.set_variable(
            "CoggingTorqueCalculation", self.mcad_dict["E_mag_settings"]["Test_Cogging"]
        )
        self.mcad.set_variable(
            "ElectromagneticForcesCalc_OC", self.mcad_dict["E_mag_settings"]["Test_OC_Forces"]
        )
        self.mcad.set_variable(
            "TorqueSpeedCalculation", self.mcad_dict["E_mag_settings"]["Test_TS_curce"]
        )
        self.mcad.set_variable(
            "DemagnetizationCalc", self.mcad_dict["E_mag_settings"]["Test_Demag"]
        )
        self.mcad.set_variable(
            "ElectromagneticForcesCalc_Load", self.mcad_dict["E_mag_settings"]["Test_Load_Forces"]
        )
        self.mcad.set_variable(
            "InductanceCalc", self.mcad_dict["E_mag_settings"]["Test_Indcutances"]
        )
        self.mcad.set_variable(
            "BPMShortCircuitCalc", self.mcad_dict["E_mag_settings"]["Test_ShortCircuit"]
        )
        self.mcad.set_variable("TorqueCalculation", self.mcad_dict["E_mag_settings"]["Test_Torque"])
        self.mcad.set_variable(
            "MagneticThermalCoupling", self.mcad_dict["E_mag_settings"]["Emag_Thermal_Coupling"]
        )
        self.mcad.do_magnetic_calculation()

    def set_thermal(self, magnet_loss=None):
        """Set the motorcad thermal calculations, cooling and losses ."""
        self.mcad.show_thermal_context()
        self.mcad.set_variable("ThermalCalcType", 0)
        if magnet_loss:
            self.mcad.set_variable("Magnet_Iron_Loss_@Ref_Speed", magnet_loss["SolidLoss"]["Value"])

    def thermal_calculation(self):
        """Perform  steady state thermal calculation."""
        self.mcad.do_steady_state_analysis()
        print("Avg Winding Temp", self.mcad.get_variable("Temp_Winding_Average"))

    def export_settings(self):
        """Set export settings."""
        self.mcad.show_magnetic_context()
        self.mcad.set_variable("AnsysExportFormat", 1)
        self.mcad.set_variable("AnsysModelType", 1)
        self.mcad.set_variable("AnsysSolve", 1)
        self.mcad.set_variable("AnsysArcSegmentMethod", 0)
        self.mcad.set_variable("Ansys_MergeEntities", 0)
        self.mcad.set_variable("Ansys_WindingGroups", 0)
        self.mcad.set_variable("AnsysRotationDirection", 0)
        self.mcad.export_to_ansys_electronics_desktop(self.vbs_file_path)

    def save(self):
        """Save the motorcad file."""
        self.mcad.save_to_file(self.mcad_file_path)

    def close(self):
        """Close the motorcad instance."""
        self.mcad.quit()
