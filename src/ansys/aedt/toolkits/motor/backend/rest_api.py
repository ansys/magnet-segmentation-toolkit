from flask import request

from ansys.aedt.toolkits.motor.backend.common.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.motor.backend.common.rest_api_generic import app
from ansys.aedt.toolkits.motor.backend.common.rest_api_generic import jsonify
from ansys.aedt.toolkits.motor.backend.common.rest_api_generic import logger
from ansys.aedt.toolkits.motor.backend.common.rest_api_generic import service
from ansys.aedt.toolkits.motor.backend.common.rest_api_generic import settings

# Toolkit entrypoints


@app.route("/init_motorcad", methods=["POST"])
def init_motorcad_call():
    logger.info("[POST] /initialize Motor-CAD.")

    response = service.init_motorcad()
    if response:
        return jsonify("Motor-CAD initialized."), 200
    else:
        return jsonify("Failure: Motor-CAD not initialized."), 500


@app.route("/load_mot_file", methods=["POST"])
def load_mot_file_call():
    logger.info("[POST] /load Motor-CAD file.")

    response = service.load_mcad_file()
    if response:
        return jsonify("Motor-CAD file loaded."), 200
    else:
        return jsonify("Failure: Motor-CAD file not loaded."), 500


@app.route("/set_Emag_model", methods=["POST"])
def set_emag_model_call():
    logger.info("[POST] /Set Motor-CAD Emag model.")

    response = service.set_emag_model()
    if response:
        return jsonify("Motor-CAD Emag model set."), 200
    else:
        return jsonify("Failure: Motor-CAD Emag model not set."), 500


@app.route("/lab_calculation", methods=["POST"])
def set_lab_calculation_call():
    logger.info("[POST] /Perform LAB calculation.")

    response = service.lab_performance_calculation()
    if response:
        return jsonify("Perform LAB calculation successful."), 200
    else:
        return jsonify("Failure: Perform LAB calculation unsuccessful."), 500


@app.route("/lab_op_point", methods=["POST"])
def set_lab_op_point_call():
    logger.info("[POST] /Set LAB op-point.")

    response = service.lab_operating_point()
    if response:
        return jsonify("LAB op-point successfully set."), 200
    else:
        return jsonify("Failure: LAB op-point."), 500


@app.route("/run_emag_calculation", methods=["POST"])
def run_emag_calculation_call():
    logger.info("[POST] /Run Emag calculation.")

    response = service.emag_calculation()
    if response:
        return jsonify("Emag calculation run successfully."), 200
    else:
        return jsonify("Failure: Emag calculation unsuccessful."), 500


@app.route("/set_thermal_calculation", methods=["POST"])
def set_thermal_calculation_call():
    magnet_losses = request.args.get("magnet_losses")
    logger.info("[POST] /Set Thermal calculation.")

    response = service.set_thermal(magnet_losses)
    if response:
        return jsonify("Thermal calculation set successfully."), 200
    else:
        return jsonify("Failure: Set thermal calculation unsuccessful."), 500


@app.route("/run_thermal_calculation", methods=["POST"])
def run_thermal_calculation_call():
    logger.info("[POST] /Run Thermal calculation.")

    response = service.thermal_calculation()
    if response:
        return jsonify("Thermal calculation run successfully."), 200
    else:
        return jsonify("Failure: Run thermal calculation unsuccessful."), 500


@app.route("/export_model", methods=["POST"])
def export_model_call():
    logger.info("[POST] /Export Motor-CAD model.")

    response = service.export_settings()
    if response:
        return jsonify("Motor-CAD model exported successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model export unsuccessful."), 500


@app.route("/save", methods=["POST"])
def save_call():
    logger.info("[POST] /Save Motor-CAD model.")

    response = service.save()
    if response:
        return jsonify("Motor-CAD model saved successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model unsuccessfully saved."), 500


@app.route("/close", methods=["POST"])
def close_call():
    logger.info("[POST] /Close Motor-CAD model.")

    response = service.save()
    if response:
        return jsonify("Motor-CAD model closed successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model unsuccessfully saved."), 500


@app.route("/set_aedt_model", methods=["POST"])
def set_aedt_model_call():
    logger.info("[POST] /Set AEDT model.")

    response = service.set_model()
    if response:
        return jsonify("AEDT model set successfully."), 200
    else:
        return jsonify("Failure: AEDT model unsuccessfully set."), 500


@app.route("/get_project_materials", methods=["GET"])
def get_materials_call():
    logger.info("[GET] /Get Project Materials.")

    response = service._get_project_materials()
    if response:
        return response
    else:
        return jsonify("Get project material failed."), 500


@app.route("/analyze_model", methods=["POST"])
def analyze_model_call():
    logger.info("[POST] /Analyze model AEDT model.")

    response = service.analyze_model()
    if response:
        return jsonify("AEDT model analyzed successfully."), 200
    else:
        return jsonify("Failure: AEDT model unsuccessfully analyzed."), 500


@app.route("/get_magnet_losses", methods=["POST"])
def get_magnet_losses_call():
    logger.info("[POST] /Get magnet losses.")

    response = service.get_losses_from_reports()
    if response[0]:
        return (
            jsonify(response[1]),
            200,
        )
    else:
        return jsonify("Failure: Magnet losses unsuccessfully calculated."), 500


@app.route("/apply_segmentation", methods=["POST"])
def magnets_segmentation_call():
    logger.info("[POST] /Apply magnets segmentation.")

    response = service.segmentation()
    if response:
        return (
            jsonify("Magnets segmentation successfully applied."),
            200,
        )
    else:
        return jsonify("Failure: Magnets segmentation failed."), 500


@app.route("/apply_skew", methods=["POST"])
def apply_skew_call():
    logger.info("[POST] /Apply skew.")

    response = service.apply_skew()
    if response:
        return (
            jsonify("Skew angle successfully applied."),
            200,
        )
    else:
        return jsonify("Failure: Apply skew angle was unsuccessful."), 500


if __name__ == "__main__":
    app.debug = True
    server = MultithreadingServer()
    server.run(host=settings["url"], port=settings["port"], app=app)
