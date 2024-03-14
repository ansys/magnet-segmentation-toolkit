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

from ansys.aedt.toolkits.common.backend.api import ToolkitThreadStatus
from ansys.aedt.toolkits.common.ui.actions_generic import FrontendGeneric
from ansys.aedt.toolkits.common.ui.logger_handler import logger
import requests


class Frontend(FrontendGeneric):
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

        aedt_file = self.file.text()
        with open(aedt_file, "r") as file:
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

        be_properties = self.get_properties()
        with open(be_properties.active_project, "r") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]

        for i in range(len(lines) - len(SHAFT_LINES) + 1):
            if lines[i : i + len(SHAFT_LINES)] == SHAFT_LINES:
                logger.debug("Selected AEDT file is compatible with skew call")
                return True

        logger.debug("Selected AEDT file is not compatible with skew call")
        return False

    # NOTE: It might be wise to disable the buttons to perform some actions.
    # This depends on the content of the file (see segmentation_page.py)
    def browse_file(self):
        """Browse file and perform checks on the fly."""
        super().browse_file()
        aedt_file = self.file.text()
        if not self.check_segmentation_compatibility():
            logger.warning(
                f"AEDT file '{aedt_file}' is not compatible with segmentation. "
                "Please, ensure that 'SymmetryFactor' and 'HalfAxial' are defined"
            )
        if not self.check_skew_compatibility():
            logger.warning(
                f"AEDT file '{aedt_file}' is not compatible with skew. "
                "Please, ensure that the name of the shaft is 'Shaft'"
            )

    def apply_segmentation(self, project_selected=None, design_selected=None):
        be_properties = self.get_properties()
        if project_selected and design_selected:
            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            msg = "Please load a valid AEDT project."
            logger.info(msg)

        self.set_properties(be_properties)
        try:
            segmentation_response = requests.post(self.url + "/apply_segmentation")
            if segmentation_response.ok:
                # self.find_design_names()
                # self.skew.setEnabled(True)
                msg = "Apply segmentation call successful"
                logger.info(msg)
            else:
                msg = f"Apply segmentation call failed"
                logger.error(msg)
        except requests.exceptions.RequestException:
            logger.error("Apply segmentation call failed")

    def apply_skew(self, project_selected=None, design_selected=None):
        be_properties = self.get_properties()
        if project_selected and design_selected:
            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            msg = "Please load a valid AEDT project."
            logger.info(msg)

        self.set_properties(be_properties)

        if be_properties["is_skewed"]:
            msg = "Model is already skewed."
            logger.info(msg)
            return

        if be_properties["skew_angle"]:
            try:
                response = requests.post(self.url + "/apply_skew")
                if response.ok:
                    self.is_skewed.setCurrentText("True")
                    msg = "Apply skew call successful."
                    logger.info(msg)
                else:
                    msg = "Apply skew call failed."
                    logger.error(msg)
            except requests.exceptions.RequestException:
                logger.error("Apply skew call failed.")

    def val_check_and_analysis(self, project_selected=None, design_selected=None):
        be_properties = self.get_properties()
        if project_selected and design_selected:
            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            msg = "Please load a valid AEDT project."
            logger.info(msg)

        # check box name setup
        be_properties.setup_to_analyze = self.setup_name.text()
        self.set_properties(be_properties)

        try:
            response = requests.post(self.url + "/validate_analyze")
            if response.ok:
                msg = "Validate and analyze call successful"
                logger.info(msg)
                # self.get_magnet_loss.setEnabled(True)
            else:
                msg = "Validate and analyze call failed"
                logger.error(msg)
        except requests.exceptions.RequestException:
            logger.error("Validate and analyze call failed")

    def get_report(self, project_selected=None, design_selected=None):
        be_properties = self.get_properties()
        if project_selected and design_selected:
            for project in be_properties["project_list"]:
                if self.get_project_name(project) == project_selected:
                    be_properties["active_project"] = project
                    if project_selected in list(be_properties["design_list"].keys()):
                        designs = be_properties["design_list"][project_selected]
                        for design in designs:
                            if design_selected == design:
                                be_properties["active_design"] = design
                                break
                    break
        else:
            msg = "Please load a valid AEDT project."
            logger.info(msg)

        self.set_properties(be_properties)

        try:
            response = requests.get(self.url + "/magnet_loss")
            if response.ok:
                msg = "Magnet loss call successful."
                logger.info(msg)
            else:
                msg = "Magnet loss call failed."
                logger.error(msg)
        except requests.exceptions.RequestException:
            logger.error("Magnet loss call failed.")

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
                if response.ok and response.json() == "ToolkitBackend is not connected to AEDT.":
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

    def get_design_setups(self):
        try:
            response = requests.get(self.url + "/status")
            if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                self.update_progress(0)
                response = requests.get(self.url + "/health")
                if response.ok and response.json() == "Toolkit is not connected to AEDT.":
                    response = requests.get(self.url + "/design_setups")
                    if response.ok:
                        return response.json()
            else:
                self.write_log_line(
                    f"Something is wrong, either the {ToolkitThreadStatus.CRASHED.value} "
                    f"or {ToolkitThreadStatus.UNKNOWN.value}"
                )
        except requests.exceptions.RequestException:
            logger.error(f"Get setups call failed")
