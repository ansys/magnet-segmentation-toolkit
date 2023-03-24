import os.path
import shutil

from pyaedt.generic.DataHandlers import json_to_dict


class CommonSettings:
    """Provides common reusable methods."""

    def __init__(self, working_dir):
        """Init."""
        self.working_dir = working_dir
        self.configuration_dict = None

    def load_json(self, json_file_path):
        """Convert a json file to a dictionary."""
        return json_to_dict(json_file_path)

    def copy_json_settings(self):
        """Copy json files folder from site-packages to working directory."""
        conf_folder = os.path.join(os.path.dirname(__file__), "configuration_settings")
        settings_path = os.path.join(self.working_dir, "configuration_settings")
        if not os.path.exists(settings_path):
            shutil.copytree(conf_folder, settings_path)
        self.configuration_dict = self.load_json(
            os.path.join(settings_path, "configuration_settings.json")
        )
        return settings_path
