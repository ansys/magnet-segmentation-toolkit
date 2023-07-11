import os
from pathlib import Path
import shutil

from pyaedt import generate_unique_folder_name

src_folder = os.path.join(Path(__file__).parents[1], "input_data")
temp_folder = shutil.copytree(src_folder, os.path.join(generate_unique_folder_name(), "input_data"))