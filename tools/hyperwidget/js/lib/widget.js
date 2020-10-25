import { DOMWidgetView, DOMWidgetModel } from '@jupyter-widgets/base';
import _ from 'lodash';
import OCRViz from './OCRViz';
export class HyperModel extends DOMWidgetModel {
  defaults() {
    return { ...super.defaults(),
      _model_name: 'HyperModel',
      _view_name: 'HyperView',
      _model_module: 'hyperwidget',
      _view_module: 'hyperwidget',
      _model_module_version: '0.1.0',
      _view_module_version: '0.1.0'
    };
  }

} // Custom View. Renders the widget model.

export class HyperView extends DOMWidgetView {
  // Render the view.
  render() {
    ReactDOM.render(React.createElement(OCRViz, {
      model: this.model
    }), this.el);
  }

}