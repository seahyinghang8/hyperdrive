import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base'
import _ from 'lodash';

import OCRVisualizer from './components/OCRVisualizer'
import ErrorTable from './components/ErrorTable'
import ExtractionHeatmap from './components/ExtractionHeatmap'

import './widget.css'


export class OCRVisualizerModel extends DOMWidgetModel {
    defaults () {
        return {
            ...super.defaults(),
            _model_name : 'OCRVisualizerModel',
            _view_name : 'OCRVisualizerView',
            _model_module : 'hyperwidget',
            _view_module : 'hyperwidget',
            _model_module_version : '0.1.0',
            _view_module_version : '0.1.0'
        }    
    }
}


export class OCRVisualizerView extends DOMWidgetView {
    render() {
        ReactDOM.render(
            React.createElement(
                OCRVisualizer, { model: this.model }),
            this.el,
        )
    }
}


export class ErrorTableModel extends DOMWidgetModel {
    defaults () {
        return {
            ...super.defaults(),
            _model_name : 'ErrorTableModel',
            _view_name : 'ErrorTableView',
            _model_module : 'hyperwidget',
            _view_module : 'hyperwidget',
            _model_module_version : '0.1.0',
            _view_module_version : '0.1.0'
        }    
    }
}


export class ErrorTableView extends DOMWidgetView {
    render() {
        ReactDOM.render(
            React.createElement(
                ErrorTable, { model: this.model }),
            this.el,
        )
    }
}


export class ExtractionHeatmapModel extends DOMWidgetModel {
    defaults () {
        return {
            ...super.defaults(),
            _model_name : 'ExtractionHeatmapModel',
            _view_name : 'ExtractionHeatmapView',
            _model_module : 'hyperwidget',
            _view_module : 'hyperwidget',
            _model_module_version : '0.1.0',
            _view_module_version : '0.1.0'
        }    
    }
}


export class ExtractionHeatmapView extends DOMWidgetView {
    render() {
        ReactDOM.render(
            React.createElement(
                ExtractionHeatmap, { model: this.model }),
            this.el,
        )
    }
}
