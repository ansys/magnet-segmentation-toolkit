import itertools
import os

from pyaedt import Maxwell3d
from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.constants import unit_converter

from ansys.aedt.toolkits.motor.common_settings import CommonSettings


class AedtExport:
    """Provides an AEDT instance.

     Create a Maxwell3D instance and the motor 3D model by running .vbs script.

    Parameters
    ----------
    vbs_file_path : str
        File path of the vbs script.

    Examples
    --------
    >>> aedt = AedtExport()
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

    def __init__(self, settings_path, vbs_file_path=None, m3d=None):
        """Init."""
        self.working_dir = os.path.dirname(settings_path)
        self.vbs_file_path = vbs_file_path
        self.maxwell = m3d
        self.aedt_dict = CommonSettings(self.working_dir).load_json(
            os.path.join(settings_path, "aedt_parameters.json")
        )
        self.conf_dict = CommonSettings(self.working_dir).load_json(
            os.path.join(settings_path, "configuration_settings.json")
        )

    def set_aedt_dict_props(self, key, value):
        """Set AEDT props."""
        try:
            self.aedt_dict[key] = value
        except:
            raise ValueError("Provided key doesn't exist.")

    def init_maxwell(self):
        """Initialize Maxwell and run .vbs script.

        Needed if an instance of Maxwell3d is not given in input of AedtExport class.
        """
        if not self.maxwell:
            self.maxwell = Maxwell3d(
                specified_version=self.conf_dict["AEDTVersion"],
                non_graphical=self.conf_dict["NonGraphical"],
            )
        if self.vbs_file_path:
            self.maxwell.odesktop.RunScript(self.vbs_file_path)

    def set_model(self):
        """Set geometry model.

        Set axial length, boundary conditions and remove from model unclassified objects.
        """
        self.maxwell["HalfAxial"] = self.aedt_dict["HalfAxial"]
        self.maxwell["NumTorqueCycles"] = self.aedt_dict["ModelParameters"]["NumberTorqueCycles"]
        self.maxwell["NumTorquePointsPerCycle"] = self.aedt_dict["ModelParameters"][
            "NumberPointsTorqueCycles"
        ]
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False
        if self.aedt_dict["HalfAxial"] == 1:
            self._apply_boundary_conditions()

    def mesh_settings(self):
        """Apply mesh settings.

        Apply mesh to rotor, stator, windings and magnets.
        """
        # windings
        windings_material = self._materials_check(self.aedt_dict["Materials"]["Windings"])
        copper_objs_list = self.maxwell.modeler.get_objects_by_material(windings_material)
        self.maxwell.mesh.assign_length_mesh(
            copper_objs_list,
            maxlength=self.aedt_dict["Mesh"]["Windings"]["Length"],
            meshop_name=self.aedt_dict["Mesh"]["Windings"]["Name"],
        )
        # rotor - stator
        rotor_material = self._materials_check(self.aedt_dict["Materials"]["Rotor"])
        stator_material = self._materials_check(self.aedt_dict["Materials"]["Stator"])
        if rotor_material == stator_material:
            rotor_stator = self.maxwell.modeler.get_objects_by_material(rotor_material)
        else:
            rotor = self.maxwell.modeler.get_objects_by_material(rotor_material)
            stator = self.maxwell.modeler.get_objects_by_material(stator_material)
            rotor_stator = [rotor, stator]
        self.maxwell.mesh.assign_length_mesh(
            rotor_stator,
            maxlength=self.aedt_dict["Mesh"]["RotorAndStator"]["Length"],
            meshop_name=self.aedt_dict["Mesh"]["RotorAndStator"]["Name"],
        )
        # magnets
        magnets_material = self._materials_check(self.aedt_dict["Materials"]["Magnets"])
        magnets = [
            magnet
            for magnet in self.maxwell.modeler.get_objects_by_material(magnets_material)
            if magnet.model
        ]
        self.maxwell.mesh.assign_length_mesh(
            magnets,
            maxlength=self.aedt_dict["Mesh"]["Magnets"]["Length"],
            meshop_name=self.aedt_dict["Mesh"]["Magnets"]["Name"],
        )

    def analyze_model(self):
        """Analyze model."""
        self.maxwell.analyze_setup(self.aedt_dict["SetupToAnalyze"])

    def get_values_from_reports(self):
        """Create report magnet losses.

        Returns
        -------
        dict
            Average values + units for each report in the project.
        """
        # TO FIX BECAUSE IT WORKS ONLY WITH POWER
        report_dict = {}
        for x in self.aedt_dict["Reports"]:
            self.maxwell.post.create_report(
                expressions=x["Expression"], plotname=x["PlotName"], primary_sweep_variable="Time"
            )
            data = self.maxwell.post.get_solution_data(
                expressions=x["Expression"], primary_sweep_variable="Time"
            )
            avg = sum(data.data_magnitude()) / len(data.data_magnitude())
            avg = unit_converter(avg, "Power", data.units_data[x["Expression"]], "W")
            report_dict[x["Expression"]] = {"Value": round(avg, 4), "Unit": "W"}
        return report_dict

    def save_and_close(self):
        """Save and close."""
        self.maxwell.close_project()
        self.maxwell.release_desktop()

    def _apply_boundary_conditions(self):
        for bound in self.maxwell.boundaries[:]:
            if (
                bound.type == "Insulating"
                and bound.name in self.maxwell.odesign.GetChildObject("Boundaries").GetChildNames()
            ):
                bound.delete()
        magnets_material = self._materials_check(self.aedt_dict["Materials"]["Magnets"])
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
        self.maxwell.assign_symmetry(face_ids, symmetry_name="model_symmetry")

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
