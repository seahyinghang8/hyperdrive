import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './OCRVisualizer.css'

class OCRVisualizer extends React.Component {
    constructor(props) {
        super(props)
        this.page1 = this.props.document.pages[0]
        this.image1 = this.props.document.images[0]
        const lineStateArr = this.page1.lines.map((l, idx) => (
            props.selectedLines.includes(idx) ? 1 : 0
        ))

        this.lineStates = {
            0: {
                'style': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.1)'
                },
                'showTooltip': true,
                'showText': true,
                'showStats': true
            },
            1: {
                'style': {
                    'backgroundColor': 'rgba(115, 146, 245, 0.5)'
                },
                'showTooltip': true,
                'showText': true,
                'showStats': true
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
        setTimeout(
            () => {
                this.setState({
                    scale: (this.container.offsetWidth - 30) / Number(this.page1.width)
                })
            }, 10)
    }           

    lineClickHandler(evt) {
        const lineIdx = Number(evt.target.getAttribute('line-index'))
        let selectedLines = this.props.selectedLines
        if (this.state.lineStateArr[lineIdx] == 1) {
            const lineIdxIdx = selectedLines.indexOf(lineIdx)
            selectedLines.splice(lineIdxIdx, 1)
        } else {
            selectedLines.push(lineIdx)
        }
        this.props.setSelectedLines(selectedLines)
        this.setState((state) => {
            let prevLineState = state.lineStateArr
            prevLineState[lineIdx] = prevLineState[lineIdx] == 1 ? 0 : 1
            return {lineStateArr: prevLineState}
        })
    }

    renderTab(showImg, showLines, showText) {
        if (showText) {
            this.lineStates[0]['showText'] = true
            this.lineStates[1]['showText'] = true
            this.lineStates[0]['showStats'] = true
            this.lineStates[1]['showStats'] = true
        } else {
            this.lineStates[0]['showText'] = false
            this.lineStates[1]['showText'] = false
            this.lineStates[0]['showStats'] = false
            this.lineStates[1]['showStats'] = false
        }

        return (<SpatialTextLayout
            page={this.page1}
            image={this.image1}
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
