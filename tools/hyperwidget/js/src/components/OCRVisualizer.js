import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './OCRVisualizer.css'

const PAGE_KEY = 'page'
const LINE_IDX_KEY = 'line_idxs'


class OCRVisualizer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            LINE_IDX_KEY: this.props.model.get(LINE_IDX_KEY),
            activeTab: 0,
            scale: 1
        }
    }

    componentDidMount() {
        // ugly hack
        const page = this.props.model.get(PAGE_KEY)
        setTimeout(
            () => {
                this.setState({
                    scale: (this.container.offsetWidth - 30) / Number(page.width)
                })
            }, 10)
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
            scale={this.state.scale}
        />)
    }

    render() {
        const tabTitle = ["OCR", "Image", "OCR + Image"]
        const tabDiv = [
            this.renderTab(false, true),
            this.renderTab(true, false),
            this.renderTab(true, true, true)
        ]

        return (
            <div ref={el => (this.container = el)}>
                <ul class="tab">
                    { tabTitle.map((title, idx) => (
                        <li class={`tab-item ${idx === this.state.activeTab ? 'active' : ''}`}
                            key={title + idx}>
                            <a href="#" onClick={() => {
                                this.setState({activeTab: idx})
                            }}>{title}</a>
                        </li>
                    ))}
                </ul>
                {
                    this.state.scale > 0. &&
                    tabDiv[this.state.activeTab]
                }
            </div>
        )
    }
}

export default OCRVisualizer
