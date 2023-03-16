import os


from pyaedt import Desktop
from pyaedt import Maxwell3d


class AEDTexport:
    def __init__(self, vbs_file_path, working_dir):
        self._vbs_file_path = vbs_file_path
        self._desktop = Desktop(specified_version="2023.1")
        self._desktop.odesktop.RunScript(self._vbs_file_path)
        self.maxwell = Maxwell3d()
        self.working_dir = working_dir

    def set_model(self):
        self.maxwell["HalfAxial"] = 1
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False

    def mesh_settings(self):
        # apply mesh sizing
        # windings
        copper_objs_list = self.maxwell.modeler.get_objects_by_material("Copper (Pure)_50C")
        self.maxwell.mesh.assign_length_mesh(copper_objs_list, maxlength=8, meshop_name="copper_objs_mesh")
        # rotor - stator
        rotor_stator = self.maxwell.modeler.get_objects_by_material("M250-35A_20C")
        self.maxwell.mesh.assign_length_mesh(rotor_stator, maxlength=8, meshop_name="rotor_stator_mesh")
        # magnets
        magnets = self.maxwell.modeler.get_objects_by_material("N30UH_20C")
        self.maxwell.mesh.assign_length_mesh(magnets, maxlength=2, meshop_name="magnets_mesh")

    def apply_boundary_conditions(self):
        # apply insulating BC on all magnet faces
        magnets = self.maxwell.modeler.get_objects_by_material("N30UH_20C")
        self.maxwell.assign_insulating(magnets, "magnets_insulation")
        # apply symmetry (flux tangential) on symmetry plane
        face_ids = []
        for obj in self.maxwell.modeler.solid_objects:
            if obj.bounding_box[2] == 0.0:
                face_ids.append(self.maxwell.modeler[obj].bottom_face_z.id)
        self.maxwell.assign_insulating(face_ids)
        # Set Eddy Effects on Magnets (already done by export)

    def analyze_model(self):
        self.maxwell.analyze_setup(self.maxwell.setups[0])

    def save_and_close(self):
        self.maxwell.save_project(os.path.join(self.working_dir, "{}.aedt".format(self.maxwell.project_name)))
        self._desktop.release_desktop(False, False)
