# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# import os.path

from pyaedt.generic.general_methods import _to_boolean
import requests

from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import ToolkitThreadStatus
from ansys.aedt.toolkits.magnet_segmentation.ui.common.frontend_api_generic import FrontendGeneric
from ansys.aedt.toolkits.magnet_segmentation.ui.common.logger_handler import logger
from ansys.aedt.toolkits.magnet_segmentation.ui.common.models import be_properties


class ToolkitFrontend(FrontendGeneric):
    def __init__(self):
        FrontendGeneric.__init__(self)

    def check_segmentation_compatibility(self):
        """Check compatibility with segmentation call.

        An AEDT file is compatible with the segmentation call if it has defined
        design settings 'SymmetryFactor' and 'HalfAxial'.
        """
        SYMMETRY_FACTOR_BEGIN = "VariableProp('SymmetryFactor'"
        HALF_AXIAL_BEGIN = "VariableProp('HalfAxial'"
        found_data = {target: False for target in [SYMMETRY_FACTOR_BEGIN, HALF_AXIAL_BEGIN]}

        with open(be_properties.active_project, "r") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]

        for line in lines:
            for target in [SYMMETRY_FACTOR_BEGIN, HALF_AXIAL_BEGIN]:
                if line.lstrip().startswith(target):
                    found_data[target] = True

        res = all(found_data.values())
        if res:
            logger.debug("Selected AEDT file is compatible with segmentation call")
        else:
            logger.debug("Selected AEDT file is not compatible with segmentation call")
        return res

    def check_skew_compatibility(self):
        """Check compatibility with skew call.

        An AEDT file is compatible with the skew call if the name of the shaft
        is 'Shaft'.
        """
        SHAFT_LINES = ["$begin 'GeometryPart'", "$begin 'Attributes'", "Name='Shaft'"]
        with open(be_properties.active_project, "r") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]

        for i in range(len(lines) - len(SHAFT_LINES) + 1):
            if lines[i : i + len(SHAFT_LINES)] == SHAFT_LINES:
                logger.debug("Selected AEDT file is compatible with skew call")
                return True

        logger.debug("Selected AEDT file is not compatible with skew call")
        return False

    def browse_and_check_for_aedt_project(self):
        super().browse_for_aedt_project()
        segmentation_compatibility = self.check_segmentation_compatibility()
        if not segmentation_compatibility:
            self.write_log_line(
                f"[Warning] AEDT file '{be_properties.active_project}' is not compatible with segmentation."
            )
            self.write_log_line("Please, ensure that 'SymmetryFactor' and 'HalfAxial' are defined")
        skew_compatibility = self.check_skew_compatibility()
        if not skew_compatibility:
            self.write_log_line(f"[Warning] AEDT file '{be_properties.active_project}' is not compatible with skew.")
            self.write_log_line("Please, ensure that the name of the shaft is 'Shaft'")

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
        try:
            segmentation_response = requests.post(self.url + "/apply_segmentation")
            if segmentation_response.ok:
                self.find_design_names()
                self.skew.setEnabled(True)
                msg = "Apply segmentation call successful"
            else:
                msg = f"Apply segmentation call failed"
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
        except requests.exceptions.RequestException:
            logger.error("Apply segmentation call failed")

    def apply_skew(self):
        if self.backend_busy():
            msg = ToolkitThreadStatus.BUSY.value
            logger.debug(msg)
            self.write_log_line(msg)
            return

        # FIXME: do we need that call ?
        self.get_properties()
        if be_properties.is_skewed:
            msg = "Model is already skewed."
            logger.debug(msg)
            self.write_log_line(msg)
            self.update_progress(100)
            return

        if be_properties.skew_angle:
            self.update_progress(0)
            try:
                response = requests.post(self.url + "/apply_skew")
                if response.ok:
                    self.is_skewed.setCurrentText("True")
                    msg = "Apply skew call successful"
                else:
                    msg = "Apply skew call failed"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)
            except requests.exceptions.RequestException:
                logger.error("Apply skew call failed")

    def val_check_and_analysis(self):
        if self.backend_busy():
            msg = ToolkitThreadStatus.BUSY.value
            logger.debug(msg)
            self.write_log_line(msg)
            return

        self.get_properties()
        # check box name setup
        be_properties.setup_to_analyze = self.setup_name.text()
        self.set_properties()

        try:
            response = requests.post(self.url + "/validate_analyze")
            if response.ok:
                msg = "Validate and analyze call successful"
            else:
                msg = "Validate and analyze call failed"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)
        except requests.exceptions.RequestException:
            logger.error("Validate and analyze call failed")

    def get_report(self):
        if self.backend_busy():
            msg = ToolkitThreadStatus.BUSY.value
            logger.debug(msg)
            self.write_log_line(msg)
            return

        try:
            response = requests.get(self.url + "/magnet_loss")
            if response.ok:
                msg = "Magnet loss call successful"
            else:
                msg = "Magnet loss call failed"
                logger.debug(msg)
                self.write_log_line(msg)
                self.update_progress(100)
        except requests.exceptions.RequestException:
            logger.error("Magnet loss call failed")

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
        try:
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
        except requests.exceptions.RequestException:
            logger.error(f"Get materials call failed")
