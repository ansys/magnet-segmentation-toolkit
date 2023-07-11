import itertools

from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.constants import unit_converter

from ansys.aedt.toolkits.motor.backend.common.api_generic import ToolkitGeneric
from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.common.properties import properties


class AedtFlow(ToolkitGeneric):
    """API to control AEDT toolkit workflow.

    This class provides methods to connect to a selected design...

    Examples
    --------
        >>> from ansys.aedt.toolkits.motor.backend.api import Toolkit
        >>> import time
        >>> toolkit = Toolkit()
        >>> msg1 = toolkit.launch_aedt()
        >>> response = toolkit.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
        >>> new_property = {"vbs_path": "path\to\toolkit.vbs"}
        >>> toolkit.set_properties(new_property)
        >>> msg3 = toolkit.run_vbs()
        >>> response = toolkit.get_thread_status()
        >>> while response[0] == 0:
        >>>     time.sleep(1)
        >>>     response = toolkit.get_thread_status()
    """

    def __init__(self):
        ToolkitGeneric.__init__(self)
        self.maxwell = None

    def init_aedt(self):
        """Initialize Maxwell.

        If the .vbs script is provided it automatically runs it.
        If a Maxwell3D instance is provided it attaches to it.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if properties.vbs_file_path and properties.active_project:
            logger.error("User can decide whether to run a .vbs script or open a Maxwell3D project at a time.")
            return False

        self.connect_aedt()

        if properties.active_project:
            self.open_project(properties.active_project)
        elif properties.vbs_file_path:
            self.desktop.odesktop.RunScript(properties.vbs_file_path)
            self._save_project_info()
            self.desktop.release_desktop(False, False)
            self.desktop = None

        if properties.design_list:
            self.connect_design(app_name="Maxwell3d")
            self.maxwell = self.aedtapp
        else:
            logger.error("No design in specified project.")
            return False
        return True

    def set_model(self, mcad_magnets_material):
        """Set geometry model.

        Set axial length, boundary conditions and remove from model unclassified objects.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False
        if not mcad_magnets_material:
            logger.error("Magnets material not provided.")
            return False

        self.maxwell["HalfAxial"] = properties.HalfAxial
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False
        if properties.HalfAxial == 1:
            return self._apply_boundary_conditions(mcad_magnets_material)
        return True

    def mesh_settings(self, mcad_magnets_material):
        """Apply mesh settings.

        Apply mesh to magnets.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False
        if not mcad_magnets_material:
            logger.error("Magnets material not provided.")
            return False

        try:
            magnets = self._get_magnets(mcad_magnets_material)
            if not self.maxwell.mesh.assign_length_mesh(
                magnets,
                maxlength=2,
                meshop_name="magnets_mesh",
            ):
                return False
            return True
        except:
            return False

    def analyze_model(self):
        """Analyze model.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False

        try:
            self.maxwell.analyze_setup(properties.SetupToAnalyze)
            return True
        except:
            return False

    def get_losses_from_reports(self):
        """Create report magnet losses.

        Returns
        -------
        dict
            Average values + units for reports specified in json file.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False

        try:
            report_dict = {}
            self.maxwell.post.create_report(expressions="SolidLoss", plotname="Losses", primary_sweep_variable="Time")
            data = self.maxwell.post.get_solution_data(expressions="SolidLoss", primary_sweep_variable="Time")
            avg = sum(data.data_magnitude()) / len(data.data_magnitude())
            avg = unit_converter(avg, "Power", data.units_data["SolidLoss"], "W")
            report_dict["SolidLoss"] = {"Value": round(avg, 4), "Unit": "W"}
            return True, report_dict
        except:
            return False

    def magnets_segmentation(self, apply_mesh_sheets=False):
        """Apply magnets segmentation.

        Parameters
        ----------
        apply_mesh_sheets : bool
            Whether to apply mesh sheets inside magnet.
            Default value is ``False``.

        Returns
        -------
        list
            list of segments the magnets have been split into.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False

        try:
            for bound in self.maxwell.boundaries[:]:
                if (
                    bound.type == "Insulating"
                    and bound.name in self.maxwell.odesign.GetChildObject("Boundaries").GetChildNames()
                ):
                    bound.delete()
            for magnet in properties.Magnets:
                segments = self.maxwell.modeler.objects_segmentation(
                    magnet["Name"],
                    segments_number=magnet["NumberOfSegments"],
                    apply_mesh_sheets=apply_mesh_sheets,
                )
            return segments
        except:
            return False

    def apply_mesh_magnets_sheets(self, segments):
        """Apply mesh to magnets sheets.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        try:
            for magnet in properties.Magnets:
                mesh_sheet_ids = [sheet.id for sheet in segments[1][magnet["Name"]]]
                self.maxwell.mesh.assign_length_mesh(
                    mesh_sheet_ids,
                    maxlength=magnet["MeshLength"],
                    meshop_name=magnet["MeshName"],
                )
            return True
        except:
            return False

    def _apply_boundary_conditions(self, mcad_magnets_material):
        try:
            for bound in self.maxwell.boundaries[:]:
                if (
                    bound.type == "Insulating"
                    and bound.name in self.maxwell.odesign.GetChildObject("Boundaries").GetChildNames()
                ):
                    bound.delete()
            magnets = self._get_magnets(mcad_magnets_material)
            self.maxwell.assign_insulating(magnets, "magnets_insulation")
            face_ids = []
            for obj in self.maxwell.modeler.solid_objects:
                if obj.bounding_box[2] == 0.0:
                    face_ids.append(self.maxwell.modeler[obj].bottom_face_z.id)
            self.maxwell.assign_symmetry(face_ids, symmetry_name="model_symmetry")
            return True
        except:
            return False

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
                decompose_variable_value(temp.split("_")[1])[0] for temp in database_materials if "_" in temp
            ]
            check = 0
            for i in range(0, len(database_mat_names)):
                if material_to_check[0].lower() in database_mat_names[i].lower():
                    check = 1
                    if float(material_to_check[1]) - database_mat_temps[i] < 0.1:
                        return database_materials[i]
                    else:
                        self.maxwell.logger.error(
                            "Wrong temperature provided for material: {}."
                            "Same material in database with correct "
                            "temperature will be used.".format(material_to_check[0])
                        )
                        return database_materials[i]
            if check == 0:
                raise ValueError("Provided material {} doesn't exist in current design.".format(material_to_check[0]))
            return True
        except:
            return False

    def _get_magnets(self, mcad_magnets_material):
        """Get all magnets objects."""
        try:
            magnets_material = self._materials_check(mcad_magnets_material)
            magnets = [
                magnet for magnet in self.maxwell.modeler.get_objects_by_material(magnets_material) if magnet.model
            ]
            return magnets
        except:
            return False
