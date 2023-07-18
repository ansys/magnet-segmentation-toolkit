from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.constants import unit_converter
from pyaedt.modeler.geometry_operators import GeometryOperators as go

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

    def set_model(self):
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

        self.maxwell["RotorSlices"] = properties.RotorSlices
        self.maxwell["MagnetsSegmentsPerSlice"] = properties.MagnetsSegmentsPerSlice
        self.maxwell["SkewAngle"] = properties.SkewAngle
        for obj in self.maxwell.modeler.unclassified_objects:
            obj.model = False
        return True

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

    def segmentation(self):
        """Apply objects segmentation.
        It automatically segments rotor, rotor pockets and magnets.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        if not self.maxwell:
            logger.error("AEDT not initialized")
            return False
        if properties.IsSkewed is None:
            logger.error("``IsSkewed`` property has to be set to perform segmentation.")
            return False

        self.maxwell.duplicate_design(properties.active_design["Maxwell3d"])

        try:
            for bound in self.maxwell.boundaries[:]:
                if (
                    bound.type == "Insulating"
                    and bound.name in self.maxwell.odesign.GetChildObject("Boundaries").GetChildNames()
                ):
                    bound.delete()

            self.maxwell["MagnetsSegmentsPerSlice"] = properties.MagnetsSegmentsPerSlice

            if not properties.IsSkewed:
                self.maxwell["RotorSlices"] = properties.RotorSlices

                magnets = self.maxwell.modeler.get_objects_by_material(properties.MagnetsMaterial)
                if len(self.maxwell.modeler.get_objects_by_material(properties.RotorMaterial)) > 1:
                    for obj in self.maxwell.modeler.get_objects_by_material(properties.RotorMaterial):
                        if len(
                            [i for i in magnets if i in self.maxwell.modeler.objects_in_bounding_box(obj.bounding_box)]
                        ) == len(magnets):
                            rotor = obj
                else:
                    rotor = self.maxwell.modeler.get_objects_by_material(properties.RotorMaterial)[0]

                vacuum_objects = [
                    x for x in self.maxwell.modeler.get_objects_by_material("vacuum") if x.object_type == "Solid"
                ]
                rotor_pockets = self._get_rotor_pockets(vacuum_objects)

                if int(properties.RotorSlices) > 1:
                    # rotor segmentation
                    rotor_slices = self.maxwell.modeler.objects_segmentation(
                        rotor.id, segments_number=int(self.maxwell["RotorSlices"]), apply_mesh_sheets=False
                    )
                    # rotor and rotor pockets split
                    rotor_objs = [rotor.name]
                    magnets_names = [x.name for x in magnets]
                    if len(rotor_pockets) > 0:
                        rotor_pockets_names = [x.name for x in rotor_pockets]
                    for slice in rotor_slices[rotor.name]:
                        cs = self.maxwell.modeler.create_coordinate_system(
                            slice.faces[0].center, name=slice.name + "_cs"
                        )
                        rotor_objs = self.maxwell.modeler.split(rotor_objs, "XY")
                        magnets_names = self.maxwell.modeler.split(magnets_names, "XY")
                        if len(rotor_pockets) > 0:
                            rotor_pockets_names = self.maxwell.modeler.split(rotor_pockets_names, "XY")

            magnets = self.maxwell.modeler.get_objects_by_material(properties.MagnetsMaterial)
            for magnet in magnets:
                cs = self.maxwell.modeler.duplicate_coordinate_system_to_global(magnet.part_coordinate_system)
                cs.origin = magnet.top_face_z.center
                magnet.part_coordinate_system = cs.name
                self.maxwell.modeler.set_working_coordinate_system("Global")
                magnet_segments = self.maxwell.modeler.objects_segmentation(
                    magnet.id,
                    segments_number=self.maxwell.variable_manager["MagnetsSegmentsPerSlice"].numeric_value,
                    apply_mesh_sheets=False,
                )
                faces = []
                for face in magnet_segments[magnet.name]:
                    obj = self.maxwell.modeler.create_object_from_face(face.top_face_z)
                    obj.part_coordinate_system = cs.name
                    faces.append(obj.top_face_z)
                [face.delete() for face in magnet_segments[magnet.name]]
                self.maxwell.assign_insulating(faces, "{}_segments".format(magnet.name))
                self._update_cs(cs)
            return True
        except:
            return False

    def _get_rotor_pockets(self, vacuum_objects):
        """Return the rotor pockets if any.

        Parameters
        ----------
        vacuum_objects : list
            List of vacuum objects.

        Returns
        -------
        list
            list of class:`pyaedt.modeler.cad.object3d.Object3d`
        """
        rotor_pockets = []
        for obj in vacuum_objects:
            obj_in_bb = self.maxwell.modeler.objects_in_bounding_box(
                obj.bounding_box, check_lines=False, check_sheets=False
            )
            obj_in_bb.remove(obj)
            if isinstance(obj_in_bb, list) and len(obj_in_bb) == 1:
                rotor_pockets.append(obj)
        return rotor_pockets

    def _update_cs(self, cs):
        """Update the cs to Euler ZYZ mode.

        Parameters
        ----------
        cs : :class:`pyaedt.modeler.Modeler.CoordinateSystem`
            Coordinate system.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        try:
            x_pointing = [
                decompose_variable_value(cs.props["XAxisXvec"])[0],
                decompose_variable_value(cs.props["XAxisYvec"])[0],
                decompose_variable_value(cs.props["XAxisZvec"])[0],
            ]
            y_pointing = [
                decompose_variable_value(cs.props["YAxisXvec"])[0],
                decompose_variable_value(cs.props["YAxisYvec"])[0],
                decompose_variable_value(cs.props["YAxisZvec"])[0],
            ]
            x, y, z = go.pointing_to_axis(x_pointing, y_pointing)
            phi, theta, psi = go.axis_to_euler_zyz(x, y, z)
            magnet_angle = go.rad2deg(phi)
            cs.change_cs_mode(2)
            cs.props["Phi"] = "{}deg".format(str(magnet_angle))
            cs.props["Psi"] = "90deg"
            cs.props["Theta"] = "0deg"
            cs.update()
            return True
        except:
            return False

    # def _apply_skew_to_cs(self, cs):
    #     """"""
    #     rad_skew_angle = go.deg2rad(properties.SkewAngle)
    #     cs.props["OriginX"] = "{}mm*cos({})-{}mm*sin({})".format(str(x), str(rad_skew_angle), str(y),
    #                                                              str(rad_skew_angle))
    #     cs.props["OriginY"] = "{}mm*sin({})+{}mm*cos({})".format(str(x), str(rad_skew_angle), str(y),
    #                                                              str(rad_skew_angle))
    #     cs.props["Phi"] = "{}deg+SkewAngle".format(str(cs.props["Phi"]))
