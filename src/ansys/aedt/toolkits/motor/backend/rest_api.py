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
    logger.info("[POST] /Initialize Motor-CAD.")

    response = service.init_motorcad()
    if response:
        return jsonify("Motor-CAD initialized successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD initialization was unsuccessful."), 500


@app.route("/load_mot_file", methods=["POST"])
def load_mot_file_call():
    logger.info("[POST] /load Motor-CAD file.")

    response = service.load_mcad_file()
    if response:
        return jsonify("Motor-CAD file loaded successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD file load was unsuccessful."), 500


@app.route("/set_Emag_model", methods=["POST"])
def set_emag_model_call():
    logger.info("[POST] /Set Motor-CAD Emag model.")

    response = service.set_emag_model()
    if response:
        return jsonify("Motor-CAD Emag model set successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD Emag model set was unsuccessful."), 500


@app.route("/lab_calculation", methods=["POST"])
def set_lab_calculation_call():
    logger.info("[POST] /Perform LAB calculation.")

    response = service.lab_performance_calculation()
    if response:
        return jsonify("LAB calculation ran successfully."), 200
    else:
        return jsonify("Failure: LAB calculation was unsuccessful."), 500


@app.route("/lab_op_point", methods=["POST"])
def set_lab_op_point_call():
    logger.info("[POST] /Set LAB op-point.")

    response = service.lab_operating_point()
    if response:
        return jsonify("LAB op-point set successfully."), 200
    else:
        return jsonify("Failure: LAB op-point set was unsuccessful."), 500


@app.route("/run_emag_calculation", methods=["POST"])
def run_emag_calculation_call():
    logger.info("[POST] /Run Emag calculation.")

    response = service.emag_calculation()
    if response:
        return jsonify("Emag calculation ran successfully."), 200
    else:
        return jsonify("Failure: Emag calculation was unsuccessful."), 500


@app.route("/set_thermal_calculation", methods=["POST"])
def set_thermal_calculation_call():
    magnet_losses = request.args.get("magnet_losses")
    logger.info("[POST] /Set thermal calculation.")

    response = service.set_thermal(magnet_losses)
    if response:
        return jsonify("Thermal calculation set successfully."), 200
    else:
        return jsonify("Failure: Thermal calculation set was unsuccessful."), 500


@app.route("/run_thermal_calculation", methods=["POST"])
def run_thermal_calculation_call():
    logger.info("[POST] /Run thermal calculation.")

    response = service.thermal_calculation()
    if response:
        return jsonify("Thermal calculation ran successfully."), 200
    else:
        return jsonify("Failure: Thermal calculation was ununsuccessful."), 500


@app.route("/export_model", methods=["POST"])
def export_model_call():
    logger.info("[POST] /Export Motor-CAD model.")

    response = service.export_settings()
    if response:
        return jsonify("Motor-CAD model exported successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model export was unsuccessful."), 500


@app.route("/save", methods=["POST"])
def save_call():
    logger.info("[POST] /Save Motor-CAD model.")

    response = service.save()
    if response:
        return jsonify("Motor-CAD model saved successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model save was unsuccessful."), 500


@app.route("/close", methods=["POST"])
def close_call():
    logger.info("[POST] /Close Motor-CAD model.")

    response = service.save()
    if response:
        return jsonify("Motor-CAD model closed successfully."), 200
    else:
        return jsonify("Failure: Motor-CAD model close was unsuccessful."), 500


@app.route("/set_aedt_model", methods=["POST"])
def set_aedt_model_call():
    logger.info("[POST] /Set AEDT model.")

    response = service.set_model()
    if response:
        return jsonify("AEDT model set successfully."), 200
    else:
        return jsonify("Failure: AEDT model set was unsuccessful."), 500


@app.route("/get_project_materials", methods=["GET"])
def get_materials_call():
    logger.info("[GET] /Get project materials.")

    response = service._get_project_materials()
    if response:
        return response
    else:
        return jsonify("Get project material was unsuccessful."), 500


@app.route("/analyze_model", methods=["POST"])
def analyze_model_call():
    logger.info("[POST] /Analyze AEDT model.")

    response = service.analyze_model()
    if response:
        return jsonify("AEDT model analyzed successfully."), 200
    else:
        return jsonify("Failure: AEDT model analysis was unsuccessful."), 500


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
        return jsonify("Failure: Magnet losses calculation was unsuccessful."), 500


@app.route("/apply_segmentation", methods=["POST"])
def magnets_segmentation_call():
    logger.info("[POST] /Apply magnets segmentation.")

    response = service.segmentation()
    if response:
        return (
            jsonify("Magnets segmentation applied successfully."),
            200,
        )
    else:
        return jsonify("Failure: Magnets segmentation application was unsuccessful."), 500


@app.route("/apply_skew", methods=["POST"])
def apply_skew_call():
    logger.info("[POST] /Apply skew.")

    response = service.apply_skew()
    if response:
        return (
            jsonify("Skew angle applied successfully."),
            200,
        )
    else:
        return jsonify("Failure: Skew angle application was unsuccessful."), 500


if __name__ == "__main__":
    app.debug = True
    server = MultithreadingServer()
    server.run(host=settings["url"], port=settings["port"], app=app)
