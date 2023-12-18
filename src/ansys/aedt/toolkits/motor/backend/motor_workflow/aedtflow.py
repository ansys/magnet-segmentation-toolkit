from operator import attrgetter

from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.constants import unit_converter
from pyaedt.modeler.cad.Modeler import CoordinateSystem
from pyaedt.modeler.cad.Modeler import FaceCoordinateSystem
from pyaedt.modeler.geometry_operators import GeometryOperators as go

from ansys.aedt.toolkits.motor.backend.common.aedt_toolkit import AEDTToolkit
from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.properties import properties


class AedtFlow(AEDTToolkit):
    """Controls the AEDT toolkit workflow.

    This class provides methods for connecting to a selected design.

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

    # FIXME: use super
    def __init__(self):
        AEDTToolkit.__init__(self)

    def analyze_model(self):
        """Analyze model.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        try:
            self.aedtapp.analyze_setup(properties.SetupToAnalyze)
            self.aedtapp.release_desktop(False, False)
            self.aedtapp = None
            return True
        except:
            return False

    def get_losses_from_reports(self):
        """Get magnet losses from reports.

        Returns
        -------
        dict
            Average values plus units for the reports specified in the JSON file.
        """
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        try:
            report_dict = {}
            self.aedtapp.post.create_report(expressions="SolidLoss", plotname="Losses", primary_sweep_variable="Time")
            data = self.aedtapp.post.get_solution_data(expressions="SolidLoss", primary_sweep_variable="Time")
            avg = sum(data.data_magnitude()) / len(data.data_magnitude())
            avg = unit_converter(avg, "Power", data.units_data["SolidLoss"], "W")
            report_dict["SolidLoss"] = {"Value": round(avg, 4), "Unit": "W"}
            self.aedtapp.release_desktop(False, False)
            self.aedtapp = None
            return True, report_dict
        except:
            return False

    # @thread.launch_thread
    def segmentation(self):
        """Apply object segmentation.

        This method automatically segments the rotor, rotor pockets, and magnets.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        # Requirements: Design needs  a design variable "HalfAxial"
        if self.aedtapp["HalfAxial"] == "1":
            self.aedtapp["HalfAxial"] = "0"

        for obj in self.aedtapp.modeler.unclassified_objects:
            obj.model = False

        if not self.aedtapp:
            logger.error("AEDT is not initialized.")
            return False

        self.aedtapp.set_active_design(properties.active_design["Maxwell3d"])
        self.aedtapp.duplicate_design(properties.active_design["Maxwell3d"])
        properties.active_design = {"Maxwell3d": self.aedtapp.design_name}
        self.aedtapp.set_active_design(properties.active_design["Maxwell3d"])
        properties.design_list[self.aedtapp.project_name].append(properties.active_design)
        self.set_properties(properties)

        try:
            if [bound for bound in self.aedtapp.boundaries if bound.type == "Insulating"]:
                for bound in self.aedtapp.boundaries[:]:
                    if (
                        bound.type == "Insulating"
                        and bound.name in self.aedtapp.odesign.GetChildObject("Boundaries").GetChildNames()
                    ):
                        bound.delete()

            self.aedtapp["MagnetsSegmentsPerSlice"] = properties.MagnetsSegmentsPerSlice

            # If model is already skewed only magnets can be segmented
            if not properties.IsSkewed:
                self.aedtapp["RotorSlices"] = properties.RotorSlices

                magnets = self.aedtapp.modeler.get_objects_by_material(properties.MagnetsMaterial)
                if properties.RotorMaterial == properties.StatorMaterial:
                    if properties.MotorType == "IPM":
                        for obj in self.aedtapp.modeler.get_objects_by_material(properties.RotorMaterial):
                            if [
                                i
                                for i in magnets
                                if i in self.aedtapp.modeler.objects_in_bounding_box(obj.bounding_box)
                            ]:
                                rotor = obj
                    elif properties.MotorType == "SPM":
                        for obj in self.aedtapp.modeler.get_objects_by_material(properties.RotorMaterial):
                            if not [
                                i
                                for i in magnets
                                if i in self.aedtapp.modeler.objects_in_bounding_box(obj.bounding_box)
                            ]:
                                rotor = obj
                else:
                    rotor = self.aedtapp.modeler.get_objects_by_material(properties.RotorMaterial)[0]

                vacuum_objects = [
                    x for x in self.aedtapp.modeler.get_objects_by_material("vacuum") if x.object_type == "Solid"
                ]
                rotor_pockets = self._get_rotor_pockets(vacuum_objects)

                if int(properties.RotorSlices) > 1:
                    # rotor segmentation
                    rotor_slices = self.aedtapp.modeler.objects_segmentation(
                        rotor.id, segments_number=int(self.aedtapp["RotorSlices"]), apply_mesh_sheets=False
                    )
                    # rotor and rotor pockets split
                    rotor_objs = [rotor.name]
                    magnets_names = [x.name for x in magnets]
                    if len(rotor_pockets) > 0:
                        rotor_pockets_names = [x.name for x in rotor_pockets]
                    for slice in rotor_slices[rotor.name]:
                        rotor_objs = self.aedtapp.modeler.split(rotor_objs, sides="Both", tool=slice.faces[0])
                        magnets_names = self.aedtapp.modeler.split(magnets_names, sides="Both", tool=slice.faces[0])
                        if len(rotor_pockets) > 0:
                            rotor_pockets_names = self.aedtapp.modeler.split(
                                rotor_pockets_names, sides="Both", tool=slice.faces[0]
                            )
                        self.aedtapp.modeler.delete_objects_containing(slice.name)
                    rotor_slices.clear()

            magnets = self.aedtapp.modeler.get_objects_by_material(properties.MagnetsMaterial)
            for magnet in magnets:
                cs = self.aedtapp.modeler.duplicate_coordinate_system_to_global(magnet.part_coordinate_system)
                magnet.part_coordinate_system = cs.name
                self.aedtapp.modeler.set_working_coordinate_system("Global")
                magnet_segments = self.aedtapp.modeler.objects_segmentation(
                    magnet.id,
                    segments_number=self.aedtapp.variable_manager["MagnetsSegmentsPerSlice"].numeric_value,
                    apply_mesh_sheets=False,
                )
                faces = []
                for face in magnet_segments[magnet.name]:
                    obj = self.aedtapp.modeler.create_object_from_face(face.top_face_z)
                    faces.append(obj.top_face_z)
                [face.delete() for face in magnet_segments[magnet.name]]
                self.aedtapp.assign_insulating(faces, "{}_segments".format(magnet.name))
                if isinstance(cs, CoordinateSystem):
                    self._update_cs(cs)

            self.aedtapp.save_project()
            self.aedtapp.release_desktop(False, False)
            self.aedtapp = None
            return True
        except:
            return False

    # @thread.launch_thread
    def apply_skew(self):
        """Apply skew to rotor slices.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        try:
            self.connect_design(app_name=list(properties.active_design.keys())[0])

            magnets = self.aedtapp.modeler.get_objects_by_material(properties.MagnetsMaterial)
            rotor_objects = self.aedtapp.modeler.get_objects_by_material(properties.RotorMaterial)
            # Independent and dependent boundary conditions can be assigned either to an object or an object face
            bound_indep_props = [bound for bound in self.aedtapp.boundaries if bound.type == "Independent"][0].props
            if "Objects" in bound_indep_props:
                bound_indep_id = bound_indep_props["Objects"][0]
                indep = self.aedtapp.modeler.objects[bound_indep_id]
            elif "Faces" in bound_indep_props:
                bound_indep_id = bound_indep_props["Faces"][0]
                obj = [o for o in self.aedtapp.modeler.object_list for f in o.faces if f.id == bound_indep_id][0]
                indep = [f for f in obj.faces if f.id == bound_indep_id][0]
            bound_dep_props = [bound for bound in self.aedtapp.boundaries if bound.type == "Dependent"][0].props
            if "Objects" in bound_indep_props:
                bound_dep_id = bound_dep_props["Objects"][0]
                dep = self.aedtapp.modeler.objects[bound_dep_id]
            elif "Faces" in bound_indep_props:
                bound_dep_id = bound_dep_props["Faces"][0]
                obj = [o for o in self.aedtapp.modeler.object_list for f in o.faces if f.id == bound_dep_id][0]
                dep = [f for f in obj.faces if f.id == bound_dep_id][0]

            # check whether stator has same rotor material
            if properties.RotorMaterial == properties.StatorMaterial:
                stator_obj = max(rotor_objects, key=attrgetter("volume"))
                rotor_objects = [
                    x for x in self.aedtapp.modeler.get_objects_by_material(properties.RotorMaterial) if x != stator_obj
                ]
            objs_in_bb = {}
            rotor_skew_ang = 0
            # rotate objects and apply skew
            for rotor_object in rotor_objects:
                if rotor_skew_ang != 0:
                    objs_in_bb[rotor_object.name] = self.aedtapp.modeler.objects_in_bounding_box(
                        rotor_object.bounding_box
                    )
                    for obj in objs_in_bb[rotor_object.name]:
                        if obj in magnets:
                            magnet_cs = [
                                cs
                                for cs in self.aedtapp.modeler.coordinate_systems
                                if cs.name == obj.part_coordinate_system
                            ][0]
                            if isinstance(magnet_cs, CoordinateSystem):
                                magnet_cs.props["Phi"] = "{}+{}deg".format(magnet_cs.props["Phi"], rotor_skew_ang)
                            elif isinstance(magnet_cs, FaceCoordinateSystem):
                                magnet_cs.props["ZRotationAngle"] = "{}deg".format(rotor_skew_ang)
                        self.aedtapp.modeler.set_working_coordinate_system("Global")
                        obj.rotate(cs_axis="Z", angle=rotor_skew_ang)

                    # duplicate around z axis (-360/symmetry_factor)
                    self.aedtapp.modeler.duplicate_around_axis(
                        rotor_object,
                        cs_axis=self.aedtapp.AXIS.Z,
                        angle=-360 / self.aedtapp.symmetry_multiplier,
                        nclones=2,
                        create_new_objects=False,
                    )
                    # split - Initial Position 0deg on x-axis
                    self.aedtapp.modeler.split(objects=rotor_object, sides="PositiveOnly", tool=indep.id)
                    self.aedtapp.modeler.split(objects=rotor_object, sides="NegativeOnly", tool=dep.id)
                rotor_skew_ang += decompose_variable_value(properties.SkewAngle)[0]

            self.aedtapp.release_desktop(False, False)
            self.aedtapp = None
            return True
        except:
            return False

    def _get_rotor_pockets(self, vacuum_objects):
        """Get the rotor pockets if any.

        Parameters
        ----------
        vacuum_objects : list
            List of vacuum objects.

        Returns
        -------
        list
            List of the class:`pyaedt.modeler.cad.object3d.Object3d` classes.
        """
        rotor_pockets = []
        for obj in vacuum_objects:
            obj_in_bb = self.aedtapp.modeler.objects_in_bounding_box(
                obj.bounding_box, check_lines=False, check_sheets=False
            )
            obj_in_bb.remove(obj)
            if isinstance(obj_in_bb, list) and len(obj_in_bb) == 1:
                rotor_pockets.append(obj)
        return rotor_pockets

    def _update_cs(self, cs):
        """Update the coordinate system to Euler ZYZ mode.

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

        # rad_skew_angle = go.deg2rad(properties.SkewAngle)
        # cs.props["OriginX"] = "{}mm*cos({})-{}mm*sin({})".format(str(x), str(rad_skew_angle), str(y),
        #                                                          str(rad_skew_angle))
        # cs.props["OriginY"] = "{}mm*sin({})+{}mm*cos({})".format(str(x), str(rad_skew_angle), str(y),
        #                                                          str(rad_skew_angle))
        # cs.props["Phi"] = "{}deg+SkewAngle".format(str(cs.props["Phi"]))

    # @thread.launch_thread
    def _get_project_materials(self):
        """Get the project materials."""
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        mats = self.aedtapp.materials.get_used_project_material_names()

        self.aedtapp.release_desktop(False, False)
        self.aedtapp = None

        return mats
