from dataclasses import FrozenInstanceError
from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
import os
from typing import Optional

import psutil
import pyaedt

from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.common.properties import properties
from ansys.aedt.toolkits.motor.backend.common.thread_manager import ThreadManager

thread = ThreadManager()


class ToolkitThreadStatus(str, Enum):
    """Status of the toolkit thread."""

    IDLE = "Toolkit is idle and ready to accept a new task."
    BUSY = "Toolkit is busy and processing a task."
    CRASHED = "Toolkit has crashed and is not functional."
    UNKNOWN = "Toolkit unknown status."


class PropertiesUpdate(str, Enum):
    """Status of the toolkit thread."""

    EMPTY = "Body is empty."
    SUCCESS = "Properties updated successfully."
    FROZEN = "Properties are frozen, updated failed."


@dataclass
class ToolkitConnectionStatus:
    """Status of the toolkit connection."""

    desktop: Optional[pyaedt.Desktop]

    def __str__(self):
        if self.desktop:
            res = f"Toolkit is connected to process {self.desktop.aedt_process_id}"
            if self.desktop.port != 0:
                res += f" on Grpc {self.desktop.port}."
        else:
            res = "Toolkit is not connected to AEDT."
        return res

    def is_connected(self):
        return self.desktop is not None


class ToolkitGeneric(object):
    """Generic API to control the toolkits.

    It provides basic functions to control AEDT and properties to share between backend and frontend.

    Examples
    --------
    >>> import time
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> service = Toolkit()
    >>> properties = service.get_properties()
    >>> new_properties = {"aedt_version": "2022.2"}
    >>> service.set_properties(new_properties)
    >>> new_properties = service.get_properties()
    >>> msg = service.launch_aedt()
    >>> response = service.get_thread_status()
    >>> while response[0] == 0:
    >>>     time.sleep(1)
    >>>     response = service.get_thread_status()

    """

    def __init__(self):
        self.desktop = None
        self.aedtapp = None
        self.aedt_apps = {
            "Circuit Design": "Circuit",
            "HFSS": "Hfss",
            "EMIT": "Emit",
            "HFSS 3D Layout Design": "Hfss3dLayout",
            "Icepak": "Icepak",
            "Maxwell 2D": "Maxwell2d",
            "Maxwell 3D": "Maxwell3d",
            "Maxwell Circuit": "MaxwellCircuit",
            "2D Extractor": "Q2d",
            "Q3D Extractor": "Q3d",
            "RMxprt": "Rmxprt",
            "Twin Builder": "Simplorer",
            "Mechanical": "Mechanical",
        }

    @staticmethod
    def set_properties(data: dict):
        """Assign the passed data to the internal data model.

        Parameters
        ----------
        data : dict
            The dictionary containing the properties to be updated.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the success status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.set_properties({"property1": value1, "property2": value2})

        """
        logger.debug("Updating the internal properties.")
        if data:
            try:
                for key, value in data.items():
                    setattr(properties, key, value)
                msg = PropertiesUpdate.SUCCESS
                updated = True
                logger.debug(msg)
            except FrozenInstanceError:
                msg = PropertiesUpdate.FROZEN
                updated = False
                logger.error(msg)
        else:
            msg = PropertiesUpdate.EMPTY
            updated = False
            logger.debug(msg)
        return updated, msg

    @staticmethod
    def get_properties():
        """Get toolkit properties.

        Returns
        -------
        dict
            The dictionary containing the toolkit properties.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.get_properties()
        {"property1": value1, "property2": value2}
        """
        return asdict(properties)

    @staticmethod
    def get_thread_status() -> ToolkitThreadStatus:
        """Get toolkit thread status.

        Returns
        -------
        ToolkitThreadStatus
            ``ToolkitThreadStatus.BUSY`` when active, ``ToolkitThreadStatus.IDLE`` when inactive and \
            ``ToolkitThreadStatus.CRASHED`` when crashed.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.get_thread_status()
        """
        thread_running = thread.is_toolkit_thread_running()
        is_toolkit_busy = properties.general_properties.is_toolkit_busy
        if thread_running and is_toolkit_busy:  # pragma: no cover
            res = ToolkitThreadStatus.BUSY
            logger.debug(res)
            # msg = "Backend running"
            # logger.debug(msg)
            # return 0, msg
        elif (not thread_running and is_toolkit_busy) or (thread_running and not is_toolkit_busy):  # pragma: no cover
            res = ToolkitThreadStatus.CRASHED
            logger.error(res)
            # msg = "Backend crashed"
            # logger.error(msg)
            # return 1, msg
        else:
            res = ToolkitThreadStatus.IDLE
            logger.debug(res)
            # msg = "Backend free"
            # logger.debug(msg)
            # return -1, msg
        logger.debug(res)
        return res

    def aedt_connected(self):
        """Check if AEDT is connected.

        Returns
        -------
        tuple[bool, str]
            A tuple indicating the connection status and a message.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> msg = service.launch_aedt()
        >>> response = service.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_aedt()
        >>> service.aedt_connected()
        (True, "Toolkit connected to process <process_id> on Grpc <grpc_port>")
        >>> service.release_aedt()
        """
        tcs = ToolkitConnectionStatus(desktop=self.desktop)
        connected = tcs.is_connected()
        msg = str(tcs)
        logger.debug(msg)
        return connected, msg
        # if self.desktop:
        #     if self.desktop.port != 0:
        #         msg = "Toolkit connected to process {} on Grpc {}".format(
        #             str(self.desktop.aedt_process_id),
        #             str(self.desktop.port),
        #         )
        #         logger.debug(msg)
        #     else:
        #         msg = "Toolkit connected to process {}".format(str(self.desktop.aedt_process_id))
        #         logger.debug(msg)
        #     connected = True
        # else:
        #     msg = "Toolkit not connected to AEDT"
        #     logger.debug(msg)
        #     connected = False
        # return connected, msg

    @staticmethod
    def installed_aedt_version():
        """
        Return the installed AEDT versions.

        Returns
        -------
        list
            List of installed AEDT versions.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.installed_aedt_version()
        ["2021.1", "2021.2", "2022.1"]
        """

        # Detect existing AEDT installation
        installed_versions = []
        for ver in pyaedt.misc.list_installed_ansysem():
            installed_versions.append(
                "20{}.{}".format(ver.replace("ANSYSEM_ROOT", "")[:2], ver.replace("ANSYSEM_ROOT", "")[-1])
            )
        logger.debug(str(installed_versions))
        return installed_versions

    @staticmethod
    def aedt_sessions():
        """Get information for the active AEDT sessions.

        Returns
        -------
        list
            List of AEDT PIDs.

        Examples
        --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.aedt_sessions()
        [[pid1, grpc_port1], [pid2, grpc_port2]]
        """
        res = []
        if not properties.general_properties.is_toolkit_busy and properties.general_properties.aedt_version:
            keys = ["ansysedt.exe"]
            version = properties.general_properties.aedt_version
            if version and "." in version:
                version = version[-4:].replace(".", "")
            if version < "222":  # pragma: no cover
                version = version[:2] + "." + version[2]
            for p in filter(lambda p: p.name() in keys, psutil.process_iter()):
                try:
                    cmd = p.cmdline()
                    if version in cmd[0]:
                        try:
                            port = int(cmd[cmd.index("-grpcsrv") + 1])
                        except IndexError:
                            port = -1
                        res.append([p.pid, port])
                except:
                    pass
            logger.debug(str(res))
        else:
            logger.debug("No active sessions.")
        return res

    @staticmethod
    def get_design_names():
        """Get design names for a specific project, the first one is the active.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.get_design_names()
        """
        if properties.general_properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False

        design_list = []
        active_project = os.path.splitext(os.path.basename(properties.general_properties.active_project))[0]
        if active_project and active_project != "No project":
            for design in properties.design_list[active_project]:
                design_list.append(design)

            if (
                properties.general_properties.active_design
                and properties.general_properties.active_design in design_list
            ):
                index = design_list.index(properties.general_properties.active_design)
                design_list.insert(0, design_list.pop(index))
            else:
                design_list.append(properties.general_properties.active_design)

        return design_list

    @thread.launch_thread
    def launch_aedt(self):
        """Launch AEDT.

        This method is launched in a thread if grpc is enabled. AEDT is released once it is opened.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> toolkit_free = service.get_thread_status()
        """
        # Check if the backend is already connected to an AEDT session
        connected, msg = self.aedt_connected()
        if not connected:
            version = properties.general_properties.aedt_version
            non_graphical = properties.general_properties.non_graphical
            selected_process = properties.general_properties.selected_process
            use_grpc = properties.general_properties.use_grpc

            pyaedt.settings.use_grpc_api = use_grpc
            desktop_args = {
                "specified_version": version,
                "non_graphical": non_graphical,
            }

            # AEDT with COM
            if selected_process == 0:  # pragma: no cover
                desktop_args["new_desktop_session"] = True
            # AEDT with gRPC
            elif use_grpc:
                desktop_args["new_desktop_session"] = False
                desktop_args["port"] = selected_process
            else:  # pragma: no cover
                desktop_args["new_desktop_session"] = False
                desktop_args["aedt_process_id"] = selected_process
            self.desktop = pyaedt.Desktop(**desktop_args)

            if not self.desktop:
                msg = "AEDT not launched"
                logger.error(msg)
                return False

            msg = "AEDT launched"
            logger.debug(msg)

            # Open project
            if properties.general_properties.active_project:
                if not os.path.exists(properties.general_properties.active_project + ".lock"):  # pragma: no cover
                    self.open_project(os.path.abspath(properties.general_properties.active_project))
            elif properties.vbs_file_path:
                self.desktop.odesktop.RunScript(properties.vbs_file_path)

            # Save AEDT session properties
            if use_grpc:
                new_properties = {"selected_process": self.desktop.port}
                logger.debug("Grpc port {}".format(str(self.desktop.port)))
            else:
                new_properties = {"selected_process": self.desktop.aedt_process_id}
                logger.debug("Process ID {}".format(str(self.desktop.aedt_process_id)))
            self.set_properties(new_properties)

            self._save_project_info()

            self.desktop.release_desktop(False, False)
            self.desktop = None
            logger.debug("Desktop released and project properties loaded")

        return True

    def connect_aedt(self):
        """Connect to an existing AEDT session.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_aedt()
        >>> service.release_aedt()
        """
        if properties.general_properties.selected_process == 0:
            logger.error("Process ID not defined")
            return False

        version = properties.general_properties.aedt_version
        non_graphical = properties.general_properties.non_graphical
        selected_process = properties.general_properties.selected_process
        use_grpc = properties.general_properties.use_grpc

        # Connect to AEDT
        pyaedt.settings.use_grpc_api = use_grpc
        logger.debug("Connecting AEDT")
        desktop_args = {
            "specified_version": version,
            "non_graphical": non_graphical,
            "new_desktop_session": False,
        }
        if use_grpc:
            desktop_args["port"] = selected_process
        else:  # pragma: no cover
            desktop_args["aedt_process_id"] = selected_process
        self.desktop = pyaedt.Desktop(**desktop_args)

        if not self.desktop:  # pragma: no cover
            logger.debug("AEDT not connected")
            return False

        logger.debug("AEDT connected")
        return True

    def connect_design(self, app_name=None):
        """Connect to an application design.
        If a design exists, it takes the active project and design, if not,
        it creates a new design of the specified type. If no application specified, the default is ``"Hfss"``.

        Parameters
        ----------
        app_name : str
            Aedt application name. The default is connecting to active design. Application available are:

            * Circuit
            * Hfss
            * Edb
            * Emit
            * Hfss3dLayout
            * Icepak
            * Maxwell2d
            * Maxwell3d
            * Q2d
            * Q3d
            * Rmxprt
            * Simplorer

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_design()

        """

        project_name = os.path.splitext(os.path.basename(properties.general_properties.active_project))[0]
        design_name = "No design"
        if properties.general_properties.active_design:
            design_name = list(properties.general_properties.active_design.values())[0]
            if not app_name:
                app_name = list(properties.general_properties.active_design.keys())[0]

        pyaedt.settings.use_grpc_api = properties.general_properties.use_grpc

        # Select app
        if design_name != "No design":
            aedt_app = getattr(pyaedt, app_name)
            active_design = {app_name: design_name}
        elif app_name in list(self.aedt_apps.keys()):
            design_name = pyaedt.generate_unique_name(app_name)
            aedt_app = getattr(pyaedt, self.aedt_apps[app_name])
            active_design = {app_name: design_name}
        else:
            design_name = pyaedt.generate_unique_name("Hfss")
            aedt_app = pyaedt.Hfss
            active_design = {"Hfss": design_name}
        aedt_app_args = {
            "specified_version": properties.general_properties.aedt_version,
            "port": properties.general_properties.selected_process,
            "non_graphical": properties.general_properties.non_graphical,
            "new_desktop_session": False,
            "projectname": project_name,
            "designname": design_name,
        }
        if properties.general_properties.use_grpc:
            aedt_app_args["port"] = properties.general_properties.selected_process
        else:
            aedt_app_args["aedt_process_id"] = properties.general_properties.selected_process
        self.aedtapp = aedt_app(**aedt_app_args)

        if self.aedtapp:
            project_name = self.aedtapp.project_file
            if self.aedtapp.project_file not in properties.project_list:
                properties.project_list.append(project_name)
                properties.design_list[self.aedtapp.project_name] = [active_design]

            if self.aedtapp.design_list and active_design not in properties.design_list[self.aedtapp.project_name]:
                properties.design_list[self.aedtapp.project_name].append(active_design)
            properties.general_properties.active_project = project_name
            properties.general_properties.active_design = active_design
            return True
        else:
            return False

    def release_aedt(self, close_projects=False, close_on_exit=False):
        """Release AEDT.

        Parameters
        ----------
        close_projects : bool, optional
            Whether to close the AEDT projects that are open in the session.
            The default is ``False``.
        close_on_exit : bool, optional
            Whether to close the active AEDT session on exiting AEDT.
            The default is ``False``.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.release_aedt(True, True)

        """
        released = False
        if self.desktop:
            try:
                released = self.desktop.release_desktop(close_projects, close_on_exit)
                self.desktop = None
                self.aedtapp = None
            except:
                logger.error("Desktop not released")
                return False

        if self.aedtapp:
            try:
                released = self.aedtapp.release_desktop(close_projects, close_on_exit)
                self.aedtapp = None
            except:
                logger.error("Desktop not released")
                return False

        if not released and close_projects and close_on_exit:
            if self.connect_aedt():
                self.desktop.release_desktop(close_projects, close_on_exit)
        return True

    def open_project(self, project_name=None):
        """Open AEDT project.

        Parameters
        ----------
        project_name : str, optional
            Project path to open.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.open_project("path/to/file")
        >>> service.release_aedt()

        """
        if self.desktop and project_name:
            self.desktop.odesktop.OpenProject(project_name)
            logger.debug("Project {} opened".format(project_name))
            return True
        else:
            return False

    @thread.launch_thread
    def save_project(self, project_path=None):
        """Save project. It uses the properties to get the project path. This method is launched in a thread.

        Parameters
        ----------
        project_path : str, optional
            Path of the AEDT project to save.
            The default value is ``None`` in which case the current project will be overwritten.

        Returns
        -------
        bool
            Returns ``True`` if the connection is successful, ``False`` otherwise.

        Examples
        --------
        >>> import time
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> service = Toolkit()
        >>> service.launch_aedt()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = service.get_thread_status()
        >>> service.connect_aedt()
        >>> service.save_project()
        """
        if self.connect_design():
            if project_path and properties.general_properties.active_project != project_path:
                old_project_name = os.path.splitext(os.path.basename(properties.general_properties.active_project))[0]
                self.aedtapp.save_project(project_file=os.path.abspath(project_path))
                index = properties.project_list.index(properties.general_properties.active_project)
                properties.project_list.pop(index)
                properties.general_properties.active_project = project_path
                properties.project_list.append(project_path)
                new_project_name = os.path.splitext(os.path.basename(properties.general_properties.active_project))[0]
                properties.design_list[new_project_name] = properties.design_list[old_project_name]
                del properties.design_list[old_project_name]
            else:
                self.aedtapp.save_project()
            self.aedtapp.release_desktop(False, False)
            logger.debug("Project saved: {}".format(project_path))
            return True
        else:  # pragma: no cover
            logger.error("Project not saved")
            return False

    def _save_project_info(self):
        # Save project and design info
        new_properties = {}
        project_list = self.desktop.odesktop.GetProjectList()

        if project_list:
            new_properties["project_list"] = []
            active_project = self.desktop.odesktop.GetActiveProject()
            if not active_project:
                active_project = self.desktop.odesktop.SetActiveProject(project_list[0])
            active_project_name = active_project.GetName()
            active_design = active_project.GetActiveDesign()
            # Save active design info
            if active_design:
                active_design_name = active_design.GetName()
                active_design_name = (
                    active_design_name if ";" not in active_design_name else active_design_name.split(";")[1]
                )
                app_name = active_design.GetDesignType()
                if app_name in list(self.aedt_apps.keys()):
                    new_properties["active_design"] = {self.aedt_apps[app_name]: active_design_name}
                else:
                    logger.error("Application {} not available".format(app_name))
                    self.desktop.release_desktop(True, True)
                    return False

            # Save active project ingo
            active_project_path = active_project.GetPath()
            new_properties["active_project"] = os.path.join(active_project_path, active_project_name + ".aedt")
            # Save projects info
            new_properties["design_list"] = {}
            for project in project_list:
                oproject = self.desktop.odesktop.SetActiveProject(project)
                project_name = oproject.GetName()
                project_path = oproject.GetPath()
                logger.debug("Project name: {}".format(project_name))
                new_properties["project_list"].append(os.path.join(project_path, project_name + ".aedt"))

                new_properties["design_list"][project_name] = []

                design_list = oproject.GetChildNames()

                if design_list:
                    for design_name in design_list:
                        odesign = oproject.SetActiveDesign(design_name)
                        app_name = odesign.GetDesignType()
                        if app_name in list(self.aedt_apps.keys()):
                            new_properties["design_list"][project_name].append({self.aedt_apps[app_name]: design_name})
                        else:
                            logger.error("Application {} not available".format(app_name))
                            self.desktop.release_desktop(True, True)
                            return False

        if new_properties:
            self.set_properties(new_properties)
