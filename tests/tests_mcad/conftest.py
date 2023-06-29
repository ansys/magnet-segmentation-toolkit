import os
import os.path
import shutil
import tempfile

from RPC_test_common import get_dir_path
from RPC_test_common import get_temp_files_dir_path
import ansys.motorcad.core as pymotorcad
from pyaedt.generic.filesystem import Scratch


class BasisTest(object):
    def my_setup(self):
        scratch_path = tempfile.gettempdir()
        self.local_scratch = Scratch(scratch_path)
        self.mcadapp = None

    def my_teardown(self):
        if self.mcadapp:
            self.mcadapp.quit()
        shutil.rmtree(self.local_scratch.path, ignore_errors=True)

    def add_app(self):
        self.mcadapp = pymotorcad.MotorCAD()
        # Disable messages if opened with UI
        self.mcadapp.set_variable("MessageDisplayState", 2)

        # Disable messages if opened with UI
        self.mcadapp.set_variable("MessageDisplayState", 2)

        return self.mcadapp

    def reset_to_default_file(self):
        self.mcadapp.load_from_file(os.path.dirname(get_dir_path()) + r"\input_data\e9_built.mot")

        # save to temp location to avoid editing base file
        self.mcadapp.save_to_file(get_temp_files_dir_path() + r"\temp_e9_built.mot")

    def reset_temp_file_folder(self):
        dir_path = get_temp_files_dir_path()

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        os.mkdir(dir_path)
