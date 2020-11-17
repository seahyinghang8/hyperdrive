import ipywidgets as widgets
from traitlets import Dict, List, Instance, Unicode, Integer


# Frontend counterpart in js/src/widget.js
@widgets.register
class OCRVisualizer(widgets.DOMWidget):
    _model_name = Unicode('OCRVisualizerModel').tag(sync=True)
    _view_name = Unicode('OCRVisualizerView').tag(sync=True)
    _view_module = Unicode('hyperwidget').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module = Unicode('hyperwidget').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(
        '^{{ cookiecutter.npm_package_version }}'
    ).tag(sync=True)

    document = Dict().tag(sync=True)
    selected_lines = List([]).tag(sync=True)


@widgets.register
class ErrorTable(widgets.DOMWidget):
    _model_name = Unicode('ErrorTableModel').tag(sync=True)
    _view_name = Unicode('ErrorTableView').tag(sync=True)
    _view_module = Unicode('hyperwidget').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module = Unicode('hyperwidget').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(
        '^{{ cookiecutter.npm_package_version }}'
    ).tag(sync=True)

    errors = Dict().tag(sync=True)


@widgets.register
class ExtractionHeatmap(widgets.DOMWidget):
    _model_name = Unicode('ExtractionHeatmapModel').tag(sync=True)
    _view_name = Unicode('ExtractionHeatmapView').tag(sync=True)
    _view_module = Unicode('hyperwidget').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module = Unicode('hyperwidget').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)
    # Version of the front-end module containing widget model
    _model_module_version = Unicode(
        '^{{ cookiecutter.npm_package_version }}'
    ).tag(sync=True)

    documents = List().tag(sync=True)
    labels = List().tag(sync=True)
    extracted_fields = List().tag(sync=True)
