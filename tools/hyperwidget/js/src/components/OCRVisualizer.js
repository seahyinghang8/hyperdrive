import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './OCRVisualizer.css'

const PAGE_KEY = 'page'
const LINE_IDX_KEY = 'line_idxs'


class OCRVisualizer extends React.Component {
    constructor(props) {
        super(props)
        const selectedLineIdxs = Array.from(this.props.model.get(LINE_IDX_KEY))
        const lineStateArr = this.props.model.get(PAGE_KEY).lines.map((l, idx) => (
            selectedLineIdxs.includes(idx) ? 1 : 0
        ))

        this.lineStates = {
            0: {
                'backgroundColor': 'rgba(0, 0, 0, 0.1)',
                'showTooltip': true,
                'showText': true
            },
            1: {
                'backgroundColor': 'rgba(0, 255, 113, 0.5)',
                'showTooltip': true,
                'showText': true
            },
        }
        
        this.state = {
            lineStateArr: lineStateArr,
            activeTab: 0,
            scale: 0
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
        // if line state between 0 and 1
        const lineIdx = Number(evt.target.getAttribute('line-index'))
        let selectedLineIdxs = Array.from(this.props.model.get(LINE_IDX_KEY))
        if (this.state.lineStateArr[lineIdx] == 1) {
            const lineIdxIdx = selectedLineIdxs.indexOf(lineIdx)
            selectedLineIdxs.splice(lineIdxIdx, 1)
        } else {
            selectedLineIdxs.push(lineIdx)
        }
        this.props.model.set(LINE_IDX_KEY, selectedLineIdxs)
        this.props.model.save_changes()
        this.setState((state) => {
            let prevLineState = state.lineStateArr
            prevLineState[lineIdx] = prevLineState[lineIdx] == 1 ? 0 : 1
            return {lineStateArr: prevLineState}
        })
    }

    renderTab(showImg, showLines, showText) {
        const page = this.props.model.get(PAGE_KEY)
        if (showText) {
            this.lineStates[0]['showText'] = true
            this.lineStates[1]['showText'] = true
        } else {
            this.lineStates[0]['showText'] = false
            this.lineStates[1]['showText'] = false
        }

        console.log(this.lineStates)
        return (<SpatialTextLayout
            page={page}
            lineStateArr={this.state.lineStateArr}
            lineStates={this.lineStates}
            lineOnClick={evt => {this.lineClickHandler(evt)}}
            showImg={showImg}
            showLines={showLines}
            scale={this.state.scale}
        />)
    }

    render() {
        const tabTitle = ["OCR", "Image", "OCR + Image"]
        const tabDivArgs = [
            [false, true, true],
            [true, false, false],
            [true, true, false]
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
                    this.renderTab(...tabDivArgs[this.state.activeTab])
                }
            </div>
        )
    }
}

export default OCRVisualizer
