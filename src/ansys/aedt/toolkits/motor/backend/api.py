from ansys.aedt.toolkits.motor.backend.motor_workflow.aedt_flow import Aedt_Flow
from ansys.aedt.toolkits.motor.backend.motor_workflow.motorcad_flow import MotorCAD_Flow


class Toolkit(MotorCAD_Flow, Aedt_Flow):
    """Template API to control the toolkit workflow.

    This class provides methods to connect to a selected design and create geometries.

    Examples
    --------
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> import time
    >>> toolkit = Toolkit()
    >>> toolkit.init_motorcad()
    >>> toolkit.load_mcad_file()
    >>> toolkit.close_motorcad()
    """

    def __init__(self):
        MotorCAD_Flow.__init__(self)
        Aedt_Flow.__init__(self)
