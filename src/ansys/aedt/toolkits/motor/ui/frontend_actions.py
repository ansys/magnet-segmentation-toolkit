import os
import sys

from PySide6 import QtWidgets

from ansys.aedt.toolkits.motor.ui.common.logger_handler import logger
from ansys.aedt.toolkits.motor.ui.common.properties import be_properties
from ansys.aedt.toolkits.motor.ui.common.properties import general_settings
from ansys.aedt.toolkits.motor.ui.frontend_api import ToolkitFrontend

os.environ["QT_API"] = "pyside6"

# User inputs
toolkit_title = "Motor Toolkit Wizard"

# Backend URL and port
url = general_settings.backend_url
port = general_settings.backend_port


class ApplicationWindow(ToolkitFrontend):
    def __init__(self):
        ToolkitFrontend.__init__(self)

        self.url = f"http://{url}:{port}"

        # Set title
        self.set_title(toolkit_title)

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
            # elif self.backend:
            #     self.aedt_version_combo.addItem("AEDT not installed")

            if hasattr(be_properties, "aedt_version") and be_properties.aedt_version in installed_versions:
                self.aedt_version_combo.setCurrentText(be_properties.aedt_version)

            self.find_process_ids()

            # Add default properties
            self.non_graphical_combo.setCurrentText(str(be_properties.non_graphical))
            self.numcores.setText(str(be_properties.core_number))

            # Launch AEDT
            if hasattr(be_properties, "selected_process") and be_properties.selected_process:
                self.launch_aedt()

        # Thread signal
        self.status_changed.connect(self.change_thread_status)

        # Select AEDT project
        self.browse_project.clicked.connect(self.browse_for_aedt_project)

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
