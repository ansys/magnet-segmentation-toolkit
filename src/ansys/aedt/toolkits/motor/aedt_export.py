import itertools
import os

from pyaedt import Desktop, Maxwell3d
from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.DataHandlers import json_to_dict


class AEDTExport:
    """Provides an AEDT instance.

     Create a Maxwell3D instance and the motor 3D model by running .vbs script.

    Parameters
    ----------
    vbs_file_path : str
        File path of the vbs script.

    Examples
    --------
    >>> aedt = AEDTExport()
    Set the geometry model such as the axial length,
    apply boundary conditions and
    remove from model unclassified objects
    >>> aedt.set_model()
    Set mesh for rotor, stator, windings and magnets
    >>> aedt.mesh_settings()
    Analyze model
    >>> aedt.analyze_model()
    Save and close project
    >>> aedt.save_and_close()
    """

    def __init__(self, vbs_file_path):
        """Init."""
        self._vbs_file_path = vbs_file_path
        self.__configuration_dict = json_to_dict(
            os.path.join(
                os.path.dirname(__file__), "configuration_settings", "configuration_settings.json"
            )
        )
        self._aedt_dict = json_to_dict(
            os.path.join(
                os.path.dirname(__file__), "configuration_settings", "aedt_parameters.json"
            )
        )
        self._desktop = Desktop(specified_version=self.__configuration_dict["AEDTVersion"])
        self._desktop.odesktop.RunScript(self._vbs_file_path)
        self.maxwell = Maxwell3d()
        self.working_dir = self.__configuration_dict["WorkingDirectory"]

    def set_model(self):
        """Set geometry model.

        Set axial length, boundary conditions and remove from model unclassified objects.
        """
        self.maxwell["HalfAxial"] = self._aedt_dict["HalfAxial"]
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False
        if self._aedt_dict["HalfAxial"] == 1:
            self._apply_boundary_conditions()

    def mesh_settings(self):
        """Apply mesh settings.

        Apply mesh to rotor, stator, windings and magnets.
        """
        # windings
        windings_material = self._materials_check(self._aedt_dict["Materials"]["Windings"])
        copper_objs_list = self.maxwell.modeler.get_objects_by_material(windings_material)
        self.maxwell.mesh.assign_length_mesh(
            copper_objs_list,
            maxlength=self._aedt_dict["Mesh"]["Windings"],
            meshop_name=self._aedt_dict["Mesh"]["WindingsMeshName"],
        )
        # rotor - stator
        rotor_material = self._materials_check(self._aedt_dict["Materials"]["Rotor"])
        stator_material = self._materials_check(self._aedt_dict["Materials"]["Stator"])
        if rotor_material == stator_material:
            rotor_stator = self.maxwell.modeler.get_objects_by_material(rotor_material)
        else:
            rotor = self.maxwell.modeler.get_objects_by_material(rotor_material)
            stator = self.maxwell.modeler.get_objects_by_material(stator_material)
            rotor_stator = [rotor, stator]
        self.maxwell.mesh.assign_length_mesh(
            rotor_stator,
            maxlength=self._aedt_dict["Mesh"]["RotorAndStator"],
            meshop_name=self._aedt_dict["Mesh"]["RotorAndStatorMeshName"],
        )
        # magnets
        magnets_material = self._materials_check(self._aedt_dict["Materials"]["Magnets"])
        magnets = [
            magnet
            for magnet in self.maxwell.modeler.get_objects_by_material(magnets_material)
            if magnet.model
        ]
        self.maxwell.mesh.assign_length_mesh(
            magnets,
            maxlength=self._aedt_dict["Mesh"]["Magnets"],
            meshop_name=self._aedt_dict["Mesh"]["MagnetsMeshName"],
        )

    def analyze_model(self):
        """Analyze model."""
        self.maxwell.analyze_setup(self._aedt_dict["SetupToAnalyze"])

    def create_report_magnet_losses(self):
        """Create report magnet losses."""
        self.maxwell.post.create_report(
            expressions="SolidLoss", plotname="Losses", primary_sweep_variable="Time"
        )

    def save_and_close(self):
        """Save and close."""
        self.maxwell.save_project(
            os.path.join(self.working_dir, "{}.aedt".format(self.maxwell.project_name))
        )
        self._desktop.release_desktop(False, False)

    def _apply_boundary_conditions(self):
        magnets_material = self._materials_check(self._aedt_dict["Materials"]["Magnets"])
        magnets = [
            magnet
            for magnet in self.maxwell.modeler.get_objects_by_material(magnets_material)
            if magnet.model
        ]
        self.maxwell.assign_insulating(magnets, "magnets_insulation")
        face_ids = []
        for obj in self.maxwell.modeler.solid_objects:
            if obj.bounding_box[2] == 0.0:
                face_ids.append(self.maxwell.modeler[obj].bottom_face_z.id)
        self.maxwell.assign_symmetry(face_ids)

    def _materials_check(self, material_to_check):
        try:
            database_materials = list(
                itertools.chain(
                    self.maxwell.materials.conductors,
                    self.maxwell.materials.dielectrics,
                    self.maxwell.materials.gases,
                    self.maxwell.materials.liquids,
                )
            )
            database_mat_names = [mat.split("_")[0] for mat in database_materials]
            database_mat_temps = [
                decompose_variable_value(temp.split("_")[1])[0]
                for temp in database_materials
                if "_" in temp
            ]
            check = 0
            for i in range(0, len(database_mat_names)):
                if material_to_check["Name"].lower() in database_mat_names[i].lower():
                    check = 1
                    if float(material_to_check["Temp"]) - database_mat_temps[i] < 0.1:
                        return database_materials[i]
                    else:
                        self.maxwell.logger.error(
                            "Wrong temperature provided for material: {}."
                            "Same material in database with correct "
                            "temperature will be used.".format(material_to_check["Name"])
                        )
                        return database_materials[i]
            if check == 0:
                raise ValueError(
                    "Provided material {} doesn't exist in current design.".format(
                        material_to_check["Name"]
                    )
                )
        except ValueError as e:
            self.maxwell.logger.error(e)
            return False
