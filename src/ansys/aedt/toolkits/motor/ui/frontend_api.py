import os.path

from pyaedt.generic.general_methods import _to_boolean
import requests

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
        properties["IsSkewed"] = _to_boolean(self.is_skewed.currentText())
        properties["MagnetsMaterial"] = self.magnets_material.currentText()
        properties["RotorMaterial"] = self.rotor_material.currentText()
        properties["StatorMaterial"] = self.stator_material.currentText()
        properties["RotorSlices"] = self.rotor_slices.text()
        properties["MagnetsSegmentsPerSlice"] = self.magnet_segments_per_slice.text()
        properties["SkewAngle"] = self.skew_angle.text()
        properties["SetupToAnalyze"] = self.setup_to_analyze.text()
        self.set_properties(properties)

        self.update_progress(0)
        segmentation_response = requests.post(self.url + "/apply_segmentation")
        if segmentation_response.ok:
            # self.update_progress(50)
            # Start the thread
            # self.running = True
            # self.start()
            msg = "Apply segmentation call successful"
            logger.debug(msg)
            self.write_log_line(msg)
            self.skew.setEnabled(True)
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
        if not properties["IsSkewed"] and float(properties["SkewAngle"]):
            self.update_progress(0)
            response = requests.post(self.url + "/apply_skew")
            if response.ok:
                # self.update_progress(50)
                # Start the thread
                # self.running = True
                # self.start()
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

        if response.ok and response.json() == "Backend running":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend free":
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

        if response.ok and response.json() == "Backend running":
            self.write_log_line("Please wait, toolkit running")
        elif response.ok and response.json() == "Backend free":
            response = requests.post(self.url + "/set_Emag_model")
            if response.ok:
                self.write_log_line("E-Mag model correctly set.")
            else:
                self.write_log_line("E-Mag model failed.")
        else:
            self.write_log_line(response.json())
            self.update_progress(100)
