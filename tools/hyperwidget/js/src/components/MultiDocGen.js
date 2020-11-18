import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './ExtractionHeatmap.css'


class MultiDocGen extends React.Component {
    constructor(props) {
        super(props)

        // Set starting state to the 0th index of all inputs
        const startDocIndex = 0
        this.state = {
            docIndex: startDocIndex,
            fieldName: "",
            windowWidth: 0,
            selectedLines: {}
        }
    }

    componentDidMount() {
        // ugly hack
        if (this.state.windowWidth == 0) {
            setTimeout(
                () => {
                    this.setState({
                        windowWidth: this.container.offsetWidth
                    })
                }, 10)
        }
    }           

    renderDocSelect() {
        const numDocs = this.props.documents.length
        
        return (
            <div class="hyper-input-group">
                <span class="hyper-input-group-addon">Doc Index</span>
                <select class="form-select" onChange={evt => {
                    this.setState({
                        docIndex: evt.target.value
                    })
                }}>
                    { [...Array(numDocs).keys()].map(idx => (
                        <option key={idx} value={idx}>{idx}</option>
                    ))}
                </select>
            </div>
        )
    } 

    renderFieldSelect() {
        const fieldNames = Object.keys(this.props.extractedFields[this.state.docIndex])

        return (
            <div class="hyper-input-group">
                <span class="hyper-input-group-addon">Field Name</span>
                <select class="form-select" 
                value={this.state.fieldName}
                onChange={(evt => {
                    const startWeights = this.props.extractedFields[this.state.docIndex][evt.target.value][0]['weights']
                    let selectedWeights = {}
                    Object.keys(startWeights).map(keyname => {
                        selectedWeights[keyname] = true
                    })
                    this.setState({
                        fieldName: evt.target.value,
                        selectedWeights: selectedWeights
                    })
                })}>
                    { fieldNames.map(name => (
                        <option key={name} value={name}>{name}</option>
                    ))}
                </select>
            </div>
        )
    }

    renderOcrSelector() {
        const page = this.props.documents[this.state.docIndex].pages[0]
        const image = this.props.documents[this.state.docIndex].images[0]
        let scale = (this.state.windowWidth - 30) / Number(page.width)
        if (scale > 1) scale = 1

        const lineStateArr = page.lines.map((l, idx) => {
            let doclines = this.state.selectedLines[this.state.docIndex]
            return (
                doclines && doclines.includes(idx) ? 1 : 0
            )
        })
        let lineStates = {
            0: {
                'style': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.1)'
                },
                'showTooltip': true,
                'showText': false
            },
            1: {
                'style': {
                    'backgroundColor': 'rgba(115, 146, 245, 0.5)'
                },
                'showTooltip': true,
                'showText': false
            },
        }

        return (<SpatialTextLayout
            page={page}
            image={image}
            showImg={true}
            showLines={true}
            lineOnClick={evt => {this.lineClickHandler(evt)}}
            lineStateArr={lineStateArr}
            lineStates={lineStates}
            scale={scale}
        />)
    }

    lineClickHandler(evt) {
        const lineIdx = Number(evt.target.getAttribute('line-index'))
        this.setState(prevState => {
            let selectedLines = deepcopy(prevState.selectedLines)
            let docLines = selectedLines[this.state.docIndex]
            if (!docLines) {
                selectedLines[this.state.docIndex] = []
            } 
            const lineIdxIdx = selectedLines[this.state.docIndex].indexOf(lineIdx)
            if (lineIdxIdx != -1) selectedLines[this.state.docIndex].splice(lineIdxIdx, 1)
            else selectedLines[this.state.docIndex].push(lineIdx)
            this.props.setSelectedLines(selectedLines)
            return {
                'selectedLines': selectedLines
            }
        })
    }

    render() {
        return (
            <div ref={el => (this.container = el)}>
                <div className='columns' style={{marginTop: 30}}>
                    <div className='column col-3'>
                        { this.renderDocSelect() }
                    </div>
                </div>
                { this.renderOcrSelector() }
            </div>
        )
    }
}

function deepcopy(obj) {
    return JSON.parse(JSON.stringify(obj))
}

export default MultiDocGen