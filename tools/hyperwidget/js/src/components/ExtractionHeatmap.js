import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './ExtractionHeatmap.css'
import { update } from 'lodash'

const COLOR_LIST = [
    '#093145',
    '#829356',
    '#C2571A',
    '#9A2617',
]


class ExtractionHeatmap extends React.Component {
    constructor(props) {
        super(props)
        this.pages = this.props.model.get('pages')
        this.labels = this.props.model.get('labels')
        this.extractedFields = this.props.model.get('extracted_fields')

        // Set starting state to the 0th index of all inputs
        const startIndex = 0
        const startFieldNames = Object.keys(this.extractedFields[startIndex])
        const startField = startFieldNames[0]
        const startWeights = deepcopy(this.extractedFields[startIndex][startField][0]['weights'])

        this.state = {
            docIndex: startIndex,
            fieldName: startField,
            weights: startWeights,
            inputError: false,
            windowWidth: 0,
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
        const numDocs = this.pages.length
        
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
        const fieldNames = Object.keys(this.extractedFields[this.state.docIndex])

        return (
            <div class="hyper-input-group">
                <span class="hyper-input-group-addon">Field Name</span>
                <select class="form-select" 
                value={this.state.fieldName}
                onChange={(evt => {
                    const weights = deepcopy(this.extractedFields[this.state.docIndex][evt.target.value][0]['weights'])
                    this.setState({
                        fieldName: evt.target.value,
                        weights: weights,
                        inputError: false,
                    })
                })}>
                    { fieldNames.map(name => (
                        <option key={name} value={name}>{name}</option>
                    ))}
                </select>
            </div>
        )
    }

    renderExpectedValue() {
        const docLabels = this.labels[this.state.docIndex]
        const expected = docLabels[this.state.fieldName]

        return (
            <div class="hyper-input-group">
                <span class="hyper-input-group-addon">Expected</span>
                <input class="form-input" type="text" value={expected} />
            </div>
        )
    }

    renderWeightAdjuster() {
        const weightKeys = Object.keys(this.state.weights)
        const hasError = this.state.weightsError

        return (
            <div className='columns' style={{marginTop: 10}}>
                { weightKeys.map((key) => {
                    const weightPercent = (this.state.weights[key] * 100).toFixed(0)
                    const onChangeWeight = (evt) => {
                        let errorState = false
                        let weight = Number(evt.target.value) / 100
                        if (isNaN(weight)) {
                            errorState = true
                            weight = 0
                        }
                        // validate weight adds up to 1
                        let weightSum = 0
                        for (const k of weightKeys) {
                            const currWeight = (k == key) ? weight : this.state.weights[k]
                            weightSum += currWeight
                            if (currWeight < 0) errorState = true
                        }
                        if (weightSum > 1) errorState = true
                        // update weights and error state
                        this.setState((prevState) => {
                            let updatedWeights = prevState.weights
                            updatedWeights[key] = weight
                            return {
                                weights: updatedWeights,
                                weightsError: errorState
                            }
                        })
                    }
                    return (
                        <div className='column col-3' key={key}>
                            <div className={`hyper-input-group ${ hasError ? 'has-error' : ''}`}>
                                <span class="hyper-input-group-addon">{key}</span>
                                <input
                                    class="form-input"
                                    type="number"
                                    value={weightPercent}
                                    onChange={onChangeWeight}
                                />
                            </div>
                        </div>
                    )
                })}
                { hasError && (
                    <div style={{color: 'red', marginLeft: 10}}>Sum of weights is greater than 100</div>
                )}
            </div>
        )
    }

    renderHeatmap() {
        const page = this.pages[this.state.docIndex]
        const scale = (this.state.windowWidth - 30) / Number(page.width)

        const extractedDict = this.extractedFields[this.state.docIndex]
        const extractedArr = extractedDict[this.state.fieldName]
        let extractedLinesScores = {}
        let minScore = 10
        let maxScore = 0
        extractedArr.map((ef) => {
            const totalScore = computeTotal(ef.scores, this.state.weights)
            extractedLinesScores[ef.index] = {
                total: totalScore,
                text: ef.line.text,
                scores: ef.scores,
                weights: this.state.weights
            }
            minScore = Math.min(totalScore, minScore)
            maxScore = Math.max(totalScore, maxScore)
        })
        const scoreDiff = maxScore - minScore

        let lineStates = {
            'base': {
                'backgroundColor': 'rgba(0, 0, 0, 0.15)',
                'showTooltip': true,
            }
        }
        let lineStateArr = page.lines.map((l, idx) => {
            const lineScore = extractedLinesScores[idx]
            if (lineScore !== undefined) {
                const green = (maxScore - lineScore.total) / scoreDiff * 255
                const newState = idx

                lineStates[newState] = {
                    'backgroundColor': `rgba(255, ${green}, 0, 0.4)`,
                    'showTooltip': true,
                    'popover': (
                        <div className='card ocr-card'>
                            <div className='card-body'>
                                <div className='form-group'>
                                    { scoreBreakdown(lineScore.scores, lineScore.weights) }
                                    <label class='form-label'>Total Score: {(lineScore.total * 100).toFixed(2)}</label>
                                </div>
                            </div>
                        </div>
                    )
                }
                return newState
            } else {
                return 'base'
            }
        })

        return (<SpatialTextLayout
            page={page}
            showImg={true}
            showLines={true}
            lineStateArr={lineStateArr}
            lineStates={lineStates}
            scale={scale}
        />)
    }

    render() {
        return (
            <div ref={el => (this.container = el)}>
                <div className='columns' style={{marginTop: 30}}>
                    <div className='column col-3'>
                        { this.renderDocSelect() }
                    </div>
                    <div className='column col-4'>
                        { this.renderFieldSelect() }
                    </div>
                    <div className='column col-5'>
                        { this.renderExpectedValue() }
                    </div>
                </div>
                { this.renderWeightAdjuster() }
                <div style={{marginTop: 20}}>
                    { this.renderHeatmap() }
                </div>
            </div>
        )
    }
}

function scoreBreakdown(rawScores, weights) {
    const scoreKeys = Object.keys(rawScores)
    return (
        <div>
            <div className='bar'>
                { scoreKeys.map((key, i) => {
                    const rscore = rawScores[key]
                    const weight = weights[key]
                    const score = (rscore * weight * 100).toFixed(0)
                    const bgColor = COLOR_LIST[i % COLOR_LIST.length]
                    return (
                        <div 
                            key={key}
                            className='bar-item hyper-tooltip'
                            style={{
                                width: `${score}%`,
                                backgroundColor: bgColor
                            }}
                            data-hyper-tooltip={key}
                        >
                            {score}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

function deepcopy(obj) {
    return JSON.parse(JSON.stringify(obj))
}

function computeTotal(scores, weights) {
    let sum = 0
    for (const [key, score] of Object.entries(scores)) {
        sum += score * weights[key]
    }
    return sum
}

export default ExtractionHeatmap
