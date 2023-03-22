from pyaedt.generic.DataHandlers import json_to_dict


class CommonSettings:
    """Provides common reusable methods."""

    def load_json(self, json_file_path):
        """Convert a json file to a dictionary."""
        return json_to_dict(json_file_path)
