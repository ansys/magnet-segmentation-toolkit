import datetime
import os
import tempfile


def get_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_temp_files_dir_path():
    test_folder = "unit_test" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    scratch_path = os.path.join(tempfile.gettempdir(), test_folder)
    if not os.path.exists(scratch_path):
        try:
            os.makedirs(scratch_path)
        except:
            pass
    return scratch_path


def almost_equal(a, b, decimal_places=1):
    # Rough check
    return round(a - b, decimal_places) == 0


def almost_equal_fixed(a, b, allowed_difference=0):
    return abs(a - b) < +allowed_difference
