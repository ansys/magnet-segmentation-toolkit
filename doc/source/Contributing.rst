.. _contributing_aedt:

==========
Contribute
==========
Overall guidance on contributing to a PyAnsys repository appears in
`Contributing <https://dev.docs.pyansys.com/how-to/contributing.html>`_
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyAEDT or its toolkits.
 
The following contribution information is specific to PyMotorCAD-PyAEDT toolkit.

Clone the repository
--------------------
To clone and install the latest version of PyMotorCAD-PyAEDT toolkit in
development mode, run:

.. code::

    git clone https://github.com/pyansys/pymotorcad-pyaedt-toolkit.git
    cd pymotorcad-pyaedt-toolkit
    python -m pip install --upgrade pip
    pip install -e .

Post issues
-----------
Use the `PyMotorCAD-PyAEDT toolkit Issues <https://github.com/ansys/pymotorcad-pyaedt-toolkit/issues>`_ page
to submit questions, report bugs, and request new features.

View toolkit documentation
--------------------------
Documentation for the latest development version, which tracks the
``main`` branch, is hosted at  `PyMotorCAD-PyAEDT toolkit Documentation <>`_.
This version is automatically kept up to date via GitHub actions.

Adhere to code style
--------------------
PyMotorCAD-PyAEDT toolkit is compliant with `PyAnsys code style
<https://dev.docs.pyansys.com/coding-style/index.html>`_. It uses the tool
`pre-commit <https://pre-commit.com/>`_ to select the code style. You can install
and activate this tool with:

.. code:: bash

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook with:

.. code:: bash

  pre-commit install

This way, it's not possible for you to push code that fails the style checks.
For example::

  $ pre-commit install
  $ git commit -am "Add my cool feature."
  black....................................................................Passed
  isort (python)...........................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  fix requirements.txt.....................................................Passed
  blacken-docs.............................................................Passed

Maximum line length
~~~~~~~~~~~~~~~~~~~
Best practice is to keep the length at or below 120 characters for code
and comments. Lines longer than this might not display properly on some terminals
and tools or might be difficult to follow.
