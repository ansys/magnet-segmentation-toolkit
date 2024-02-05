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

from functools import wraps
import threading
import time
from typing import List

from ansys.aedt.toolkits.magnet_segmentation.backend.common.logger_handler import logger
from ansys.aedt.toolkits.magnet_segmentation.backend.models import properties


class ThreadManager(object):
    """Class to control toolkit threads."""

    toolkit_thread_name = "Toolkit_Thread"

    def __init__(self):
        pass

    @classmethod
    def process_exe(cls, process, *args):
        """Execute process."""
        try:
            # Set the variable at process start
            properties.is_toolkit_busy = True

            # Start
            process(*args)

            # Waits for the thread closure
            time.sleep(0.5)

            # Set the variable at process end
            properties.is_toolkit_busy = False
        except Exception as e:
            print(f"An error occurred: {e}")

    @classmethod
    def launch_thread(cls, process):
        """Launch process."""

        @wraps(process)
        def inner_function(*args):
            if not properties.is_toolkit_busy:
                # Multithreading fails with COM
                logger.debug("Starting thread: {}".format(cls.toolkit_thread_name))
                properties.is_toolkit_busy = True
                running_thread = threading.Thread(
                    target=cls.process_exe,
                    name=cls.toolkit_thread_name,
                    args=(
                        process,
                        *args,
                    ),
                    daemon=True,
                )
                running_thread.start()
                return True
            else:
                return False

        return inner_function

    @staticmethod
    def running_threads() -> List[threading.Thread]:
        """List the running threads."""
        threads_list = [thread for thread in threading.enumerate() if type(thread) == threading.Thread]
        return threads_list

    @classmethod
    def is_toolkit_thread_running(cls) -> bool:
        """Check if the thread associated to the toolkit is running."""
        running_threads_names = [t.name for t in cls.running_threads()]
        return cls.toolkit_thread_name in running_threads_names
