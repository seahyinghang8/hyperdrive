import React, { useState } from 'react'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import 'react-tabs/style/react-tabs.css';

import ReactTooltip from 'react-tooltip';

const FONT_SIZE_SCALE = 0.9
const TAB_OFFSET = 44

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
    componentDidMount () {
        ReactTooltip.rebuild();
    }
    renderTab(showImg, showLines) {
        ReactTooltip.rebuild();
        return (
            <div style={getParentStyle(this.props.model.get('page'), showImg)}>
                {
                    showLines && this.props.model.get('page').lines.map((line, index) => {
                        return (
                            <div onClick={ this.getLineClickHandler(index).bind(this) }
                                data-tip={line.text}
                                data-for="preview"
                                style={ getLineStyle(this.state.lineIdx.includes(index), line) }>
                                {line.text}
                            </div>
                        )
                    })
                }
                <ReactTooltip id="preview"/>
            </div>
        )
    }
    render () {
        return (
            <Tabs>
                <TabList>
                    <Tab>OCR</Tab>
                    <Tab>Image</Tab>
                    <Tab>OCR + Image</Tab>
                </TabList>

                <TabPanel>
                    <div>
                        {this.renderTab(false, true)}
                    </div>
                </TabPanel>
                <TabPanel>
                    <div>
                        {this.renderTab(true, false)}
                    </div>
                </TabPanel>
                <TabPanel>
                    <div>
                        {this.renderTab(true, true)}
                    </div>
                </TabPanel>
            </Tabs>
        )
        
    }
}

function getParentStyle(page, showImg) {
    let imgUrl = ""
    if (showImg) {
        imgUrl = `data:image/jpeg;base64, ${page.image}`
    }
    return  {
        width: `${page.width}px`,
        height: `${page.height}px`,
        overflow: 'scroll',
        backgroundImage: `url("${imgUrl}")`
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
        top: `${line.top + TAB_OFFSET}px`,
        border: "thin solid #000000",
        textAlign: "center",
        cursor: "pointer",
        fontSize: font_size,
        borderColor: borderColor
    }
}

export default OCRViz
