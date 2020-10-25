import React, { useState } from 'react';

const FONT_SIZE_SCALE = 0.9

class OCRViz extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            lineIdx: []
        }
    }
    getLineClickHandler(chosen_idx) {
        const page = this.props.model.get('page')
        const lines = this.props.model.get('lines')
        const lineIdxs = this.props.model.get('line_idxs')
        return (e) => {
            if (e.shiftKey || e.ctrlKey || e.metaKey) {
                this.props.model.set(
                    'lines', lines.concat([page.lines[chosen_idx]]))
                this.props.model.set('line_idxs', lineIdxs.concat([chosen_idx]))
                this.setState({lineIdx: this.state.lineIdx.concat([chosen_idx])})
            } else {
                this.props.model.set('lines', [page.lines[chosen_idx]])
                this.props.model.set('line_idxs', [chosen_idx])
                this.setState({lineIdx: [chosen_idx]})
            }
            this.props.model.save_changes();
        }
    }
    render () {
        return (
            <div style={getParentStyle(this.props.model.get('page'))}>
                {
                    this.props.model.get('page').lines.map((line, index) => {
                        return (
                            <div onClick={ this.getLineClickHandler(index).bind(this) }
                                style={ getLineStyle(this.state.lineIdx.includes(index), line) }>
                                {line.text}
                            </div>
                        )
                    })
                }
            </div>
        )
    }
}

function getParentStyle(page) {
    return  {
        display: 'absolute',
        width: `${page.width}px`,
        height: `${page.height}px`,
        overflow: 'scroll'
    }
}

function getLineStyle(chosen, line) {
    let borderColor = 'black';
    if (chosen) {
        borderColor = 'red'
    }
    let font_size = Math.min(line.height, line.width / line.text.length) * FONT_SIZE_SCALE
    return {
        width: `${line.width}px`,
        height: `${line.height}px`,
        lineHeight: `${line.height}px`,
        position: 'absolute',
        left: `${line.left}px`,
        top: `${line.top}px`,
        border: "thin solid #000000",
        textAlign: "center",
        cursor: "pointer",
        fontSize: font_size,
        borderColor: borderColor
    }
}

export default OCRViz
