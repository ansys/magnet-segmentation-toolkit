# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from operator import attrgetter

from pyaedt.application.Variables import decompose_variable_value
from pyaedt.generic.constants import unit_converter
from pyaedt.modeler.cad.Modeler import CoordinateSystem
from pyaedt.modeler.cad.Modeler import FaceCoordinateSystem
from pyaedt.modeler.geometry_operators import GeometryOperators as go

from ansys.aedt.toolkits.magnet_segmentation.backend.common.toolkit import AEDTCommonToolkit
from ansys.aedt.toolkits.magnet_segmentation.backend.models import properties


class AEDTWorkflow(AEDTCommonToolkit):
    """Controls the AEDT toolkit workflow.

    This class provides methods for connecting to a selected design,
    segment and skew the motor.

    Examples
    --------
        >>> from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit
        >>> toolkit = Toolkit()
        >>> msg1 = toolkit.launch_aedt()
        >>> toolkit.wait_to_be_idle()
        >>> toolkit.segmentation()
        >>> toolkit.apply_skew()
        >>> toolkit.release_aedt(True, True)
    """

    def __init__(self):
        super().__init__()

    # @thread.launch_thread
    def segmentation(self):
        """Apply object segmentation.

        This method automatically segments the rotor, rotor pockets, and magnets.

        .. warning::
            This method only works if the AEDT active project has
            ``SymmetryFactor`` and ``HalfAxial`` design settings defined.

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

        vacuum_objects = [x for x in self.aedtapp.modeler.get_objects_by_material("vacuum") if x.object_type == "Solid"]
        rotor_pockets = self._get_rotor_pockets(vacuum_objects)

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

        .. warning::
            This method only works if the active AEDT project contains a shaft
            named ``Shaft``.

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
                        split = self.aedtapp.modeler.split(objects=rotor_object, sides="Both", tool=indep.id)
                        if not all([self.aedtapp.modeler[o] for o in split]):
                            self.aedtapp.odesign.Undo()
                        split = self.aedtapp.modeler.split(objects=rotor_object, sides="Both", tool=dep.id)
                        split_objects = [self.aedtapp.modeler.objects_by_name[obj] for obj in split]
                        # Get object with minimum volume
                        min_vol_object = min(split_objects, key=lambda x: x.volume).volume
                        # Get object whose volume is equal to min_vol_object
                        obj_rotate = [obj for obj in split_objects if obj.volume == min_vol_object][0]
                        # duplicate around z axis (-360/symmetry_multiplier)
                        obj_rotate.rotate(cs_axis=self.aedtapp.AXIS.Z, angle=-360 / self.aedtapp.symmetry_multiplier)
                        self.aedtapp.modeler.unite([split_objects[0], split_objects[1]])
                rotor_skew_ang += decompose_variable_value(properties.skew_angle)[0]

            self.release_aedt(False, False)
            return True
        except:
            return False

    def validate_and_analyze(self):
        """Validate and analyze the design.

        Returns
        -------
        bool
            ``True`` when successful, ``False`` when failed.
        """
        self.connect_design(app_name=list(properties.active_design.keys())[0])

        if self.aedtapp.validate_simple():
            self.aedtapp.analyze_setup(properties.setup_to_analyze, use_auto_settings=False)
            self.aedtapp.release_desktop(False, False)
            return True
        else:
            return False

    def get_magnet_loss(self):
        """Get magnet loss.

        Returns
        -------
        dict
            dictionary containing the average magnet loss value when successful, ``False`` when failed.
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
            return report_dict
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
