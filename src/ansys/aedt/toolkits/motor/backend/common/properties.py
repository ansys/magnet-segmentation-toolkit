import json
import os

from ansys.aedt.toolkits.motor.backend.properties import AEDTProperties
from ansys.aedt.toolkits.motor.backend.properties import GeneralProperties
from ansys.aedt.toolkits.motor.backend.properties import Properties

with open(os.path.join(os.path.dirname(__file__), "general_properties.json")) as fh:
    general_properties = GeneralProperties(json.load(fh))
with open(os.path.join(os.path.dirname(__file__), "..", "aedt_properties.json")) as fh:
    aedt_properties = AEDTProperties(json.load(fh))

properties = Properties(general_properties=general_properties, aedt_properties=aedt_properties)
