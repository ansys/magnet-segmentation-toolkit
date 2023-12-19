from dataclasses import dataclass
from dataclasses import field
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
