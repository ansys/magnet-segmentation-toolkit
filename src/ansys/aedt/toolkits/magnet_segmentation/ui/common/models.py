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

"""Data classes used to store data related to UI settings.
"""

import json
import os

from pydantic import BaseModel

from ansys.aedt.toolkits.magnet_segmentation.backend.models import Properties


class UIProperties(BaseModel, validate_assignment=True):
    """Store properties useful for UI."""

    backend_url: str = "127.0.0.1"
    backend_port: int = 5001
    debug: bool = True
    log_file: str = "motor_frontend.log"


general_kwargs = {}
if os.path.expanduser(os.path.join(os.path.dirname(__file__), "general_properties.json")):
    with open(os.path.join(os.path.dirname(__file__), "general_properties.json")) as file_handler:
        general_kwargs = json.load(file_handler)

general_settings = UIProperties(**general_kwargs)

be_properties = Properties()
