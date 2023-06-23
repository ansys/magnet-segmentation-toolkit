from ansys.aedt.toolkits.motor.backend.common.api_generic import ToolkitGeneric
from ansys.aedt.toolkits.motor.backend.common.properties import properties


class Aedt_Flow(ToolkitGeneric):
    """API to control AEDT toolkit workflow.

    This class provides methods to connect to a selected design...

    Examples
    --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> import time
        >>> toolkit = Toolkit()
        >>> msg1 = toolkit.launch_aedt()
        >>> response = toolkit.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> new_property = {"vbs_path": "path\to\toolkit.vbs"}
        >>> toolkit.set_properties(new_property)
        >>> msg3 = toolkit.run_vbs()
        >>> response = toolkit.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
    """

    def __init__(self):
        ToolkitGeneric.__init__(self)

    def run_vbs(self):
        """Initialize Maxwell.

        If the .vbs script is provided it automatically runs it.
        If a Maxwell3D instance is provided it attaches to it.
        """

        # Connect AEDT
        self.connect_aedt()

        if properties.vbs_file_path:
            self.desktop.odesktop.RunScript(properties.vbs_file_path)
            # I need to understand the workflow, if an existing AEDT is open, is always creating a new project ?
            self._save_project_info()

        self.desktop.release_desktop(False, False)
        self.desktop = None
        return True
