hyperwidget
===============================

A Custom Jupyter Widget Library

Installation
------------

## To install use pip:

    $ pip install hyperwidget
    $ jupyter nbextension enable --py --sys-prefix hyperwidget

## Local Dev Installation for Classic Notebook

To develop this package against the classic notebook, run:

- `pip install -e .` (installs python package for development, runs `npm install` and `npm run build`)
- `jupyter nbextension install --py --symlink --sys-prefix <python_package_name>`\
(symlinks `static/` directory into `<jupyter path>/nbextensions/<extension_name>/`). Now the notebook has access to the frontend code.
- `jupyter nbextension enable --py --sys-prefix <python_package_name>`\
(copies `<npm_package_name>.json` into  `<environment path>/etc/jupyter/nbconfig/notebook.d/` directory). Now the notebook will load your frontend code on page load.

Now make some changes to your source code. Then:

- After making Python code changes, restarting the notebook kernel will be enough to reflect changes
- After making JavaScript code changes:
    - `cd js`
    - `npm run build`
    - Refresh browser to reflect changes

