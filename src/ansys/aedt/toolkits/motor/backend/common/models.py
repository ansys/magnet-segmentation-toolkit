# # from pydantic.dataclasses import dataclass
# # from dataclasses import dataclass
# # from dataclasses import field
# from typing import Dict
# from typing import List

# from pydantic import BaseModel
# from pydantic import Field


# class CommonProperties(BaseModel):
#     """Store common AEDT properties."""

#     aedt_version: str = "2023.2"
#     non_graphical: bool = False
#     nb_core: int = Field(4, gt=0)
#     active_project: str = ""
#     active_design: Dict[str, str] = Field(default_factory=dict, min_length=0, max_length=1)
#     projects: List[str] = Field(default_factory=list)
#     designs_by_project_name: Dict[str, List[Dict[str, str]]] = Field(default_factory=dict)
#     selected_process: int = 0
#     use_grpc: bool = True
#     is_toolkit_busy: bool = False
#     url: str = "127.0.0.1"
#     port: int = 5001
#     debug: bool = True
#     log_file: str = "motor_backend.log"


from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate


class CommonProperties(Schema):
    """Store common AEDT properties."""

    aedt_version = fields.Str(missing="2023.2")
    non_graphical = fields.Bool(missing=False)
    nb_core = fields.Int(validate=validate.Range(min=0), missing=4)
    active_project = fields.Str(missing="")
    active_design = fields.Dict(keys=fields.Str, values=fields.Str, missing=dict)
    projects = fields.List(fields.Str(), missing=list)
    # NOTE: designs_by_project_name should be Dict[str, List[Dict[str, str]]]
    designs_by_project_name = fields.Dict(keys=fields.Str, missing=dict)
    selected_process = fields.Int(validate=validate.Range(min=0), missing=0)
    use_grpc = fields.Bool(missing=True)
    is_toolkit_busy = fields.Bool(missing=False)
    url = fields.Str(missing="127.0.0.1")
    port = fields.Int(validate=validate.Range(min=0), missing=5001)
    debug = fields.Bool(missing=True)
    log_file = fields.Str(missing="motor_backend.log")
