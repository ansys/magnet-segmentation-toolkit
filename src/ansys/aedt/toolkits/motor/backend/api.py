from ansys.aedt.toolkits.motor.backend.motor_workflow.aedtflow import AedtFlow


class Toolkit(AedtFlow):
    """Provides methods for controlling the toolkit workflow.

    This class provides methods for creating a new or connecting to an existing AEDT
    session and automating the segmentation and skew of a 3D motor model.

    Examples
    --------
    >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
    >>> import time
    >>> toolkit = Toolkit()
    >>> toolkit.launch_aedt()
    """

    def __init__(self):
        super().__init__(self)
