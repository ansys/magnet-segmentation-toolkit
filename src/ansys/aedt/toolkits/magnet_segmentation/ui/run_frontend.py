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

# PySide6 Widgets
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow

# ToolkitBackend frontend API
from actions import Frontend
from ansys.aedt.toolkits.common.ui.common_windows.home_menu import HomeMenu
from ansys.aedt.toolkits.common.ui.common_windows.settings_column import SettingsMenu

# Import general common frontend modules
from ansys.aedt.toolkits.common.ui.logger_handler import logger

# Common windows
from ansys.aedt.toolkits.common.ui.main_window.main_window_layout import MainWindowLayout

# Default user interface properties
from models import properties
from windows.plot_design.plot_design_menu import PlotDesignMenu
from windows.post_processing.post_processing_menu import PostProcessingMenu

# New windows
from windows.segmentation.segmentation_menu import SegmentationMenu

# Windows


# Backend URL and port
url = properties.backend_url
port = properties.backend_port

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

if properties.high_resolution:
    os.environ["QT_SCALE_FACTOR"] = "2"


class ApplicationWindow(QMainWindow, Frontend):
    def __init__(self):
        super().__init__()

        self.thread = None
        self.properties = properties

        # General Settings

        # Create main window layout
        self.ui = MainWindowLayout(self)
        self.ui.setup()

        # Settings menu
        self.settings_menu = SettingsMenu(self)
        self.settings_menu.setup()

        # Check backend connection
        success = self.check_connection()

        if not success:
            msg = "Error getting properties from backend. User interface running without backend"
            self.ui.update_logger(msg)
            logger.error(msg)
            self.settings_menu.signal_flag = False
            self.settings_menu.aedt_version.addItem("Backend OFF")
            self.settings_menu.aedt_session.addItem("Backend OFF")
        else:
            # Get default properties
            be_properties = self.get_properties()
            # Get AEDT installed versions
            installed_versions = self.installed_versions()

            self.settings_menu.aedt_session.clear()
            self.settings_menu.aedt_session.addItem("New Session")
            if installed_versions:
                self.settings_menu.connect_aedt.setEnabled(True)
                for ver in installed_versions:
                    self.settings_menu.aedt_version.addItem(ver)
            else:
                self.settings_menu.aedt_version.addItem("AEDT not installed")

            if be_properties.get("aedt_version") in installed_versions:
                self.settings_menu.aedt_version.setCurrentText(be_properties.get("aedt_version"))

        # Custom toolkit setup starts here

        # Home menu
        self.home_menu = HomeMenu(self)
        self.home_menu.setup()

        # Segmentation menu
        self.segmentation_menu = SegmentationMenu(self)
        self.segmentation_menu.setup()
        self.ui.left_menu.clicked.connect(self.segmentation_menu_clicked)

        # Post-processing menu
        self.post_processing_menu = PostProcessingMenu(self)
        self.post_processing_menu.setup()
        self.ui.left_menu.clicked.connect(self.post_processing_menu_clicked)

        # Plot design menu
        self.plot_design_menu = PlotDesignMenu(self)
        self.plot_design_menu.setup()
        self.ui.left_menu.clicked.connect(self.plot_design_menu_clicked)

        # Home page as first page
        self.ui.set_page(self.ui.load_pages.home_page)

    def segmentation_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "segmentation_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.segmentation_menu.segmentation_menu_widget)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.segmentation_menu.segmentation_column_widget,
                title="Segmentation",
                icon_path=self.ui.images_load.icon_path("motor.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

            # Check backend connection
            success = self.check_connection()

            if success:
                # msg = "Loading materials..."
                # self.ui.update_logger(msg)
                # logger.info(msg)
                self.segmentation_menu.get_materials()

    def post_processing_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "post_processing_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.post_processing_menu.postprocessing_menu_widget)

            is_left_visible = self.ui.is_left_column_visible()

            self.ui.set_left_column_menu(
                menu=self.post_processing_menu.postprocessing_column_widget,
                title="PostProcessing",
                icon_path=self.ui.images_load.icon_path("icon_plot_2d.svg"),
            )

            if not is_left_visible:
                self.ui.toggle_left_column()

            # Check backend connection
            success = self.check_connection()

            if success:
                # msg = "Loading setups..."
                # self.ui.update_logger(msg)
                # logger.info(msg)
                self.post_processing_menu.get_setups()

    def plot_design_menu_clicked(self):
        selected_menu = self.ui.get_selected_menu()
        menu_name = selected_menu.objectName()

        if menu_name == "plot_design_menu":
            selected_menu.set_active(True)
            self.ui.set_page(self.plot_design_menu.plot_design_menu_widget)

            self.ui.set_left_column_menu(
                menu=self.plot_design_menu.plot_design_column_widget,
                title="Plot Design",
                icon_path=self.ui.images_load.icon_path("cylindrical_data_graphic.svg"),
            )

            is_left_visible = self.ui.is_left_column_visible()
            if not is_left_visible:
                self.ui.toggle_left_column()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
