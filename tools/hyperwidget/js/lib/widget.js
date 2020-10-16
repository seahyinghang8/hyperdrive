var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');

const FONT_SIZE_SCALE = 0.9

var HyperModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HyperModel',
        _view_name : 'HyperView',
        _model_module : 'hyperwidget',
        _view_module : 'hyperwidget',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0'
    })
});


// Custom View. Renders the widget model.
var HyperView = widgets.DOMWidgetView.extend({
    // Render the view.
    render: function() {
        const page = this.model.get('page');
        let parent = document.createElement('div');
        parent.style.display = 'absolute';
        parent.style.width = page.width +"px";
        parent.style.height = page.height + "px";
        parent.style.overflow = "scroll";
        this.line_divs = []
        for (var i = 0; i < page.lines.length; i++) {
            let line_div = document.createElement('div');
            let line = page.lines[i]
            line_div.innerText = line.text;
            this.applyInitialStyle(line_div, line)
            line_div.onclick = this.getOnclick(i).bind(this);
            parent.appendChild(line_div);
            this.line_divs.push(line_div)
        }
        this.el.appendChild(parent)
    },
    applyInitialStyle: function (line_div, line) {
        line_div.style.width = line.width +"px";
        line_div.style.height = line.height + "px";
        line_div.style.lineHeight = line.height + "px";
        line_div.style.position = 'absolute';
        line_div.style.left = line.left + "px";
        line_div.style.top = line.top + "px";
        line_div.style.border = "thin solid #000000";
        line_div.style.textAlign = "center";
        line_div.style.cursor = "pointer"
        let font_size = Math.min(line.height, line.width / line.text.length) * FONT_SIZE_SCALE
        line_div.style.fontSize = font_size;
    },
    getOnclick: function (i) {
        function clickHandler (e) {
            let page = this.model.get('page')
            let lines = this.model.get('lines')
            let line_idxs = this.model.get('line_idxs')
            this.line_divs[i].style.borderColor = "red";
            if (e.shiftKey || e.ctrlKey || e.metaKey) {
                this.model.set(
                    'lines', lines.concat([page.lines[i]]));
                this.model.set('line_idxs', line_idxs.concat([i]));
            } else {
                for (const b_idx of line_idxs) {
                    this.line_divs[b_idx].style.borderColor = "black"
                }
                this.model.set('lines', [page.lines[i]]);
                this.model.set('line_idxs', [i]);
            }
            this.model.save_changes();
        }
        return clickHandler.bind(this);
    }
});


module.exports = {
    HyperModel: HyperModel,
    HyperView: HyperView
};
