import React from 'react'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import SpatialTextLayout from './SpatialTextLayout'

import 'react-tabs/style/react-tabs.css'
import './OCRVisualizer.css'

const PAGE_KEY = 'page'
const LINE_IDX_KEY = 'line_idxs'


class OCRVisualizer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            LINE_IDX_KEY: this.props.model.get(LINE_IDX_KEY)
        }
    }

    lineClickHandler(evt) {
        var selectedLineIdxs = this.state.LINE_IDX_KEY
        const lineIdx = Number(evt.target.getAttribute('line-index'))
        // toggle element to be selected
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

    renderTab(showImg, showLines, hideText = false) {
        const selectedLineIdxs = this.state.LINE_IDX_KEY
        const page = this.props.model.get(PAGE_KEY)
        return (<SpatialTextLayout
            page={page}
            lineOnClick={evt => {this.lineClickHandler(evt)}}
            showImg={showImg}
            showLines={showLines}
            hideText={hideText}
            selectedLineIdxs={selectedLineIdxs}
        />)
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
                        {this.renderTab(true, true, true)}
                    </div>
                </TabPanel>
            </Tabs>
        )
    }
}

export default OCRVisualizer
