import os
import ansys.motorcad.core as pymotorcad
import tempfile
from ansys.aedt.toolkits.motor.backend.common.api_generic import ToolkitGeneric
from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.common.properties import properties
from ansys.aedt.toolkits.motor.backend.common.api_generic import thread


class Toolkit(ToolkitGeneric):
    """Template API to control the toolkit workflow.

    This class provides methods to connect to a selected design and create geometries.

    Examples
    --------
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> import time
    >>> service = Toolkit()
    >>> msg1 = service.launch_aedt()
    >>> response = service.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = service.get_thread_status()
    >>> msg3 = service.create_geometry()
    >>> response = service.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = service.get_thread_status()
    """

    def __init__(self):
        ToolkitGeneric.__init__(self)
        self.mcad = None

    @property
    def vbs_file_path(self):
        """Path to .vbs file exported from Motor-CAD."""
        motorcad_filepath = properties.MotorCAD_filepath
        if not motorcad_filepath:
            return False
        return os.path.join(
            motorcad_filepath,
            "{}.vbs".format(os.path.splitext(motorcad_filepath)[0]),
        )

    @thread.launch_thread
    def init_motorcad(self):
        """Initialize MotorCAD."""
        if not self.mcad:
            self.mcad = pymotorcad.MotorCAD()
            self.mcad.set_variable("MessageDisplayState", 2)
            logger.debug("MotorCAD initialized")
            return True
        else:
            logger.debug("MotorCAD was already active")
            return False

    def load_mcad_file(self):
        """Load a .mot file."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        motorcad_filepath = properties.MotorCAD_filepath
        if not motorcad_filepath:
            new_mot_path = os.path.join(tempfile.gettempdir(), "toolkit.mot")
            self.mcad.save_to_file(new_mot_path)
            properties.MotorCAD_filepath = new_mot_path
            logger.debug("MotorCAD file not specified, loaded default one")

        logger.debug("MotorCAD file loaded")
        self.mcad.load_from_file(properties.MotorCAD_filepath)
        return True

    def set_geometry_model(self):
        """Set geometry model."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.show_magnetic_context()
        self.mcad.display_screen("Scripting")
        self.mcad.set_variable(
            "ProximityLossModel", properties.E_mag_settings["AC_Winding_Loss_Model"]
        )
        self.mcad.set_variable(
            "NumberOfCuboids", properties.E_mag_settings["Number_of_Cuboids"]
        )
        self.mcad.set_variable("AxialSegments", properties.Geometry["Magnet_Axial_Segments"])

        self.mcad.save_to_file(properties.MotorCAD_filepath)
        return True

    def lab_performance_calculation(self):
        """Calculate lab performance curves-Maximum Torque-speed and Efficiency Map."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False

        self.mcad.set_variable("EmagneticCalcType_Lab", 0)
        self.mcad.set_variable("SpeedMax_MotorLAB", properties.LAB_settings["Max_Speed"])
        self.mcad.set_variable("SpeedMin_MotorLAB", properties.LAB_settings["Speed_Min"])
        self.mcad.set_variable("Speedinc_MotorLAB", properties.LAB_settings["Speed_Step"])
        self.mcad.set_variable("OperatingMode_Lab", properties.LAB_settings["Max_TS_Curve"])
        self.mcad.calculate_magnetic_lab()
        return True

    def lab_operating_point(self):
        """Set lab operating point based on given input conditions."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.set_variable(
            "OpPointSpec_MotorLAB", properties.LAB_settings["OP_Def_Max_Temp"]
        )
        self.mcad.set_variable(
            "LabMagneticCoupling", properties.LAB_settings["OP_Link_Lab_Emag"]
        )
        self.mcad.set_variable(
            "ThermCalcType_MotorLAB", properties.LAB_settings["OP_Link_Lab_Thermal"]
        )
        self.mcad.set_variable(
            "ThermalMapType_Lab", properties.LAB_settings["Thermal_Envelop"]
        )
        self.mcad.set_variable(
            "MaxWindTemp_MotorLAB", properties.LAB_settings["Lab_Max_Temp_St_Wind"]
        )
        self.mcad.set_variable(
            "StatorTempDemand_Lab", properties.LAB_settings["Lab_Max_Temp_St_Wind"]
        )
        self.mcad.set_variable(
            "MaxMagnet_MotorLAB", properties.LAB_settings["Lab_Max_Temp_Magnet"]
        )
        self.mcad.set_variable(
            "RotorTempDemand_Lab", properties.LAB_settings["Lab_Max_Temp_Magnet"]
        )
        self.mcad.set_variable("SpeedDemand_MotorLAB", properties.LAB_settings["OP_Speed"])
        self.mcad.calculate_operating_point_lab()
        shaft_power = self.mcad.get_variable("LabOpPoint_ShaftPower")
        efficiency = self.mcad.get_variable("LabOpPoint_Efficiency")
        logger.debug("Shaft Power", round(shaft_power / 1000, 2), "kW")
        logger.debug("Efficiency", round(efficiency, 2), "%")
        return True

    def emag_calculation(self):
        """Set Emag calculation."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.show_magnetic_context()

        self.mcad.set_variable(
            "BackEMFCalculation", properties.E_mag_settings["Test_Back_EMF"]
        )
        self.mcad.set_variable(
            "CoggingTorqueCalculation", properties.E_mag_settings["Test_Cogging"]
        )
        self.mcad.set_variable(
            "ElectromagneticForcesCalc_OC", properties.E_mag_settings["Test_OC_Forces"]
        )
        self.mcad.set_variable(
            "TorqueSpeedCalculation", properties.E_mag_settings["Test_TS_curce"]
        )
        self.mcad.set_variable(
            "DemagnetizationCalc", properties.E_mag_settings["Test_Demag"]
        )
        self.mcad.set_variable(
            "ElectromagneticForcesCalc_Load", properties.E_mag_settings["Test_Load_Forces"]
        )
        self.mcad.set_variable(
            "InductanceCalc", properties.E_mag_settings["Test_Indcutances"]
        )
        self.mcad.set_variable(
            "BPMShortCircuitCalc", properties.E_mag_settings["Test_ShortCircuit"]
        )
        self.mcad.set_variable("TorqueCalculation", properties.E_mag_settings["Test_Torque"])
        self.mcad.set_variable(
            "MagneticThermalCoupling", properties.E_mag_settings["Emag_Thermal_Coupling"]
        )
        self.mcad.do_magnetic_calculation()

    def set_thermal(self, magnet_loss):
        """Set the motorcad thermal calculations, cooling and losses ."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.show_thermal_context()
        self.mcad.set_variable("ThermalCalcType", 0)
        self.mcad.set_variable("Magnet_Iron_Loss_@Ref_Speed", magnet_loss["SolidLoss"]["Value"])

    def thermal_calculation(self):
        """Perform  steady state thermal calculation."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.do_steady_state_analysis()
        variable = self.mcad.get_variable("Temp_Winding_Average")
        logger.debug("Avg Winding Temp " + str(variable))
        return variable

    def export_settings(self):
        """Set export settings."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.show_magnetic_context()
        self.mcad.set_variable("AnsysExportFormat", 1)
        self.mcad.set_variable("AnsysModelType", 1)
        self.mcad.set_variable("AnsysSolve", 1)
        self.mcad.set_variable("AnsysArcSegmentMethod", 0)
        self.mcad.set_variable("Ansys_MergeEntities", 0)
        self.mcad.set_variable("Ansys_WindingGroups", 0)
        self.mcad.set_variable("AnsysRotationDirection", 0)
        self.mcad.export_to_ansys_electronics_desktop(self.vbs_file_path)
        return self.vbs_file_path

    def save(self):
        """Save the motorcad file."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        path = properties.MotorCAD_filepath
        if path:
            self.mcad.save_to_file(path)
            return True
        else:
            logger.error("Path not specified")

    def close_motorcad(self):
        """Close the motorcad instance."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.quit()
        return True