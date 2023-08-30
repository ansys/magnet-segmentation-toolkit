from pyaedt.generic.general_methods import _to_boolean
import requests

from ansys.aedt.toolkits.motor.ui.common.frontend_api_generic import FrontendGeneric
from ansys.aedt.toolkits.motor.ui.common.logger_handler import logger
from ansys.aedt.toolkits.motor.ui.common.thread_manager import FrontendThread


class ToolkitFrontend(FrontendThread, FrontendGeneric):
    def __init__(self):
        FrontendThread.__init__(self)
        FrontendGeneric.__init__(self)

    def apply_segmentation_and_skew(self):
        if self.backend_busy():
            msg = "Toolkit running"
            logger.debug(msg)
            self.write_log_line(msg)
            return

        properties = self.get_properties()
        properties["IsSkewed"] = _to_boolean(self.is_skewed.currentText())
        properties["MagnetsMaterial"] = self.magnets_material.text()
        properties["RotorMaterial"] = self.rotor_material.text()
        properties["RotorSlices"] = self.rotor_slices.text()
        properties["MagnetsSegmentsPerSlice"] = self.magnet_segments_per_slice.text()
        properties["SkewAngle"] = self.skew_angle.text()
        properties["SetupToAnalyze"] = self.setup_to_analyze.text()

        self.set_properties(properties)

        self.update_progress(0)
        init_response = requests.post(self.url + "/init_aedt")
        if init_response.ok:
            self.update_progress(25)
            # Start the thread
            self.running = True
            self.start()
            msg = "Connect toolkit to AEDT.."
            logger.debug(msg)
            segmentation_response = requests.post(self.url + "/apply_segmentation")
            if segmentation_response.ok:
                self.update_progress(50)
                # Start the thread
                self.running = True
                self.start()
                msg = "Apply segmentation call launched"
                logger.debug(msg)
                self.write_log_line(msg)
            else:
                msg = f"Failed backend call: {self.url}"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)

            if not properties["IsSkewed"] and float(properties["SkewAngle"]):
                self.update_progress(0)
                response = requests.post(self.url + "/apply_skew")

                if response.ok:
                    self.update_progress(50)
                    # Start the thread
                    self.running = True
                    self.start()
                    msg = "Apply skew call launched"
                    logger.debug(msg)
                    self.write_log_line(msg)
                else:
                    msg = f"Failed backend call: {self.url}"
                    logger.debug(msg)
                    self.write_log_line(msg)
                    self.update_progress(100)
        else:
            msg = f"Failed backend call: {self.url}"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)

    def hide_options(self):
        if self.is_skewed.currentText() == "True":
            self.rotor_material.setEnabled(False)
            self.rotor_slices.setEnabled(False)
            self.skew_angle.setEnabled(False)
        else:
            self.rotor_material.setEnabled(True)
            self.rotor_slices.setEnabled(True)
            self.skew_angle.setEnabled(True)
