"""Utils module"""

import requests


def download_file(url, local_filename):
    """Download a file from an URL inti a local file."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=4096):
                f.write(chunk)
    return local_filename
