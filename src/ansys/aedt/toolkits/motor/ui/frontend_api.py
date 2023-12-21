import os.path

from pyaedt.generic.general_methods import _to_boolean
import requests

from ansys.aedt.toolkits.motor.ui.common.frontend_api_generic import FrontendGeneric
from ansys.aedt.toolkits.motor.ui.common.logger_handler import logger
from ansys.aedt.toolkits.motor.ui.common.properties import be_properties


class ToolkitFrontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def apply_segmentation(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        self.get_properties()
        be_properties.motor_type = self.motor_type_combo.currentText()
        be_properties.is_skewed = _to_boolean(self.is_skewed.currentText())
        be_properties.magnets_material = self.magnets_material.currentText()
        be_properties.rotor_material = self.rotor_material.currentText()
        be_properties.stator_material = self.stator_material.currentText()
        be_properties.rotor_slices = self.rotor_slices.text()
        be_properties.magnet_segments_per_slice = self.magnet_segments_per_slice.text()
        be_properties.skew_angle = self.skew_angle.text()
        be_properties.setup_to_analyze = self.setup_to_analyze.text()
        be_properties.active_design = {"Maxwell3d": self.design_aedt_combo.currentText()}
        # self.set_properties()

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

        self.get_properties()
        if not be_properties.is_skewed and properties["SkewAngle"]:
            self.update_progress(0)
            response = requests.post(self.url + "/apply_skew")
            if response.ok:
                # self.update_progress(50)
                # Start the thread
                # self.running = True
                # self.start()
                self.is_skewed.setCurrentText("True")
                be_properties.is_skewed = True
                self.set_properties()
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
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend is running.":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend is free.":
            self.update_progress(0)
            response = requests.get(self.url + "/health")
            if response.ok and response.json() == "Toolkit not connected to AEDT":
                properties = self.get_properties()
                response = requests.get(self.url + "/get_project_materials")
                if response.ok:
                    return response.json()

    def export_vbs(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        properties = self.get_properties()
        file_path_wo_extension = os.path.splitext(properties["MotorCAD_filepath"])[0]
        properties["vbs_file_path"] = "{}.vbs".format(file_path_wo_extension)
        self.set_properties(properties)

        self.update_progress(0)
        response = requests.post(self.url + "/export_model")
        if response.ok:
            self.update_progress(50)
            # Start the thread
            self.running = True
            self.start()
            msg = "Export Motor-CAD model in AEDT successful"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
        else:
            msg = f"Failed backend call: {self.url}"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
            return

    def set_emag_model(self):
        response = requests.get(self.url + "/get_status")

        if response.ok and response.json() == "Backend is running.":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend is free.":
            response = requests.post(self.url + "/set_Emag_model")
            if response.ok:
                self.write_log_line("E-Mag model correctly set.")
            else:
                self.write_log_line("E-Mag model failed.")
        else:
            self.write_log_line(response.json())
            self.update_progress(100)
