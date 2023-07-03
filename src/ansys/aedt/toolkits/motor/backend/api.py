from ansys.aedt.toolkits.motor.backend.motor_workflow.aedtflow import AedtFlow
from ansys.aedt.toolkits.motor.backend.motor_workflow.motorcadflow import MotorCADFlow


class Toolkit(MotorCADFlow, AedtFlow):
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
        MotorCADFlow.__init__(self)
        AedtFlow.__init__(self)
