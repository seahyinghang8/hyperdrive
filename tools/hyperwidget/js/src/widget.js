import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base'
import _ from 'lodash';

import OCRVisualizer from './components/OCRVisualizer';


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
    // Render the view.
    render() {
        ReactDOM.render(
            React.createElement(
                OCRVisualizer, { model: this.model }),
            this.el,
        )
    }
}
