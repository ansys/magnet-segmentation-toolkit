# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

from ansys.aedt.core.application.variables import decompose_variable_value
from ansys.aedt.core.generic.numbers import Quantity
from ansys.aedt.core.modeler.cad.modeler import CoordinateSystem
from ansys.aedt.core.modeler.cad.modeler import FaceCoordinateSystem
from ansys.aedt.toolkits.common.backend.api import AEDTCommon

from ansys.aedt.toolkits.magnet_segmentation.backend.models import properties


class AEDTWorkflow(AEDTCommon):
    """Controls the AEDT toolkit workflow.

    This class provides methods for connecting to a selected design,
    segment and skew the motor.

    Examples
    --------
        >>> from ansys.aedt.toolkits.magnet_segmentation.backend.api import AEDTWorkflow
        >>> toolkit = AEDTWorkflow()
        >>> msg1 = toolkit.launch_aedt()
        >>> toolkit.wait_to_be_idle()
        >>> toolkit.segmentation()
        >>> toolkit.apply_skew()
        >>> toolkit.release_aedt(True, True)
    """

    def __init__(self):
        AEDTCommon.__init__(self, properties)
        self.properties = properties

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
        self.connect_design()

        # Requirements: Design needs  a design variable "HalfAxial"
        if self.aedtapp["HalfAxial"] == "1":
            self.aedtapp["HalfAxial"] = "0"

        for obj in self.aedtapp.modeler.unclassified_objects:
            obj.model = False

        self.aedtapp.set_active_design(self.properties.active_design)
        self.aedtapp.duplicate_design(self.properties.active_design)
        self.properties.active_design = self.aedtapp.design_name
        self.aedtapp.set_active_design(self.properties.active_design)
        self.properties.design_list[self.aedtapp.project_name].append(self.properties.active_design)
        self.set_properties(self.properties.model_dump())

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
        if not self.properties.is_skewed:
            magnets = self.aedtapp.modeler.get_objects_by_material(self.properties.magnets_material)
            if self.properties.rotor_material == self.properties.stator_material:
                rotor_stator = self.aedtapp.modeler.get_objects_by_material(self.properties.rotor_material)
                stator_obj = max(rotor_stator, key=attrgetter("volume"))
                rotor = [
                    x
                    for x in self.aedtapp.modeler.get_objects_by_material(self.properties.rotor_material)
                    if x != stator_obj and x.name != "Shaft"
                ][0]
            else:
                rotor = self.aedtapp.modeler.get_objects_by_material(self.properties.rotor_material)[0]

            if self.properties.rotor_slices > 1:
                # rotor segmentation
                rotor_slices = self.aedtapp.modeler.objects_segmentation(
                    rotor.id, segments=self.properties.rotor_slices, apply_mesh_sheets=False
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

        magnets = self.aedtapp.modeler.get_objects_by_material(self.properties.magnets_material)
        for magnet in magnets:
            faces = []
            mesh_sheets = []
            cs = self.aedtapp.modeler.duplicate_coordinate_system_to_global(magnet.part_coordinate_system)
            magnet.part_coordinate_system = cs.name
            self.aedtapp.modeler.set_working_coordinate_system("Global")
            if self.properties.magnet_segments_per_slice > 1:
                objects_segmentation = self.aedtapp.modeler.objects_segmentation(
                    magnet.id,
                    segments=self.properties.magnet_segments_per_slice,
                    apply_mesh_sheets=self.properties.apply_mesh_sheets,
                    mesh_sheets=self.properties.mesh_sheets_number,
                )
                if self.properties.apply_mesh_sheets:
                    magnet_segments = objects_segmentation[0]
                    mesh_sheets.extend([s.name for s in objects_segmentation[1][magnet.name]])
                else:
                    magnet_segments = objects_segmentation
                # Apply insulation
                for face in magnet_segments[magnet.name]:
                    obj = self.aedtapp.modeler.create_object_from_face(face.top_face_z)
                    faces.append(obj.top_face_z)
                [face.delete() for face in magnet_segments[magnet.name]]
            faces.extend([magnet.top_face_z, magnet.bottom_face_z])
            self.aedtapp.assign_insulating(faces, "{}_segments".format(magnet.name))
            if isinstance(cs, CoordinateSystem):
                cs.change_cs_mode(2)

        magnets = self.aedtapp.modeler.get_objects_by_material(self.properties.magnets_material)
        segments = self.aedtapp.modeler.get_objects_in_group("Insulating")

        self.properties.objects.extend([m.name for m in magnets])
        if segments:
            self.properties.objects.extend(segments)
        self.set_properties(self.properties.model_dump())

        self.aedtapp.save_project()
        self.release_aedt(False, False)
        return True

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
            self.connect_design()

            magnets = self.aedtapp.modeler.get_objects_by_material(self.properties.magnets_material)
            rotor_objects = self.aedtapp.modeler.get_objects_by_material(self.properties.rotor_material)
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
            if self.properties.rotor_material == self.properties.stator_material:
                stator_obj = max(rotor_objects, key=attrgetter("volume"))
                rotor_objects = [
                    x
                    for x in self.aedtapp.modeler.get_objects_by_material(self.properties.rotor_material)
                    if x != stator_obj and x.name != "Shaft"
                ]
            rotor_skew_ang = 0
            # rotate objects and apply skew
            for rotor_object in rotor_objects:
                if rotor_skew_ang != 0:
                    # IPM
                    obj_in_bb = self.aedtapp.modeler.objects_in_bounding_box(
                        rotor_object.bounding_box, check_lines=False, check_sheets=False
                    )
                    magnets_in_rotor_object = list(set(obj_in_bb).intersection(magnets))
                    objects_to_rotate = obj_in_bb

                    # SPM
                    # if magnets_in_rotor_object is empty it means that the magnets are not in the bounding box
                    # of the rotor object -> SPM.
                    if not magnets_in_rotor_object:
                        magnets_in_rotor_object = self._get_magnets_per_slice(magnets, rotor_object)
                        objects_to_rotate = magnets_in_rotor_object

                    sheets_to_rotate = []
                    for obj in magnets_in_rotor_object:
                        insulation = [
                            sheet for sheet in self.aedtapp.modeler.sheet_objects if obj.name in sheet.touching_objects
                        ]
                        if insulation:
                            sheets_to_rotate.extend(insulation)
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
                    for obj in objects_to_rotate + sheets_to_rotate:
                        obj.rotate(axis="Z", angle=rotor_skew_ang)

                    # It means that indep. and dep. boundaries exist -> symmetry factor != 1
                    if independent and dependent:
                        split = self.aedtapp.modeler.split(assignment=obj_in_bb, sides="Both", tool=indep.id)
                        if [s for s in split if s not in self.aedtapp.modeler.objects_by_name]:
                            self.aedtapp.odesign.Undo()
                        split_objects = self.aedtapp.modeler.split(assignment=obj_in_bb, sides="Both", tool=dep.id)
                        split_objects_with_rotor = [
                            self.aedtapp.modeler.objects_by_name[obj] for obj in split_objects[1:]
                        ]
                        if split_objects_with_rotor[1:]:
                            split_objects_without_rotor = split_objects_with_rotor[1:]
                            insulation_faces = []
                            # remove rotor object from split objects to assign insulation
                            for obj in split_objects_without_rotor:
                                # re-apply insulation only to top and bottom faces of the split magnet
                                # this does not re-apply insulation on magnet segments
                                # because it is difficult to detect which sheets are magnet segments or mesh sheets
                                if obj in self.aedtapp.modeler.sheet_objects:
                                    # insulation_faces.append(obj.faces[0])
                                    pass
                                else:
                                    insulation_faces.extend([obj.top_face_z, obj.bottom_face_z])
                            self.aedtapp.assign_insulating(insulation_faces)
                        self.aedtapp.modeler.rotate(
                            split_objects_with_rotor, self.aedtapp.AXIS.Z, -360 / self.aedtapp.symmetry_multiplier
                        )
                        self.aedtapp.modeler.unite([rotor_object, split_objects_with_rotor[0]])
                rotor_skew_ang += decompose_variable_value(self.properties.skew_angle)[0]

            # Delete and reassign the band to include all objects that have been moved in skew
            band = [bound for bound in self.aedtapp.boundaries if bound.type == "Band"]
            band_name = band[0].properties["Assignment"]
            band_angular_velocity = band[0].props["Angular Velocity"]
            band_init_pos = band[0].props["InitPos"]
            rotate_limit = band[0].props["HasRotateLimit"]
            self.aedtapp.omodelsetup.DeleteMotionSetup([band[0].name])
            self.aedtapp.assign_rotate_motion(
                self.aedtapp.modeler[band_name],
                angular_velocity=band_angular_velocity,
                start_position=band_init_pos,
                has_rotation_limits=rotate_limit,
            )
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
        self.connect_design()

        if not self.aedtapp.validate_simple():
            self.aedtapp.change_validation_settings(ignore_unclassified=True, skip_intersections=True)
        if self.aedtapp.validate_simple():
            self.aedtapp.analyze_setup(self.properties.setup_to_analyze, use_auto_settings=False)
            self.release_aedt(False, False)
            return True
        return False

    def get_magnet_loss(self):
        """Get magnet loss.

        Returns
        -------
        dict
            dictionary containing the average magnet loss value when successful, ``False`` when failed.
        """
        self.connect_design()

        try:
            self.aedtapp.post.create_report(expressions="SolidLoss", plot_name="Losses", primary_sweep_variable="Time")
            data = self.aedtapp.post.get_solution_data(
                expressions="SolidLoss", primary_sweep_variable="Time", domain="Sweep"
            )
            avg = Quantity(
                expression=sum(data.data_magnitude()) / len(data.data_magnitude()), unit=data.units_data["SolidLoss"]
            )
            avg_w = avg.to("W")
            self.release_aedt(False, False)
            return str(avg_w)
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
            List of the class:`ansys.aedt.core.modeler.cad.object3d.Object3d` classes.
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

    # @thread.launch_thread
    def _get_project_materials(self):
        """Get the project materials."""
        self.connect_design()

        if not self.aedtapp:
            return
        mats = self.aedtapp.materials.get_used_project_material_names()

        self.release_aedt(False, False)

        return mats

    def _get_design_setup_names(self):
        """Get the design setup names."""
        self.connect_design()

        setup_names = [setup.name for setup in self.aedtapp.setups]

        self.release_aedt(False, False)

        return setup_names

    def _get_magnets_per_slice(self, magnets, rotor_slice):
        """Get the magnets that touch rotor slice."""
        top_face_z_id = rotor_slice.top_face_z.id
        bottom_face_z_id = rotor_slice.bottom_face_z.id
        face = [face for face in rotor_slice.faces if face.id not in [top_face_z_id, bottom_face_z_id]][0]
        magnets_in_slice = []
        for magnet in magnets:
            magnet_face = max(magnet.faces, key=lambda f: f.area)
            if magnet_face.center[2] == face.center[2]:
                magnets_in_slice.append(magnet)

        return magnets_in_slice
