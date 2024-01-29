# from pydantic.dataclasses import dataclass
# from dataclasses import dataclass
# from dataclasses import field
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import Field


class CommonProperties(BaseModel):
    """Store common AEDT properties."""

    aedt_version: str = "2023.2"
    non_graphical: bool = False
    nb_core: int = Field(4, gt=0)
    active_project: str = ""
    active_design: Dict[str, str] = Field(default_factory=dict, min_length=0, max_length=1)
    projects: List[str] = Field(default_factory=list)
    designs_by_project_name: Dict[str, List[Dict[str, str]]] = Field(default_factory=dict)
    selected_process: int = 0
    use_grpc: bool = True
    is_toolkit_busy: bool = False
    url: str = "127.0.0.1"
    port: int = 5001
    debug: bool = True
    log_file: str = "motor_backend.log"
