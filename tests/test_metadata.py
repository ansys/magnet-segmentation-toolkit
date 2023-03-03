from ansys.pymotorcad_pyaedt_toolkit.pymotorcad_pyaedt_toolkit import __version__


def test_pkg_version():
    assert __version__ == "0.1.dev0"
