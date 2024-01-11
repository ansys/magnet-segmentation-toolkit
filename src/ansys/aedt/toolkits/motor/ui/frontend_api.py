# import os.path

from pyaedt.generic.general_methods import _to_boolean
import requests

from ansys.aedt.toolkits.motor.backend.common.toolkit import ToolkitThreadStatus
from ansys.aedt.toolkits.motor.ui.common.frontend_api_generic import FrontendGeneric
from ansys.aedt.toolkits.motor.ui.common.logger_handler import logger
from ansys.aedt.toolkits.motor.ui.common.models import be_properties


class ToolkitFrontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def apply_segmentation(self):
        if self.backend_busy():
            msg = ToolkitThreadStatus.BUSY.value
            logger.debug(msg)
            self.write_log_line(msg)
            return

        self.get_properties()
        be_properties.motor_type = self.motor_type_combo.currentText()
        be_properties.is_skewed = _to_boolean(self.is_skewed.currentText())
        if not be_properties.is_skewed:
            be_properties.rotor_material = self.rotor_material.currentText()
            be_properties.stator_material = self.stator_material.currentText()
            be_properties.rotor_slices = int(self.rotor_slices.text())
            be_properties.skew_angle = self.skew_angle.text()
        be_properties.apply_mesh_sheets = _to_boolean(self.apply_mesh_sheets.currentText())
        be_properties.magnets_material = self.magnets_material.currentText()
        be_properties.magnet_segments_per_slice = int(self.magnet_segments_per_slice.text())
        be_properties.mesh_sheets_number = int(self.mesh_sheets_number.text())
        # be_properties.setup_to_analyze = self.setup_to_analyze.text()
        be_properties.active_design = {"Maxwell3d": self.design_aedt_combo.currentText()}
        self.set_properties()

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
            msg = ToolkitThreadStatus.BUSY.value
            logger.debug(msg)
            self.write_log_line(msg)
            return

        self.get_properties()
        if be_properties.is_skewed:
            msg = "Model is already skewed."
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
            return
        else:
            if be_properties.skew_angle:
                self.update_progress(0)
                response = requests.post(self.url + "/apply_skew")
                if response.ok:
                    # self.update_progress(50)
                    # Start the thread
                    # self.running = True
                    # self.start()
                    self.is_skewed.setCurrentText("True")
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

        if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
            self.update_progress(0)
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit is not connected to AEDT.":
                response = requests.get(self.url + "/project_materials")
                if response.ok:
                    return response.json()
        else:
            self.write_log_line(
                f"Something is wrong, either the {ToolkitThreadStatus.CRASHED.value} "
                f"or {ToolkitThreadStatus.UNKNOWN.value}"
            )
