import os
import tempfile

import ansys.motorcad.core as pymotorcad

from ansys.aedt.toolkits.motor.backend.common.api_generic import ToolkitGeneric
from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.common.properties import properties


class MotorCADFlow(ToolkitGeneric):
    """API to control MotorCAD toolkit workflow.

    This class provides methods to initialize and control a MotorCAD design.

    Examples
    --------
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> import time
    >>> toolkit = Toolkit()
    >>> toolkit.init_motorcad()
    >>> toolkit.load_mcad_file()
    >>> toolkit.close_motorcad()
    """

    def __init__(self):
        ToolkitGeneric.__init__(self)
        self.mcad = None

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
            motorcad_filepath = os.path.join(tempfile.gettempdir(), "default.mot")
            self.mcad.save_to_file(motorcad_filepath)
            properties.MotorCAD_filepath = motorcad_filepath
            logger.debug("MotorCAD file not specified, default one has been loaded.")

        if not properties.vbs_file_path:
            properties.vbs_file_path = os.path.join(
                motorcad_filepath, "{}.vbs".format(os.path.splitext(motorcad_filepath)[0])
            )

        logger.debug("MotorCAD file loaded")
        self.mcad.load_from_file(properties.MotorCAD_filepath)
        return True

    def set_emag_model(self):
        """Set geometry model."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.show_magnetic_context()
        self.mcad.display_screen("Scripting")
        self.mcad.set_variable("ProximityLossModel", 1)
        self.mcad.set_variable("NumberOfCuboids", properties.E_mag_settings["NumberOfCuboids"])
        self.mcad.set_variable("AxialSegments", properties.Geometry["MagnetAxialSegments"])

        # self.mcad.save_to_file(properties.MotorCAD_filepath)
        return True

    def lab_performance_calculation(self):
        """Calculate lab performance curves-Maximum Torque-speed and Efficiency Map."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False

        self.mcad.set_variable("EmagneticCalcType_Lab", 0)
        self.mcad.set_variable("SpeedMax_MotorLAB", properties.LAB_settings["MaxSpeed"])
        self.mcad.set_variable("SpeedMin_MotorLAB", properties.LAB_settings["SpeedMin"])
        self.mcad.set_variable("Speedinc_MotorLAB", properties.LAB_settings["SpeedStep"])
        self.mcad.set_variable("OperatingMode_Lab", 0)
        self.mcad.calculate_magnetic_lab()
        return True

    def lab_operating_point(self):
        """Set lab operating point based on given input conditions."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
        self.mcad.set_variable("OpPointSpec_MotorLAB", 2)
        self.mcad.set_variable("LabMagneticCoupling", 1)
        self.mcad.set_variable("ThermCalcType_MotorLAB", 0)
        self.mcad.set_variable("ThermalMapType_Lab", 0)
        self.mcad.set_variable("MaxWindTemp_MotorLAB", properties.LAB_settings["MaxTempStatorWinding"])
        self.mcad.set_variable("StatorTempDemand_Lab", properties.LAB_settings["MaxTempStatorWinding"])
        self.mcad.set_variable("MaxMagnet_MotorLAB", properties.LAB_settings["MaxTempMagnet"])
        self.mcad.set_variable("RotorTempDemand_Lab", properties.LAB_settings["MaxTempMagnet"])
        self.mcad.set_variable("SpeedDemand_MotorLAB", properties.LAB_settings["OPSpeed"])
        self.mcad.calculate_operating_point_lab()
        shaft_power = self.mcad.get_variable("LabOpPoint_ShaftPower")
        efficiency = self.mcad.get_variable("LabOpPoint_Efficiency")
        logger.debug("Shaft Power: {} kW".format(str(round(shaft_power / 1000, 2))))
        logger.debug("Efficiency: {} %".format(str(round(efficiency, 2))))
        return True

    def emag_calculation(self):
        """Set Emag calculation."""
        if not self.mcad:
            logger.error("MotorCAD not initialized")
            return False
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
        self.mcad.set_variable("MagneticThermalCoupling", False)
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
        wdg_avg = self.mcad.get_variable("Temp_Winding_Average")
        logger.debug("Avg Winding Temp " + str(wdg_avg))
        return wdg_avg

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
        self.mcad.export_to_ansys_electronics_desktop(properties.vbs_file_path)
        return properties.vbs_file_path

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
