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

import sys

# isort: off

from ansys.aedt.toolkits.magnet_segmentation.backend.api import ToolkitBackend

from ansys.aedt.toolkits.common.backend.multithreading_server import MultithreadingServer
from ansys.aedt.toolkits.common.backend.rest_api import app
from ansys.aedt.toolkits.common.backend.rest_api import jsonify
from ansys.aedt.toolkits.common.backend.rest_api import logger

# from flask import request

# isort: on

toolkit_api = ToolkitBackend()

if len(sys.argv) == 3:
    toolkit_api.properties.url = sys.argv[1]
    toolkit_api.properties.port = int(sys.argv[2])


# ToolkitBackend entrypoints


@app.route("/project_materials", methods=["GET"])
def get_materials():
    logger.info("[GET] /Get project materials.")

    response = toolkit_api._get_project_materials()
    if response:
        return response
    else:
        return jsonify("Get project material was unsuccessful."), 500


@app.route("/design_setups", methods=["GET"])
def get_design_setups():
    logger.info("[GET] /Get design setups.")

    response = toolkit_api._get_design_setup_names()
    if response:
        return response
    else:
        return jsonify("Get design setups was unsuccessful."), 500


@app.route("/apply_segmentation", methods=["POST"])
def magnets_segmentation():
    logger.info("[POST] /Apply magnets segmentation.")

    response = toolkit_api.segmentation()
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

    response = toolkit_api.apply_skew()
    if response:
        return (
            jsonify("Skew angle applied successfully."),
            200,
        )
    else:
        return jsonify("Failure: Skew angle application was unsuccessful."), 500


@app.route("/validate_analyze", methods=["POST"])
def analyze_model():
    logger.info("[POST] /Validate and analyze AEDT model.")

    response = toolkit_api.validate_and_analyze()
    if response:
        return jsonify("AEDT model analyzed successfully."), 200
    else:
        return jsonify("Failure: AEDT model analysis was unsuccessful."), 500


@app.route("/magnet_loss", methods=["GET"])
def get_magnet_loss():
    logger.info("[GET] /Get magnet loss.")

    response = toolkit_api.get_magnet_loss()
    if response:
        return jsonify(f"Magnet Loss (avg)[W] = {response}"), 200
    else:
        return jsonify("Failure: Magnet loss calculation was unsuccessful."), 500


def run_backend(port=0):
    """Run the server."""
    app.debug = toolkit_api.properties.debug
    server = MultithreadingServer()
    if port == 0:
        port = toolkit_api.properties.port
    server.run(host=toolkit_api.properties.url, port=port, app=app)


if __name__ == "__main__":
    run_backend()
