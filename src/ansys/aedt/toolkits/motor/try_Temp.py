import tempfile
import os
import ansys.motorcad.core as pymotorcad

dirpath=tempfile.mkdtemp()

working_folder=dirpath

if os.path.isdir(working_folder) is False:
    print("Working folder does not exist. Choose a folder that exists and try again.")
    print(working_folder)
    exit()

print(working_folder)
mcad = pymotorcad.MotorCAD(reuse_parallel_instances=True)
# Disable all popup messages from Motor-CAD.
mcad.set_variable("MessageDisplayState", 2)
# ------------------------------
mcad.load_template("e9")
# Save the file.
filename = os.path.join(working_folder, "test_e9.mot")
# Show magnetic context
# Hybrid FEA ac winding losses
mcad.show_magnetic_context()
# Display scripting tab
mcad.display_screen("Scripting")
# enabling the hybrid AC loss model
mcad.set_variable("ProximityLossModel", 1)
mcad.set_variable("NumberOfCuboids", 6)
# setting the axial magnet segments
mcad.set_variable("AxialSegments", 6)
# %%

# ------------------------------
mcad.save_to_file(filename)
# -----------------------------------
# %%
# LAB Module
# -----------
# Set build options for the lab model.
mcad.set_variable("ModelType_MotorLAB", 2)  # Model type: Saturation Model (Full Cycle)
mcad.set_variable("SatModelPoints_MotorLAB", 1)  # Model Resolution : Fine (30 Points)
mcad.set_variable("LossModel_Lab", 1)  # Loss Model : FEA Map
mcad.set_variable("ACLossMethod_Lab", 0)  # AC Loss Model : Hybrid Method
mcad.set_variable("ModelBuildSpeed_MotorLAB", 10000)  # Max speed
mcad.set_variable("MaxModelCurrent_MotorLAB", 480)  # Max current
mcad.set_variable("BuildSatModel_MotorLAB", True)  # Enable Saturation model
mcad.set_variable("BuildLossModel_MotorLAB", True)  # Enable Loss model

# %%
# Show the lab context.
mcad.set_motorlab_context()

# %%
# Build the model.
# mcad.clear_model_build_lab()
# mcad.build_model_lab()
# ------------------------------

# -----------------------------------
mcad.load_template("Test_e9_built")

# Peak performance  Torque-Speed curve
mcad.set_variable("EmagneticCalcType_Lab", 0)  # Calc type: Max Torque speed curve
mcad.set_variable("SpeedMax_MotorLAB", 10000)  # Max speed for TS curve
mcad.set_variable("SpeedMin_MotorLAB", 0)  # Min speed for TS curve
mcad.set_variable("Speedinc_MotorLAB", 500)  # Step size
mcad.set_variable("OperatingMode_Lab", 0)  # Motor mode only
mcad.calculate_magnetic_lab()  # calculate Emagnetic Performance
# mcad.show_results_viewer_lab("Electromagnetic")  #Load result viewer

#plot torque speed curve
# TS_matfile= os.path.join(working_folder, r"test_e9\Lab\MotorLAB_elecdata.mat")
#
# TS_curve= loadmat(TS_matfile)



### Continuous performance operating points
mcad.set_variable("LabMagneticCoupling", 1)  # Send operating point to emag
mcad.set_variable("OpPointSpec_MotorLAB", 2)  # Max temp definition for operating point
mcad.set_variable(
    "ThermCalcType_MotorLAB", 0
)  # Run steady state thermal calc to save computation time
mcad.set_variable(
    "ThermalMapType_Lab", 0
)  # Thermal envelope option (relevant for max curve value option only)
mcad.set_variable("MaxWindTemp_MotorLAB", 140)  # Set winding temperature
mcad.set_variable("StatorTempDemand_Lab", 140)  # Set winding temperature
mcad.set_variable("MaxMagnet_MotorLAB", 160)  # Set magnet temperature
mcad.set_variable("RotorTempDemand_Lab", 160)  # Set magnet temperature
mcad.set_variable("SpeedDemand_MotorLAB", 4500)
mcad.calculate_operating_point_lab()  # calculate operating point
Shaft_power = mcad.get_variable("LabOpPoint_ShaftPower")
Efficiency = mcad.get_variable("LabOpPoint_Efficiency")
print("Shaft Power", round(Shaft_power / 1000, 2), "kW")
print("Efficiency", round(Efficiency, 2), "%")
#
#
# Simulate the Operating point in Emag Module

# Show the magnetic context.
mcad.show_magnetic_context()

# Disable all performance tests except the ones for transient torque.
mcad.set_variable("BackEMFCalculation", False)
mcad.set_variable("CoggingTorqueCalculation", False)
mcad.set_variable("ElectromagneticForcesCalc_OC", False)
mcad.set_variable("TorqueSpeedCalculation", False)
mcad.set_variable("DemagnetizationCalc", False)
mcad.set_variable("ElectromagneticForcesCalc_Load", False)
mcad.set_variable("InductanceCalc", False)
mcad.set_variable("BPMShortCircuitCalc", False)

# %%
# Enable transient torque.
mcad.set_variable("TorqueCalculation", True)
# --------------
# Run the simulation.
mcad.do_magnetic_calculation()
output_power = mcad.get_variable("OutputPower")
print("Output Power Emag", round(output_power / 1000, 2), "kW")




