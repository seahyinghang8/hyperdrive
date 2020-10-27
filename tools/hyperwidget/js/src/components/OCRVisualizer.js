import React from 'react'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import ReactTooltip from 'react-tooltip'

import 'react-tabs/style/react-tabs.css'
import './OCRVisualizer.css'

const FONT_SIZE_SCALE = 0.9
const TAB_OFFSET = 44
const PAGE_KEY = 'page'
const LINE_IDX_KEY = 'line_idxs'


class OCRVisualizer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            LINE_IDX_KEY: this.props.model.get(LINE_IDX_KEY)
        }
    }

    componentDidMount () {
        ReactTooltip.rebuild();
    }

    getLineClickHandler(lineIdx) {
        return () => {
            var selectedLineIdxs = Array.from(this.state.LINE_IDX_KEY)
            const lineIdxIdx = selectedLineIdxs.indexOf(lineIdx)
            if (lineIdxIdx !== -1) {
                selectedLineIdxs.splice(lineIdxIdx, 1)
            } else {
                selectedLineIdxs.push(lineIdx)
            }
            this.props.model.set(LINE_IDX_KEY, Array.from(selectedLineIdxs))
            this.props.model.save_changes()
            this.setState({
                LINE_IDX_KEY: selectedLineIdxs
            })
        }
    }

    renderTab(showImg, showLines, showText) {
        ReactTooltip.rebuild();
        const selectedLineIdxs = this.state.LINE_IDX_KEY
        return (
            <div style={getParentStyle(this.props.model.get(PAGE_KEY), showImg)}>
                {
                    showLines && this.props.model.get(PAGE_KEY).lines.map((line, index) => {
                        return (
                            <div onClick={this.getLineClickHandler(index).bind(this)}
                                key={index}
                                data-tip={line.text}
                                data-for='preview'
                                className={`ocr-line ${selectedLineIdxs.includes(index) && 'ocr-line-selected'}`}
                                style={getLineStyle(line)}>
                                {showText && line.text}
                            </div>
                        )
                    })
                }
                <ReactTooltip id='preview'/>
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
                        {this.renderTab(false, true, true)}
                    </div>
                </TabPanel>
                <TabPanel>
                    <div>
                        {this.renderTab(true, false, false)}
                    </div>
                </TabPanel>
                <TabPanel>
                    <div>
                        {this.renderTab(true, true, false)}
                    </div>
                </TabPanel>
            </Tabs>
        )
        
    }
}

function getParentStyle(page, showImg) {
    let imgUrl = ""
    if (showImg) {
        imgUrl = `data:image/jpeg;base64, ${page.b64_image}`
    }
    return  {
        width: `${page.width}px`,
        height: `${page.height}px`,
        backgroundImage: `url("${imgUrl}")`
    }
}

function getLineStyle(line) {
    let font_size = Math.min(line.height, line.width / line.text.length) * FONT_SIZE_SCALE
    return {
        width: `${line.width}px`,
        height: `${line.height}px`,
        lineHeight: `${line.height}px`,
        left: `${line.left}px`,
        top: `${line.top + TAB_OFFSET}px`,
        fontSize: font_size,
    }
}

export default OCRVisualizer
