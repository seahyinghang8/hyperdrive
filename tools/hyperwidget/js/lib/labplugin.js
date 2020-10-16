var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'hyperwidget',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'hyperwidget',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

