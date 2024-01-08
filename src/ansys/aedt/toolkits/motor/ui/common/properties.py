# """Data classes used to store data related to UI settings.

import json
import os

from ansys.aedt.toolkits.motor.backend.models import Properties


class UIProperties(validate_assignment=True):
    """Store properties useful for UI."""

    backend_url: str = "127.0.0.1"
    backend_port: int = 5001
    debug: bool = True
    log_file: str = "motor_frontend.log"


general_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "general_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "general_properties.json")) as file_handler:
        general_kwargs = json.load(file_handler)

general_settings = UIProperties(**general_kwargs)

be_properties = Properties()
