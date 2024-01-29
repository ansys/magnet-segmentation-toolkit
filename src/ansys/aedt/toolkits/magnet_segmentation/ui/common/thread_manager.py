import logging
import os

from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
import requests

from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import ToolkitThreadStatus
from ansys.aedt.toolkits.magnet_segmentation.ui.common.models import be_properties

# from ansys.aedt.toolkits.magnet_segmentation.ui.frontend_api import ToolkitFrontend

logger = logging.getLogger("Global")


class FrontendThread(QThread):
    status_changed = Signal(bool)
    running = True

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        while self.running:
            try:
                response = requests.get(self.url + "/status")
                if response.ok and response.json() != ToolkitThreadStatus.BUSY.value:
                    self.running = False
                    self.get_properties()
                    if be_properties.active_project and "projects_aedt_combo" in self.__dir__():
                        self.projects_aedt_combo.clear()
                        if not be_properties.projects:
                            self.projects_aedt_combo.addItem("No project")
                        else:
                            cont = 0
                            for project in be_properties.projects:
                                active_project_name = os.path.splitext(os.path.basename(project))[0]
                                self.projects_aedt_combo.addItem(active_project_name)
                                if active_project_name == os.path.splitext(os.path.basename(project))[0]:
                                    self.projects_aedt_combo.setCurrentIndex(cont)
                                cont += 1

                    if be_properties.active_design and "design_aedt_combo" in self.__dir__():
                        self.design_aedt_combo.clear()
                        if not be_properties.designs_by_project_name:
                            self.design_aedt_combo.addItem("No design")
                        else:
                            cont = 0
                            design_name = be_properties.active_design
                            active_design_list = be_properties.designs_by_project_name[active_project_name]
                            for design in active_design_list:
                                self.design_aedt_combo.addItem(list(design.values())[0])
                                if list(design_name.values())[0] == design:
                                    self.design_aedt_combo.setCurrentIndex(cont)
                                cont += 1
                    if (
                        "magnets_material" in self.__dir__()
                        and "rotor_material" in self.__dir__()
                        and "stator_material" in self.__dir__()
                        and be_properties.active_project
                    ):
                        mats = self.get_materials()
                        for mat in mats:
                            self.magnets_material.addItem(mat)
                            self.rotor_material.addItem(mat)
                            self.stator_material.addItem(mat)

                    self.motor_type_combo.addItems(["IPM", "SPM"])

                    # Emit the status_changed signal if the status changes
                    self.status_changed.emit(self.running)

                # Sleep for a certain amount of time before checking again
                self.msleep(200)
            except requests.exceptions.RequestException:
                logger.error(f"Front end thread error")
