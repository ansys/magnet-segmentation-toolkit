import ansys.motorcad.core as pymotorcad
import os

from pyaedt import generate_unique_folder_name


class MotorCADSettings:
    def __init__(self, working_dir=None):
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
        self.mcad.load_template(self.mcad_name)
        self.mcad.show_magnetic_context()
        self.mcad.display_screen("Scripting")
        self.mcad.set_variable("ProximityLossModel", 1)
        self.mcad.set_variable("NumberOfCuboids", 6)
        self.mcad.set_variable("AxialSegments", 6)

        self.mcad.save_to_file(self.mcad_file_path)

    def set_lab_model(self):
        # LAB Module
        self.mcad.set_motorlab_context()

        self.mcad.set_variable("ModelType_MotorLAB", 2)  # Model type: Saturation Model (Full Cycle)
        self.mcad.set_variable("SatModelPoints_MotorLAB", 1)  # Model Resolution : Fine (30 Points)
        self.mcad.set_variable("LossModel_Lab", 1)  # Loss Model : FEA Map
        self.mcad.set_variable("ACLossMethod_Lab", 0)  # AC Loss Model : Hybrid Method
        self.mcad.set_variable("ModelBuildSpeed_MotorLAB", 10000)  # Max speed
        self.mcad.set_variable("MaxModelCurrent_MotorLAB", 480)  # Max current
        self.mcad.set_variable("BuildSatModel_MotorLAB", True)  # Enable Saturation model
        self.mcad.set_variable("BuildLossModel_MotorLAB", True)  # Enable Loss model

        # Build the model.
        self.mcad.clear_model_build_lab()
        self.mcad.build_model_lab()

        #self.mcad.load_template("Test_e9_built")

        # Peak performance  Torque-Speed curve
        self.mcad.set_variable("EmagneticCalcType_Lab", 0)  # Calc type: Max Torque speed curve
        self.mcad.set_variable("SpeedMax_MotorLAB", 10000)  # Max speed for TS curve
        self.mcad.set_variable("SpeedMin_MotorLAB", 0)  # Min speed for TS curve
        self.mcad.set_variable("Speedinc_MotorLAB", 500)  # Step size
        self.mcad.set_variable("OperatingMode_Lab", 0)  # Motor mode only
        self.mcad.calculate_magnetic_lab()  # calculate Emagnetic Performance

        # Continuous performance operating points
        self.mcad.set_variable("LabMagneticCoupling", 1)  # Send operating point to emag
        self.mcad.set_variable("OpPointSpec_MotorLAB", 2)  # Max temp definition for operating point
        self.mcad.set_variable(
            "ThermCalcType_MotorLAB", 0
        )  # Run steady state thermal calc to save computation time
        self.mcad.set_variable(
            "ThermalMapType_Lab", 0
        )  # Thermal envelope option (relevant for max curve value option only)
        self.mcad.set_variable("MaxWindTemp_MotorLAB", 140)  # Set winding temperature
        self.mcad.set_variable("StatorTempDemand_Lab", 140)  # Set winding temperature
        self.mcad.set_variable("MaxMagnet_MotorLAB", 160)  # Set magnet temperature
        self.mcad.set_variable("RotorTempDemand_Lab", 160)  # Set magnet temperature
        self.mcad.set_variable("SpeedDemand_MotorLAB", 4500)
        self.mcad.calculate_operating_point_lab()  # calculate operating point
        shaft_power = self.mcad.get_variable("LabOpPoint_ShaftPower")
        efficiency = self.mcad.get_variable("LabOpPoint_Efficiency")
        print("Shaft Power", round(shaft_power / 1000, 2), "kW")
        print("Efficiency", round(efficiency, 2), "%")

    def emag_calculation(self):
        self.mcad.show_magnetic_context()

        # Disable all performance tests except the ones for transient torque.
        self.mcad.set_variable("BackEMFCalculation", False)
        self.mcad.set_variable("CoggingTorqueCalculation", False)
        self.mcad.set_variable("ElectromagneticForcesCalc_OC", False)
        self.mcad.set_variable("TorqueSpeedCalculation", False)
        self.mcad.set_variable("DemagnetizationCalc", False)
        self.mcad.set_variable("ElectromagneticForcesCalc_Load", False)
        self.mcad.set_variable("InductanceCalc", False)
        self.mcad.set_variable("BPMShortCircuitCalc", False)
        self.mcad.set_variable("TorqueCalculation", True)

        self.mcad.do_magnetic_calculation()

    def export_settings(self):
        self.mcad.set_variable("AnsysExportFormat", 1)
        # 3D export
        self.mcad.set_variable("AnsysModelType", 1)
        self.mcad.set_variable("AnsysSolve", 1)
        self.mcad.set_variable("AnsysArcSegmentMethod", 0)
        self.mcad.set_variable("Ansys_MergeEntities", 0)
        self.mcad.set_variable("Ansys_WindingGroups", 0)
        self.mcad.set_variable("AnsysRotationDirection", 0)
        self.mcad.export_to_ansys_electronics_desktop(self.vbs_file_path)
