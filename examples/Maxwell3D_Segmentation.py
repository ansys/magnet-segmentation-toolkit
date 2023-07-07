from pyaedt import Maxwell3d

m3d = Maxwell3d(specified_version="2023.1", aedt_process_id=24868)

m3d["RotorSlices"] = 3
m3d["MagnetsSegmentsPerSlice"] = 2
m3d["SkewAngle"] = "1.67deg"

magnet_material = "N42UH"
rotor_material = "POSCO 27PN1350_copy_130.7C"
shaft_material = "Mild Steel_HVH250_115_DWM_30C"

magnets = m3d.modeler.get_objects_by_material(magnet_material)
rotor = m3d.modeler.get_objects_by_material(rotor_material)[0]
vacuum_objects = m3d.modeler.get_objects_by_material("vacuum")
shaft = m3d.modeler.get_objects_by_material(shaft_material)[0]

if int(m3d.variable_manager["RotorSlices"].numeric_value) > 1:
    # rotor segmentation
    rotor_slices = m3d.modeler.objects_segmentation(rotor.id, segments_number=int(m3d["RotorSlices"]),
                                                    apply_mesh_sheets=False)
    # rotor and rotor pockets split
    rotor_objs = [rotor.name]
    rotor_pockets = [x.name for x in vacuum_objects]
    magnets_names = [x.name for x in magnets]
    for slice in rotor_slices[rotor.name]:
        cs = m3d.modeler.create_coordinate_system(slice.faces[0].center, name=slice.name + "_cs")
        rotor_objs = m3d.modeler.split(rotor_objs, "XY")
        rotor_pockets = m3d.modeler.split(rotor_pockets, "XY")
        magnets_names = m3d.modeler.split(magnets_names, "XY")

# set global cs
m3d.modeler.set_working_coordinate_system('Global')

faces = []
for rotor_obj in m3d.modeler.get_objects_by_material(rotor_material):
    objs_in_slice = [x for x in m3d.modeler.object_list if
                     round(x.bottom_face_z.center[2], 1) == rotor_obj.bottom_face_z.center[2] and x.name != shaft.name]
    for obj in objs_in_slice:
        m3d.modeler.set_working_coordinate_system('Global')
        if obj in magnets:
            magnet_segments = m3d.modeler.objects_segmentation(obj.id, segments_number=m3d.variable_manager[
                "MagnetsSegmentsPerSlice"].numeric_value, apply_mesh_sheets=False)
            faces = [x.bottom_face_z for x in magnet_segments[obj.name]]
            m3d.assign_insulating(faces, "{}_segments".format(obj.name))
            # create relative coordinate system for magnets
            # do we need as many cs as magnet segment or just for magnet object?
            for segment in magnet_segments[obj.name]:
                # fix
                cs = m3d.modeler.create_coordinate_system(segment.bottom_face_z.center, name=segment + "_cs")

m3d.release_desktop(False, False)
