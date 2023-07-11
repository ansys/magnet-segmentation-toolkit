from pyaedt import Maxwell3d
from pyaedt.modeler.geometry_operators import GeometryOperators as go

# Specify project path and design name
active_design = "Motor-CAD e9_eMobility_IPM"
m3d = Maxwell3d(specified_version="2023.1", projectname="", designname=active_design)

magnet_material = "N30UH_65C"

magnets = [x for x in m3d.modeler.get_objects_by_material(magnet_material) if x.object_type == "Solid"]
magnets_cs_dict = {}
for magnet in magnets:
    m3d.modeler.set_working_coordinate_system('Global')
    # create relative cs for each magnet and assign XY plane direction calculating x and y vectors
    new_list = sorted([x for x in magnet.top_face_z.edges], key=lambda x: x.length, reverse=True)
    x_pointing = go.distance_vector(magnet.top_face_z.center, new_list[0].vertices[0].position,
                                    new_list[0].vertices[1].position)
    y_pointing = go.distance_vector(magnet.top_face_z.center, new_list[2].vertices[0].position,
                                    new_list[2].vertices[1].position)
    cs = m3d.modeler.create_coordinate_system(magnet.top_face_z.center,
                                              name=magnet.name + "_cs",
                                              x_pointing=x_pointing,
                                              y_pointing=y_pointing)
    magnets_cs_dict[magnet.name] = cs

m3d.release_desktop(False, False)