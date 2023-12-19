# from flask import request

from ansys.aedt.toolkits.motor.backend.common.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.motor.backend.common.rest_api import app
from ansys.aedt.toolkits.motor.backend.common.rest_api import jsonify
from ansys.aedt.toolkits.motor.backend.common.rest_api import logger
from ansys.aedt.toolkits.motor.backend.common.rest_api import service
from ansys.aedt.toolkits.motor.backend.common.rest_api import settings

# Toolkit entrypoints


@app.route("/project_materials", methods=["GET"])
def get_materials():
    logger.info("[GET] /Get project materials.")

    response = service._get_project_materials()
    if response:
        return response
    else:
        return jsonify("Get project material was unsuccessful."), 500


# FIXME: should this call be modified into GET ?
@app.route("/analyze_model", methods=["POST"])
def analyze_model():
    logger.info("[POST] /Analyze AEDT model.")

    response = service.analyze_model()
    if response:
        return jsonify("AEDT model analyzed successfully."), 200
    else:
        return jsonify("Failure: AEDT model analysis was unsuccessful."), 500


@app.route("/magnet_losses", methods=["GET"])
def get_magnet_losses():
    logger.info("[GET] /Get magnet losses.")

    response = service.get_losses_from_reports()
    if response[0]:
        return (
            jsonify(response[1]),
            200,
        )
    else:
        return jsonify("Failure: Magnet losses calculation was unsuccessful."), 500


@app.route("/apply_segmentation", methods=["POST"])
def magnets_segmentation():
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
def apply_skew():
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
