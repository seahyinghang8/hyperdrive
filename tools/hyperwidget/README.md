hyperwidget
===============================

A Custom Jupyter Widget Library

Installation
------------

To install use pip:

    $ pip install hyperwidget
    $ jupyter nbextension enable --py --sys-prefix hyperwidget

To install for jupyterlab

    $ jupyter labextension install hyperwidget

For a development installation (requires npm),

    $ git clone https://github.com//hyperwidget.git
    $ cd hyperwidget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix hyperwidget
    $ jupyter nbextension enable --py --sys-prefix hyperwidget
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

