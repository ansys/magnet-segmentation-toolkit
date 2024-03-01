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

import os
import sys

from PySide6 import QtWidgets

from ansys.aedt.toolkits.magnet_segmentation.ui.common.logger_handler import logger
from ansys.aedt.toolkits.magnet_segmentation.ui.common.models import be_properties
from ansys.aedt.toolkits.magnet_segmentation.ui.common.models import general_settings
from ansys.aedt.toolkits.magnet_segmentation.ui.frontend_api import ToolkitFrontend

os.environ["QT_API"] = "pyside6"

# Constants
TOOLKIT_TITLE = "Magnet Segmentation Toolkit Wizard"

# Backend URL and port
url = general_settings.backend_url
port = general_settings.backend_port


class ApplicationWindow(ToolkitFrontend):
    def __init__(self):
        ToolkitFrontend.__init__(self)

        self.url = f"http://{url}:{port}"

        # Set title
        self.set_title(TOOLKIT_TITLE)

        # General Settings
        success = self.get_properties()
        if not success:
            logger.error("Error getting default properties from backend")
        else:
            # Get AEDT installed versions
            installed_versions = self.installed_versions()

            # Add versions to the UI
            if installed_versions:
                for ver in installed_versions:
                    self.aedt_version_combo.addItem(ver)

            if be_properties.aedt_version in installed_versions:
                self.aedt_version_combo.setCurrentText(be_properties.aedt_version)

            self.find_process_ids()

            # Add default properties
            self.non_graphical_combo.setCurrentText(str(be_properties.non_graphical))
            self.numcores.setText(str(be_properties.nb_core))

            # Launch AEDT
            if be_properties.selected_process:
                self.launch_aedt()

        # Thread signal
        self.status_changed.connect(self.change_thread_status)

        # Select AEDT project
        self.browse_project.clicked.connect(self.browse_and_check_for_aedt_project)

        # Close toolkit button
        self.release_button.clicked.connect(self.release_only)

        # Close toolkit and AEDT button
        self.release_and_exit_button.clicked.connect(self.release_and_close)

        # Find active AEDT sessions
        self.aedt_version_combo.currentTextChanged.connect(self.find_process_ids)

        # Change designs
        self.projects_aedt_combo.currentTextChanged.connect(self.find_design_names)

        self.connect_aedtapp.clicked.connect(self.launch_aedt)

        # If is_skewed combo box is True only magnets can be segmented
        # Rotor material, slices and skew angle are greyed out
        self.is_skewed.currentTextChanged.connect(self.hide_options)

        # Perform Segmentation
        self.perform_segmentation.clicked.connect(self.apply_segmentation)

        # Apply Skew
        self.skew.clicked.connect(self.apply_skew)

        # Validate and analyze design
        self.validate_and_analyze.clicked.connect(self.val_check_and_analysis)

        # Magnet loss report
        self.get_magnet_loss.clicked.connect(self.get_report)

        # Save project
        self.action_save_project.triggered.connect(lambda checked: self.save_project())

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(
            self, "QUIT", "Confirm quit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if close == QtWidgets.QMessageBox.Yes:
            logger.info("Closing toolkit")
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
