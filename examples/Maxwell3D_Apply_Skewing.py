from pyaedt import Maxwell3d
from pyaedt.modeler.geometry_operators import GeometryOperators as go

# Specify project path and design name
active_design = "Motor-CAD e9_eMobility_IPM"
m3d = Maxwell3d(specified_version="2023.1", projectname="", designname=active_design)

m3d["RotorSlices"] = 3
m3d["MagnetsSegmentsPerSlice"] = 2
m3d["SkewAngle"] = "1.67deg"

magnet_material = "N42UH"