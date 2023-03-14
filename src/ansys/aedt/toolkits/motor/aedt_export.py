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
        # clear unclassified objects ? -> Uncheck model in Properties

    def mesh_settings(self):
        # apply mesh sizing
        # windings (5mm)
        copper_objs_list = self.maxwell.modeler.get_objects_by_material("Copper (Pure)_50C")
        self.maxwell.mesh.assign_length_mesh(copper_objs_list, maxlength=8, meshop_name="copper_objs_mesh")
        # rotor - stator (8mm)
        rotor_stator = self.maxwell.modeler.get_objects_by_material("M250-35A_20C")
        self.maxwell.mesh.assign_length_mesh(rotor_stator, maxlength=8, meshop_name="rotor_stator_mesh")
        # magnets (2mm)
        magnets = self.maxwell.modeler.get_objects_by_material("N30UH_20C")
        self.maxwell.mesh.assign_length_mesh(magnets, maxlength=2, meshop_name="magnets_mesh")

    def apply_boundary_conditions(self):
        # apply insulating BC on all magnet faces
        magnets = self.maxwell.modeler.get_objects_by_material("N30UH_20C")
        self.maxwell.assign_insulating(magnets, "magnets_insulation")
        # apply symmetry (flux tangential) on symmetry plane
        # HOW TO GET ALL FACES GIVEN A SPECIFIC PLANE?

        # Set Eddy Effects on Magnets (already done by export)

    def save_and_close(self):

        self.maxwell.save_project(os.path.join(self.working_dir, "{}.aedt".format(self.maxwell.project_name)))

        self._desktop.release_desktop(False, False)

        # maxwell.analyze_all()
        # maxwell.create_output_variable("Mech_deg_1", "cum_integ(Moving1.Speed)*4")
        # maxwell.post.create_report("-Moving1.Torque", primary_sweep_variable="Mech_deg_1", domain="Sweep", variations={"Time": ["All"]})
        # solutions = maxwell.post.get_solution_data("-Moving1.Torque", primary_sweep_variable="Time")
        # solutions.plot()
