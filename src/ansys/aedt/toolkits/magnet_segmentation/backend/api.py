from ansys.aedt.toolkits.magnet_segmentation.backend.motor_workflow.aedtflow import AedtFlow
from ansys.aedt.toolkits.magnet_segmentation.backend.motor_workflow.motorcadflow import MotorCADFlow


class Toolkit(MotorCADFlow, AedtFlow):
    """Provides methods for controlling the toolkit workflow.

    This class provides methods for creating a new or connecting to an existing AEDT
    session and automating the segmentation and skew of a 3D motor model.

    Examples
    --------
    >>> from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit
    >>> import time
    >>> toolkit = Toolkit()
    >>> toolkit.launch_aedt()
    """

    def __init__(self):
        MotorCADFlow.__init__(self)
        AedtFlow.__init__(self)
