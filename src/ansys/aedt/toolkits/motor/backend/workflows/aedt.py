from operator import attrgetter

from pyaedt.application.Variables import decompose_variable_value
from pyaedt.modeler.cad.Modeler import CoordinateSystem
from pyaedt.modeler.cad.Modeler import FaceCoordinateSystem
from pyaedt.modeler.geometry_operators import GeometryOperators as go

# from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger
from ansys.aedt.toolkits.motor.backend.common.toolkit import AEDTCommonToolkit
from ansys.aedt.toolkits.motor.backend.models import properties


class AEDTWorkflow(AEDTCommonToolkit):
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

    def __init__(self):
        super().__init__()

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

        self.aedtapp.set_active_design(properties.active_design["Maxwell3d"])
        self.aedtapp.duplicate_design(properties.active_design["Maxwell3d"])
        properties.active_design = {"Maxwell3d": self.aedtapp.design_name}
        self.aedtapp.set_active_design(properties.active_design["Maxwell3d"])
        properties.designs_by_project_name[self.aedtapp.project_name].append(properties.active_design)
        self.set_properties(properties.model_dump())

        # try:
        if [bound for bound in self.aedtapp.boundaries if bound.type == "Insulating"]:
            for bound in self.aedtapp.boundaries[:]:
                if (
                    bound.type == "Insulating"
                    and bound.name in self.aedtapp.odesign.GetChildObject("Boundaries").GetChildNames()
                ):
                    bound.delete()

        # If model is already skewed only magnets can be segmented
        if not properties.is_skewed:
            magnets = self.aedtapp.modeler.get_objects_by_material(properties.magnets_material)
            if properties.rotor_material == properties.stator_material:
                if properties.motor_type == "IPM":
                    for obj in self.aedtapp.modeler.get_objects_by_material(properties.rotor_material):
                        if [i for i in magnets if i in self.aedtapp.modeler.objects_in_bounding_box(obj.bounding_box)]:
                            rotor = obj
                elif properties.motor_type == "SPM":
                    for obj in self.aedtapp.modeler.get_objects_by_material(properties.rotor_material):
                        if not [
                            i for i in magnets if i in self.aedtapp.modeler.objects_in_bounding_box(obj.bounding_box)
                        ]:
                            rotor = obj
                else:
                    raise RuntimeError(f"Motor type {properties.motor_type} is not yet handled.")
            else:
                rotor = self.aedtapp.modeler.get_objects_by_material(properties.rotor_material)[0]

            vacuum_objects = [
                x for x in self.aedtapp.modeler.get_objects_by_material("vacuum") if x.object_type == "Solid"
            ]
            rotor_pockets = self._get_rotor_pockets(vacuum_objects)

            if properties.rotor_slices > 1:
                # rotor segmentation
                rotor_slices = self.aedtapp.modeler.objects_segmentation(
                    rotor.id, segments_number=properties.rotor_slices, apply_mesh_sheets=False
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

        magnets = self.aedtapp.modeler.get_objects_by_material(properties.magnets_material)
        for magnet in magnets:
            cs = self.aedtapp.modeler.duplicate_coordinate_system_to_global(magnet.part_coordinate_system)
            magnet.part_coordinate_system = cs.name
            self.aedtapp.modeler.set_working_coordinate_system("Global")
            objects_segmentation = self.aedtapp.modeler.objects_segmentation(
                magnet.id,
                segments_number=properties.magnet_segments_per_slice,
                apply_mesh_sheets=properties.apply_mesh_sheets,
                mesh_sheets_number=properties.mesh_sheets_number,
            )
            faces = []
            if properties.apply_mesh_sheets:
                magnet_segments = objects_segmentation[0]
            else:
                magnet_segments = objects_segmentation
            for face in magnet_segments[magnet.name]:
                obj = self.aedtapp.modeler.create_object_from_face(face.top_face_z)
                faces.append(obj.top_face_z)
            [face.delete() for face in magnet_segments[magnet.name]]
            self.aedtapp.assign_insulating(faces, "{}_segments".format(magnet.name))
            if isinstance(cs, CoordinateSystem):
                self._update_cs(cs)

        self.aedtapp.save_project()
        self.release_aedt(False, False)
        return True
        # except:
        #     return False

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

            magnets = self.aedtapp.modeler.get_objects_by_material(properties.magnets_material)
            rotor_objects = self.aedtapp.modeler.get_objects_by_material(properties.rotor_material)
            # Independent and dependent boundary conditions can be assigned either to an object or an object face
            independent = [bound for bound in self.aedtapp.boundaries if bound.type == "Independent"]
            dependent = [bound for bound in self.aedtapp.boundaries if bound.type == "Dependent"]
            # If no indep. o dep. boundary are found it means that the symmetry factor is 1 -> whole motor.
            if independent or dependent:
                bound_indep_props = independent[0].props
                if "Objects" in bound_indep_props:
                    bound_indep_id = bound_indep_props["Objects"][0]
                    indep = self.aedtapp.modeler.objects[bound_indep_id]
                elif "Faces" in bound_indep_props:
                    bound_indep_id = bound_indep_props["Faces"][0]
                    obj = [o for o in self.aedtapp.modeler.object_list for f in o.faces if f.id == bound_indep_id][0]
                    indep = [f for f in obj.faces if f.id == bound_indep_id][0]
                bound_dep_props = dependent[0].props
                if "Objects" in bound_indep_props:
                    bound_dep_id = bound_dep_props["Objects"][0]
                    dep = self.aedtapp.modeler.objects[bound_dep_id]
                elif "Faces" in bound_indep_props:
                    bound_dep_id = bound_dep_props["Faces"][0]
                    obj = [o for o in self.aedtapp.modeler.object_list for f in o.faces if f.id == bound_dep_id][0]
                    dep = [f for f in obj.faces if f.id == bound_dep_id][0]

            # check whether stator has same rotor material
            if properties.rotor_material == properties.stator_material:
                stator_obj = max(rotor_objects, key=attrgetter("volume"))
                rotor_objects = [
                    x
                    for x in self.aedtapp.modeler.get_objects_by_material(properties.rotor_material)
                    if x != stator_obj and x.name != "Shaft"
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

                    # It means that indep. and dep. boundaries exist -> symmetry factor != 1
                    if independent and dependent:
                        # duplicate around z axis (-360/symmetry_multiplier)
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
                rotor_skew_ang += decompose_variable_value(properties.skew_angle)[0]

            self.release_aedt(False, False)
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

    # @thread.launch_thread
    def _get_project_materials(self):
        """Get the project materials."""
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        mats = self.aedtapp.materials.get_used_project_material_names()

        self.aedtapp.release_desktop(False, False)
        self.aedtapp = None

        return mats
