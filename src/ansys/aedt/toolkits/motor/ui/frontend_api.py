# import os.path

from pyaedt.generic.general_methods import _to_boolean
import requests

from ansys.aedt.toolkits.motor.backend.common.toolkit import ToolkitConnectionStatus
from ansys.aedt.toolkits.motor.backend.common.toolkit import ToolkitThreadStatus
from ansys.aedt.toolkits.motor.ui.common.frontend_api_generic import FrontendGeneric
from ansys.aedt.toolkits.motor.ui.common.logger_handler import logger
from ansys.aedt.toolkits.motor.ui.common.thread_manager import FrontendThread


class ToolkitFrontend(FrontendThread, FrontendGeneric):
    def __init__(self):
        FrontendThread.__init__(self)
        FrontendGeneric.__init__(self)

    def apply_segmentation(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        properties = self.get_properties()
        properties["MotorType"] = self.motor_type_combo.currentText()
        properties["IsSkewed"] = _to_boolean(self.is_skewed.currentText())
        properties["MagnetsMaterial"] = self.magnets_material.currentText()
        properties["RotorMaterial"] = self.rotor_material.currentText()
        properties["StatorMaterial"] = self.stator_material.currentText()
        properties["RotorSlices"] = self.rotor_slices.text()
        properties["MagnetsSegmentsPerSlice"] = self.magnet_segments_per_slice.text()
        properties["SkewAngle"] = self.skew_angle.text()
        properties["SetupToAnalyze"] = self.setup_to_analyze.text()
        # FIXME: activate design should be str not dict
        properties["active_design"] = {"Maxwell3d": self.design_aedt_combo.currentText()}
        self.set_properties(properties)

        self.update_progress(0)
        segmentation_response = requests.post(self.url + "/apply_segmentation")
        if segmentation_response.ok:
            # self.update_progress(50)
            # Start the thread
            # self.running = True
            # self.start()
            self.find_design_names()
            self.skew.setEnabled(True)
            msg = "Apply segmentation call successful"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
        else:
            msg = f"Failed backend call: {self.url}"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
            return

    def apply_skew(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        properties = self.get_properties()
        if not properties["IsSkewed"] and properties["SkewAngle"]:
            self.update_progress(0)
            response = requests.post(self.url + "/apply_skew")
            if response.ok:
                # self.update_progress(50)
                # Start the thread
                # self.running = True
                # self.start()
                self.is_skewed.setCurrentText("True")
                properties["IsSkewed"] = True
                self.set_properties(properties)
                msg = "Apply skew call successful"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)
            else:
                msg = f"Failed backend call: {self.url}"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)
                return
        else:
            msg = f"Failed backend call: {self.url}"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
            return

    def hide_options(self):
        if self.is_skewed.currentText() == "True":
            self.rotor_material.setEnabled(False)
            self.stator_material.setEnabled(False)
            self.rotor_slices.setEnabled(False)
            self.skew_angle.setEnabled(False)
        else:
            self.rotor_material.setEnabled(True)
            self.stator_material.setEnabled(True)
            self.rotor_slices.setEnabled(True)
            self.skew_angle.setEnabled(True)

    def get_materials(self):
        response = requests.get(self.url + "/status")

        if response.ok and response.json() == str(ToolkitThreadStatus.BUSY):
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == str(ToolkitThreadStatus.IDLE):
            self.update_progress(0)
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == str(ToolkitConnectionStatus):
                response = requests.get(self.url + "/project_materials")
                if response.ok:
                    return response.json()
