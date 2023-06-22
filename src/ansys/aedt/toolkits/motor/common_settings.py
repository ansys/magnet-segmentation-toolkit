import os.path
import shutil

from pyaedt.generic.DataHandlers import json_to_dict


class CommonSettings:
    """Provide common reusable methods.

    Parameters
    ----------
    working_dir : str
        Path to working directory.
    """

    def __init__(self, working_dir):
        self.working_dir = working_dir
        self.config_settings_path = os.path.join(self.working_dir, "configuration_settings")
        if not os.path.exists(self.config_settings_path):
            shutil.copytree(
                os.path.join(os.path.dirname(__file__), "configuration_settings"),
                self.config_settings_path,
            )

    def load_json(self, json_file_path):
        """Convert a json file into a dictionary.

        Parameters
        ----------
        json_file_path : str
            Path to json file to convert into a dictionary.
        """
        return json_to_dict(json_file_path)

    def update_dict_props(self, dictionary, key, value, remove=False):
        """Remove or add dictionary properties.

        Parameters
        ----------
        dictionary : dict
            Dictionary to update.
        key : str
            Dictionary key to point to in order to update its value.
        value : str
            Value in dictionary to update.
        remove : bool, optional
            Whether to remove or add a new value in a specific dictionary key.
            Default value is ``False``.
        """
        try:
            if key not in dictionary.keys():
                raise ValueError("Provided key doesn't exist.")
            if remove:
                dictionary[key].remove(value)
            elif isinstance(dictionary[key], list):
                dictionary[key].append(value)
        except ValueError as e:
            return False
