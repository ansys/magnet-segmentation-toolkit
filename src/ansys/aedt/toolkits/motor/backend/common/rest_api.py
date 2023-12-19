from flask import Flask
from flask import jsonify
from flask import request

from ansys.aedt.toolkits.motor.backend.api import Toolkit
from ansys.aedt.toolkits.motor.backend.common.logger_handler import logger

service = Toolkit()
settings = service.get_properties()

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def get_health():
    logger.info("[GET] /health (check if the server is healthy).")
    _, msg = service.aedt_connected()
    return jsonify(msg), 200


@app.route("/status", methods=["GET"])
def get_status():
    raise Exception("get status")
    logger.info("[GET] /status (check if the thread is running).")
    exit_code, msg = service.get_thread_status()
    if exit_code <= 0:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/properties", methods=["GET"])
def get_properties():
    app.logger.info("[GET] /properties (get toolkit properties).")
    return jsonify(service.get_properties()), 200


@app.route("/properties", methods=["PUT"])
def set_properties():
    app.logger.info("[PUT] /properties (set toolkit properties).")
    body = request.json
    success, msg = service.set_properties(body)
    if success:
        return jsonify(msg), 200
    else:
        return jsonify(msg), 500


@app.route("/installed_versions", methods=["GET"])
def installed_aedt_version():
    logger.info("[GET] /installed_versions (get the installed versions).")
    return jsonify(service.installed_aedt_version()), 200


@app.route("/aedt_sessions", methods=["GET"])
def aedt_sessions():
    logger.info("[GET] /aedt_sessions (AEDT sessions for a specific version).")
    response = service.aedt_sessions()
    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500


@app.route("/launch_aedt", methods=["POST"])
def launch_aedt():
    logger.info("[POST] /launch_aedt (launch or connect AEDT).")
    response = service.launch_aedt()
    if response:
        return jsonify("AEDT session launched."), 200
    else:
        return jsonify("AEDT session fail to launch."), 500


@app.route("/close_aedt", methods=["POST"])
def close_aedt():
    logger.info("[POST] /close_aedt (close AEDT).")

    body = request.json
    aedt_keys = ["close_projects", "close_on_exit"]
    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify(msg), 500
    elif not isinstance(body, dict) or not all(item in body for item in set(aedt_keys)):
        msg = "Body is not correct."
        logger.error(msg)
        return jsonify(msg), 500

    close_projects = body["close_projects"]
    close_on_exit = body["close_on_exit"]
    response = service.release_aedt(close_projects, close_on_exit)

    if response:
        return jsonify("AEDT correctly released."), 200
    else:
        return jsonify("AEDT is not connected."), 500


@app.route("/connect_design", methods=["POST"])
def connect_design():
    logger.info("[POST] /connect_design (connect or create a design).")
    body = request.json
    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify("Body is empty."), 500

    response = service.connect_design(body["aedtapp"])
    if response:
        return jsonify("Design is connected"), 200
    else:
        return jsonify("Failed to connect to design."), 500


@app.route("/save_project", methods=["POST"])
def save_project():
    logger.info("[POST] /save_project (save AEDT project).")
    body = request.json
    if not body:
        msg = "Body is empty."
        logger.error(msg)
        return jsonify("body is empty."), 500

    response = service.save_project(body)
    if response:
        return jsonify("Project saved: {}".format(body)), 200
    else:
        return jsonify(response), 500


@app.route("/design_names", methods=["GET"])
def get_design_names():
    logger.info("[GET] /design_names (AEDT designs for a specific project).")

    response = service.get_design_names()

    if isinstance(response, list):
        return jsonify(response), 200
    else:
        return jsonify(response), 500
