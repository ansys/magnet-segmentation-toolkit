from ansys.aedt.toolkits.motor.backend.motor_workflow.aedtflow import AedtFlow
from ansys.aedt.toolkits.motor.backend.motor_workflow.motorcadflow import MotorCADFlow


class Toolkit(MotorCADFlow, AedtFlow):
    """API to control the toolkit workflow.

    This class provides methods to connect to a selected AEDT session or a new one and automates the segmentation and
    skew of a 3D motor model.

    Examples
    --------
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> import time
    >>> toolkit = Toolkit()
    >>> toolkit.launch_aedt()
    """

    def __init__(self):
        MotorCADFlow.__init__(self)
        AedtFlow.__init__(self)
