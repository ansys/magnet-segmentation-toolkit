from pyaedt import Maxwell3d

# Specify project path and design name
active_design = "Motor-CAD e9_eMobility_IPM"
m3d = Maxwell3d(specified_version="2023.1", projectname="", designname=active_design)

m3d["RotorSlices"] = 3
m3d["MagnetsSegmentsPerSlice"] = 3
m3d["SkewAngle"] = "1.67deg"

m3d.duplicate_design(active_design)

magnet_material = "N42UH"
rotor_material = "POSCO 27PN1350_copy_130.7C"
shaft_material = "Mild Steel_HVH250_115_DWM_30C"

magnets = m3d.modeler.get_objects_by_material(magnet_material)
rotor = m3d.modeler.get_objects_by_material(rotor_material)[0]
vacuum_objects = m3d.modeler.get_objects_by_material("vacuum")
rotor_pockets = []
for obj in vacuum_objects:
    obj_in_bb = m3d.modeler.objects_in_bounding_box(obj.bounding_box, check_lines=False, check_sheets=False)
    if isinstance(obj_in_bb,list) and len(obj_in_bb) == 2:
        rotor_pockets.append(obj)
shaft = m3d.modeler.get_objects_by_material(shaft_material)[0]

if int(m3d.variable_manager["RotorSlices"].numeric_value) > 1:
    # rotor segmentation
    rotor_slices = m3d.modeler.objects_segmentation(rotor.id, segments_number=int(m3d["RotorSlices"]),
                                                    apply_mesh_sheets=False)
    # rotor and rotor pockets split
    rotor_objs = [rotor.name]
    rotor_pockets_names = [x.name for x in rotor_pockets]
    magnets_names = [x.name for x in magnets]
    for slice in rotor_slices[rotor.name]:
        cs = m3d.modeler.create_coordinate_system(slice.faces[0].center, name=slice.name + "_cs")
        rotor_objs = m3d.modeler.split(rotor_objs, "XY")
        rotor_pockets = m3d.modeler.split(rotor_pockets, "XY")
        magnets_names = m3d.modeler.split(magnets_names, "XY")

magnets = m3d.modeler.get_objects_by_material(magnet_material)
for magnet in magnets:
    magnet_segments = m3d.modeler.objects_segmentation(magnet.id, segments_number=m3d.variable_manager[
        "MagnetsSegmentsPerSlice"].numeric_value, apply_mesh_sheets=False)
    faces = [x.bottom_face_z for x in magnet_segments[magnet.name]]
    m3d.assign_insulating(faces, "{}_segments".format(magnet.name))

m3d.release_desktop(False, False)
