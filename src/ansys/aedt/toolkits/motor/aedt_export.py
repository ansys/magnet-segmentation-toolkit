import os

from pyaedt import Desktop, Maxwell3d


class AEDTexport:
    """Provides an AEDT instance.

     Create a Maxwell3D instance and the motor 3D model by running .vbs script.

    Parameters
    ----------
    vbs_file_path : str
        File path of the vbs script.
    working_dir : str
        Working directory where to save th project to.

    Examples
    --------
    >>>> aedt = AEDTexport()
    Set the geometry model such as the axial length,
    apply boundary conditions and
    remove from model unclassified objects
    >>>> aedt.set_model()
    Set mesh for rotor, stator, windings and magnets
    >>>> aedt.mesh_settings()
    Analyze model
    >>>> aedt.analyze_model()
    Save and close project
    >>>> aedt.save_and_close()
    """

    def __init__(self, vbs_file_path, working_dir):
        """Init."""
        self._vbs_file_path = vbs_file_path
        self._desktop = Desktop(specified_version="2023.1")
        self._desktop.odesktop.RunScript(self._vbs_file_path)
        self.maxwell = Maxwell3d()
        self.working_dir = working_dir

    def set_model(self):
        """Set geometry model.

        Set axial length, boundary conditions and remove from model unclassified objects.
        """
        self.maxwell["HalfAxial"] = 1
        if self.maxwell["HalfAxial"] == 1:
            self._apply_boundary_conditions()
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False

    def mesh_settings(self):
        """Apply mesh settings.

        Apply mesh to rotor, stator, windings and magnets.
        """
        # windings
        copper_objs_list = self.maxwell.modeler.get_objects_by_material("Copper (Pure)_50C")
        self.maxwell.mesh.assign_length_mesh(
            copper_objs_list, maxlength=8, meshop_name="copper_objs_mesh"
        )
        # rotor - stator
        rotor_stator = self.maxwell.modeler.get_objects_by_material("M250-35A_20C")
        self.maxwell.mesh.assign_length_mesh(
            rotor_stator, maxlength=8, meshop_name="rotor_stator_mesh"
        )
        # magnets
        magnets = self.maxwell.modeler.get_objects_by_material("N30UH_20C")
        self.maxwell.mesh.assign_length_mesh(magnets, maxlength=2, meshop_name="magnets_mesh")

    def analyze_model(self):
        """Analyze model."""
        self.maxwell.analyze_setup(self.maxwell.setups[0])

    def save_and_close(self):
        """Save and close."""
        self.maxwell.save_project(
            os.path.join(self.working_dir, "{}.aedt".format(self.maxwell.project_name))
        )
        self._desktop.release_desktop(False, False)

    def _apply_boundary_conditions(self):
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
