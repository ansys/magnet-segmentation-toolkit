import shutil
import tempfile

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
