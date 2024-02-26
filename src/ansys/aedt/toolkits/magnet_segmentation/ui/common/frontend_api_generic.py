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

from dataclasses import FrozenInstanceError
import os
import sys
import time

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from pydantic import ValidationError
import qdarkstyle
import requests

from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import PropertiesUpdate
from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import ToolkitConnectionStatus
from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import ToolkitThreadStatus
from ansys.aedt.toolkits.magnet_segmentation.ui.common.frontend_ui import Ui_MainWindow
from ansys.aedt.toolkits.magnet_segmentation.ui.common.logger_handler import logger
from ansys.aedt.toolkits.magnet_segmentation.ui.common.models import be_properties
from ansys.aedt.toolkits.magnet_segmentation.ui.common.thread_manager import FrontendThread


class FrontendGeneric(QtWidgets.QMainWindow, Ui_MainWindow, FrontendThread):
    def __init__(self):
        logger.info("Frontend initialization...")
        super(FrontendGeneric, self).__init__()
        FrontendThread.__init__(self)

        self.setupUi(self)

        # Load toolkit icon
        self.images_path = os.path.join(os.path.dirname(__file__), "images")
        icon = self._load_icon(self.images_path)
        self.setWindowIcon(icon)

        # Set font style
        self.set_style(self)

        # UI Logger
        XStream.stdout().messageWritten.connect(lambda value: self.write_log_line(value))
        XStream.stderr().messageWritten.connect(lambda value: self.write_log_line(value))

    def set_title(self, toolkit_title):
        # Toolkit name
        self.setWindowTitle(toolkit_title)
        return True

    def write_log_line(self, value):
        self.log_text.insertPlainText(value + "\n")
        tc = self.log_text.textCursor()
        tc.setPosition(self.log_text.document().characterCount())
        self.log_text.setTextCursor(tc)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if 0 < value < 100:
            self.progress_bar.setStyleSheet(
                """
                QProgressBar {
                    background-color: transparent;  /* Set the background color */
                    color: #FFFFFF;  /* Set the text color */
                }
                QProgressBar::chunk {
                    background-color: #FF0000;  /* Set the progress color */
                }
            """
            )
        elif value == 100:
            self.progress_bar.setStyleSheet(
                """
                QProgressBar {
                    background-color: transparent;  /* Set the background color */
                    color: #FFFFFF;  /* Set the text color */
                 }
                QProgressBar::chunk {
                    background-color: #008000;  /* Set the progress color */
                }
                """
            )

        if self.progress_bar.isHidden():
            self.progress_bar.setVisible(True)

    def check_connection(self):
        try:
            logger.debug("Check backend connection")
            count = 0
            response = False
            while not response and count < 10:
                time.sleep(1)
                response = requests.get(self.url + "/health")
                count += 1

            if response.ok:
                logger.debug(response.json())
                return True
            logger.error(response.json())
            return False

        except requests.exceptions.RequestException as e:
            logger.error("Backend is not running.")
            return False

    def backend_busy(self):
        try:
            response = requests.get(self.url + "/status")
            res = response.ok and response.json() == ToolkitThreadStatus.BUSY.value
            return res
        except requests.exceptions.RequestException:
            self.write_log_line(f"Get backend status failed")
            return False

    def installed_versions(self):
        """Retrieve AEDT installed versions."""
        try:
            response = requests.get(self.url + "/installed_versions")
            if response.ok:
                versions = response.json()
                return versions
        except requests.exceptions.RequestException:
            self.write_log_line("Get AEDT installed versions failed")
            return False

    def get_properties(self):
        """Retrieve backend's properties."""
        logger.debug("Retrieving backend properties.")
        try:
            response = requests.get(self.url + "/properties")
            if response.ok:
                data = response.json()
                logger.debug("Updating the properties from backend.")
                try:
                    for key, value in data.items():
                        logger.info(f"Updating '{key}' with value {value}")
                        setattr(be_properties, key, value)
                    msg = PropertiesUpdate.SUCCESS.value
                    updated = True
                    logger.debug(msg)
                except FrozenInstanceError:
                    msg = PropertiesUpdate.FROZEN.value
                    updated = False
                    logger.error(msg)
                except ValidationError:
                    msg = PropertiesUpdate.VALIDATION_ERROR.value
                    updated = False
                    logger.error(msg)
                    logger.error(f"key {key} with value {value}")
            else:
                msg = PropertiesUpdate.EMPTY.value
                updated = False
                logger.debug(msg)
            return updated
        except requests.exceptions.RequestException:
            self.write_log_line("Get properties failed")

    def set_properties(self):
        """Assign stored backend properties to the backend internal data model."""
        try:
            requests.put(self.url + "/properties", json=be_properties.model_dump())
        except requests.exceptions.RequestException:
            self.write_log_line(f"Set properties failed")

    def change_thread_status(self):
        self.find_process_ids()
        logger.info("Frontend thread finished")
        self.update_progress(100)

    def browse_for_aedt_project(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        file_name, _ = dialog.getOpenFileName(
            self,
            "Open or create new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )
        if file_name:
            self.project_name.setText(file_name)
            self.get_properties()
            be_properties.active_project = file_name
            self.set_properties()

    def find_process_ids(self):
        self.process_id_combo.clear()
        self.process_id_combo.addItem("Create New Session")
        try:
            # Modify selected version
            self.get_properties()
            if self.aedt_version_combo.currentText():
                be_properties.aedt_version = self.aedt_version_combo.currentText()
            self.set_properties()

            response = requests.get(self.url + "/aedt_sessions")
            if response.ok:
                sessions = response.json()
                for session in sessions:
                    if session[1] == -1:
                        self.process_id_combo.addItem(f"Process {session[0]}")
                    else:
                        self.process_id_combo.addItem(f"Process {session[0]} on Grpc {session[1]}")
            return True
        except requests.exceptions.RequestException:
            self.write_log_line(f"Find AEDT sessions failed")
            return False

    # FXIME: add a loop to wait for the toolkit to be idle ?
    def find_design_names(self):
        try:
            response = requests.get(self.url + "/status")
            if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                self.design_aedt_combo.clear()
                response = requests.get(self.url + "/design_names")
                if response.ok:
                    designs = response.json()
                    for design in designs:
                        if list(design.values())[0] not in [
                            self.design_aedt_combo.itemText(i) for i in range(self.design_aedt_combo.count())
                        ]:
                            self.design_aedt_combo.addItem(list(design.values())[0])
                return True
            else:
                self.write_log_line(
                    f"Something is wrong, either the {ToolkitThreadStatus.CRASHED.value} "
                    f"or {ToolkitThreadStatus.UNKNOWN.value}"
                )
        except requests.exceptions.RequestException:
            self.write_log_line(f"Find AEDT designs failed")
            return False

    def launch_aedt(self):
        try:
            response = requests.get(self.url + "/status")
            if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                self.update_progress(0)
                response = requests.get(self.url + "/health")
                if response.ok and response.json() == str(ToolkitConnectionStatus(desktop=None)):
                    # FIXME: is that call needed ?
                    self.get_properties()
                    if be_properties.selected_process == 0:
                        be_properties.aedt_version = self.aedt_version_combo.currentText()
                        be_properties.non_graphical = True
                        if self.non_graphical_combo.currentText() == "False":
                            be_properties.non_graphical = False
                        if self.process_id_combo.currentText() == "Create New Session":
                            if not be_properties.active_project:
                                be_properties.selected_process = 0
                        else:
                            text_splitted = self.process_id_combo.currentText().split(" ")
                            if len(text_splitted) == 5:
                                be_properties.use_grpc = True
                                be_properties.selected_process = int(text_splitted[4])
                            else:
                                be_properties.use_grpc = False
                                be_properties.selected_process = int(text_splitted[1])
                        self.set_properties()

                    response = requests.post(self.url + "/launch_aedt")

                    if response.status_code == 200:
                        self.update_progress(50)
                        # Start the thread
                        self.running = True
                        logger.debug("Launching AEDT")
                        self.start()
                    else:
                        self.write_log_line(f"Failed backend call: {self.url}")
                        self.update_progress(100)
                else:
                    self.write_log_line(response.json())
                    self.update_progress(100)
            else:
                self.write_log_line(response.json())
                self.update_progress(100)
        except requests.exceptions.RequestException:
            self.write_log_line(f"Launch AEDT failed")
            return False

    def save_project(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        dialog.setFileMode(QtWidgets.QFileDialog.FileMode.AnyFile)
        dialog.setOption(QtWidgets.QFileDialog.Option.DontConfirmOverwrite, True)
        file_name, _ = dialog.getSaveFileName(
            self,
            "Save new aedt file",
            "",
            "Aedt Files (*.aedt)",
        )

        if file_name:
            try:
                response = requests.get(self.url + "/status")
                if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                    self.write_log_line("Please wait, toolkit running")
                elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                    self.project_name.setText(file_name)
                    self.update_progress(0)
                    response = requests.post(self.url + "/save_project", json=file_name)
                    if response.ok:
                        self.update_progress(50)
                        # Start the thread
                        self.running = True
                        logger.debug(f"Saving project: {file_name}")
                        self.start()
                        self.write_log_line("Saving project process launched")
                    else:
                        msg = f"Failed backend call: {self.url}"
                        logger.debug(msg)
                        self.write_log_line(msg)
                        self.update_progress(100)
                else:
                    self.write_log_line(response.json())
                    self.update_progress(100)
            except requests.exceptions.RequestException:
                self.write_log_line(f"Save project failed")
                return False

    def release_only(self):
        """Release desktop."""
        try:
            response = requests.get(self.url + "/status")

            if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                properties = {"close_projects": False, "close_on_exit": False}
                if self.close():
                    requests.post(self.url + "/close_aedt", json=properties)
            else:
                self.write_log_line(response.json())
                self.update_progress(100)
        except requests.exceptions.RequestException:
            self.write_log_line(f"Release of AEDT failed")

    def release_and_close(self):
        """Release and close desktop."""
        try:
            response = requests.get(self.url + "/status")
            if response.ok and response.json() == ToolkitThreadStatus.BUSY.value:
                self.write_log_line("Please wait, toolkit running")
            elif response.ok and response.json() == ToolkitThreadStatus.IDLE.value:
                properties = {"close_projects": True, "close_on_exit": True}
                if self.close():
                    requests.post(self.url + "/close_aedt", json=properties)
            else:
                self.write_log_line(response.json())
                self.update_progress(100)
        except requests.exceptions.RequestException:
            self.write_log_line(f"Release and close of AEDT failed")

    def on_cancel_clicked(self):
        self.close()

    @staticmethod
    def set_style(ui_obj):
        ui_obj.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))

    @staticmethod
    def set_font(ui_obj):
        ui_obj._font = QtGui.QFont()
        ui_obj._font.setPointSize(12)
        ui_obj.setFont(ui_obj._font)
        ui_obj.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyside6"))
        ui_obj.top_menu_bar.setFont(ui_obj._font)

    @staticmethod
    def _load_icon(images_path):
        icon = QtGui.QIcon()
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        icon.addFile(
            os.path.join(images_path, "logo_cropped.png"),
            QtCore.QSize(),
            QtGui.QIcon.Normal,
            QtGui.QIcon.On,
        )
        return icon


class XStream(QtCore.QObject):
    """User interface message streamer."""

    _stdout = None
    _stderr = None

    messageWritten = QtCore.Signal(str)

    def flush(self):
        """Pass."""
        pass

    def fileno(self):
        """File."""
        return -1

    def write(self, msg):
        """Write a message."""
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        """Info logger."""
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        """Error logger."""
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
