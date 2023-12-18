# try:
#     from properties_data import PropertiesData
# except ModuleNotFoundError:
#     from .properties_data import PropertiesData

# import json
# import os

# with open(os.path.join(os.path.dirname(__file__), "general_properties.json")) as fh:
#     _general_properties = json.load(fh)

# with open(os.path.join(os.path.dirname(__file__), "..", "motorcad_properties.json")) as fh:
#     _motorcad_properties = json.load(fh)

# with open(os.path.join(os.path.dirname(__file__), "..", "aedt_properties.json")) as fh:
#     _aedt_properties = json.load(fh)

# _default_properties = {**_general_properties, **_motorcad_properties, **_aedt_properties}
# properties = PropertiesData(_default_properties)


# def check_property_file_against_defaults(prop_filename):
#     """
#     Check if property exists in the defaults.

#     Parameters
#     ----------
#     prop_filename : str
#         Qualified path of the property file to check.

#     Returns
#     -------
#     bool
#         ``True`` if the file check passes, `False` otherwise.
#     """
#     tmp_properties = PropertiesData(_default_properties)
#     try:
#         tmp_properties.read_from_file(prop_filename)
#         return True
#     except Exception as e:
#         print(e)
#         return False

from dataclasses import dataclass
from dataclasses import field

# import json
# import os
from typing import Dict
from typing import List


@dataclass()
class CommonProperties:
    """Store common AEDT properties."""

    aedt_version: str = "2023.2"
    non_graphical: bool = False
    nb_core: int = 4
    active_project: str = ""
    active_design: Dict[str, str] = field(default_factory=dict)
    projects: List[str] = field(default_factory=list)
    designs_by_project_name: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
    selected_process: int = 0
    use_grpc: bool = True
    is_toolkit_busy: bool = False
    url: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    log_file: str = "backend.log"
