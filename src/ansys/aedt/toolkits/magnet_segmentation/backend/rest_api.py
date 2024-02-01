# from flask import request

from ansys.aedt.toolkits.magnet_segmentation.backend.api import Toolkit
from ansys.aedt.toolkits.magnet_segmentation.backend.common.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.magnet_segmentation.backend.common.rest_api import app
from ansys.aedt.toolkits.magnet_segmentation.backend.common.rest_api import jsonify
from ansys.aedt.toolkits.magnet_segmentation.backend.common.rest_api import logger
from ansys.aedt.toolkits.magnet_segmentation.backend.common.rest_api import settings

service = Toolkit()
# Toolkit entrypoints


@app.route("/project_materials", methods=["GET"])
def get_materials():
    logger.info("[GET] /Get project materials.")

    response = service._get_project_materials()
    if response:
        return response
    else:
        return jsonify("Get project material was unsuccessful."), 500


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
