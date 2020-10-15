import ipywidgets as widgets
from traitlets import Dict, List, Instance, Unicode, Integer

# See js/lib/example.js for the frontend counterpart to this file.

@widgets.register
class HyperWidget(widgets.DOMWidget):
    _view_name = Unicode('HyperView').tag(sync=True)
    _view_module = Unicode('hyper_widget').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)
    
    page = Dict().tag(sync=True)
    lines = List().tag(sync=True)
    line_idxs = List([0]).tag(sync=True)
