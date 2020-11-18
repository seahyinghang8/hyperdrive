import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './ExtractionHeatmap.css'


class ExtractionHeatmap extends React.Component {
    constructor(props) {
        super(props)

        // Set starting state to the 0th index of all inputs
        const startDocIndex = 0
        const startFieldNames = Object.keys(props.extractedFields[startDocIndex])
        const startField = startFieldNames[0]
        const startWeights = props.extractedFields[startDocIndex][startField][0]['weights']
        let selectedWeights = {}
        Object.keys(startWeights).map(keyname => {
            selectedWeights[keyname] = true
        })

        this.state = {
            docIndex: startDocIndex,
            fieldName: startField,
            selectedWeights: selectedWeights,
            windowWidth: 0,
            selectedLines: []
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
                    const startWeights = this.props.extractedFields[evt.target.value][this.state.fieldName][0]['weights']
                    let selectedWeights = {}
                    Object.keys(startWeights).map(keyname => {
                        selectedWeights[keyname] = true
                    })
                    this.setState({
                        docIndex: evt.target.value,
                        selectedWeights: selectedWeights
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

    renderExpectedValue() {
        const docLabels = this.props.labels[this.state.docIndex]
        const expected = docLabels[this.state.fieldName]

        return (
            <div class="hyper-input-group">
                <span class="hyper-input-group-addon">Expected</span>
                <input class="form-input" type="text" value={expected} />
            </div>
        )
    }

    renderWeightSelect() {
        const weightsName = Object.keys(this.state.selectedWeights)

        return (
            <div className='columns' style={{marginTop: 10}}>
                { weightsName.map((name, i) => {
                    const checked = this.state.selectedWeights[name]
                    const setChecked = () => {
                        this.setState(oldState => {
                            let newWeightsSelected = deepcopy(oldState.selectedWeights)
                            newWeightsSelected[name] = !newWeightsSelected[name]
                            return {
                                selectedWeights: newWeightsSelected
                            }
                        })
                    }
                    return (
                        <div className='column col-3' key={name} >
                            <div class="form-group">
                                <label class="form-switch">
                                    <input type="checkbox" onChange={setChecked} checked={checked}/>
                                    <i class={`form-icon color-${i % 4}`}></i>{name} weight
                                </label>
                            </div>
                        </div>
                    )
                })}
            </div>
        )
    }

    renderHeatmap() {
        const page = this.props.documents[this.state.docIndex].pages[0]
        const image = this.props.documents[this.state.docIndex].images[0]
        let scale = (this.state.windowWidth - 30) / Number(page.width)

        const extractedDict = this.props.extractedFields[this.state.docIndex]
        const extractedArr = extractedDict[this.state.fieldName]
        const lineScores = extractedArr.map(ef => ({
            index: ef.index,
            computedTotal: computeTotal(ef.scores, ef.weights, this.state.selectedWeights),
            scoreWidth: computeScoreWidth(ef.scores, ef.weights, this.state.selectedWeights),
            text: lineDictToLine(ef.line).text,
        }))

        lineScores.sort((a, b) => b.computedTotal - a.computedTotal)
        let lineScoresRanked = {}

        lineScores.map((lineScore, i) => {
            lineScore.rank = i + 1
            lineScoresRanked[lineScore.index] = lineScore
        })
        const maxScore = lineScores[0].computedTotal
        const minScore = lineScores[lineScores.length - 1].computedTotal
        const scoreDiff = maxScore - minScore

        let lineStates = {
            'base': {
                'style': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.15)'
                },
                'showTooltip': true,
            },
            'baseExpected': {
                'style': {
                    'backgroundColor': 'rgba(0, 0, 0, 0.15)',
                    'outline': '#066d10 dashed 3px'
                },
                'showTooltip': true,
            },
        }

        const docLabels = this.props.labels[this.state.docIndex]
        const expected = docLabels[this.state.fieldName]

        const lineStateArr = page.lines.map((line_dict, idx) => {
            const line = lineDictToLine(line_dict)
            const lineScore = lineScoresRanked[idx]
            if (lineScore !== undefined) {
                const green = (maxScore - lineScore.computedTotal) / scoreDiff * 255
                const newState = idx
                const isSelected = this.state.selectedLines.includes(idx)
                let style = {
                    'backgroundColor': `rgba(255, ${green}, 0, 0.4)`
                }
                if (line.text.includes(expected)) style['outline'] = '#066d10 dashed 3px'
                if (isSelected) style['border'] = '2px solid rgba(115, 146, 245, 0.9)'

                lineStates[newState] = {
                    'style': style,
                    'showTooltip': false,
                    'popoverLock': isSelected,
                    'popover': (
                        <div className='card ocr-card'>
                            <div className='card-body'>
                                { scoreBreakdown(lineScore.scoreWidth) }
                                <label class='form-label' style={{marginBottom: 0, paddingBottom: 0}}>
                                    Total Score: {(lineScore.computedTotal * 100).toFixed(2)} &emsp; Rank: {lineScore.rank}
                                    <br />
                                    Text: {lineScore.text}
                                </label>
                            </div>
                        </div>
                    )
                }
                return newState
            } else if (l.text.includes(expected)) {
                return 'baseExpected'
            } else {
                return 'base'
            }
        })

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
            let selectedLines = prevState.selectedLines
            const lineIdxIdx = selectedLines.indexOf(lineIdx)
            if (lineIdxIdx != -1) selectedLines.splice(lineIdxIdx, 1)
            else selectedLines.push(lineIdx)
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
                    <div className='column col-4'>
                        { this.renderFieldSelect() }
                    </div>
                    <div className='column col-5'>
                        { this.renderExpectedValue() }
                    </div>
                </div>
                { this.renderWeightSelect() }
                { this.renderHeatmap() }
            </div>
        )
    }
}

function lineDictToLine(line_dict) {
    const words = line_dict['words']
    const text = words.map(w => w.text).join(' ')
    const left = Math.min(...words.map(w => w.left))
    const top = Math.min(...words.map(w => w.top))
    const right = Math.max(...words.map(w => w.left + w.width))
    const bottom = Math.max(...words.map(w => w.top + w.height))
    return {
        'text': text,
        'left': left,
        'top': top,
        'width': right - left,
        'height': bottom - top
    }
}

function scoreBreakdown(scoreWidth) {
    const scoreKeys = Object.keys(scoreWidth)
    return (
        <div className='bar'>
            { scoreKeys.map((key, i) => (
                <div 
                    key={key}
                    className={`bar-item hyper-tooltip color-${i % 4}`}
                    style={{width: `${scoreWidth[key]}%`}}
                    data-hyper-tooltip={key}
                >
                    {scoreWidth[key]}
                </div>
            ))}
        </div>
    )
}

function deepcopy(obj) {
    return JSON.parse(JSON.stringify(obj))
}

function computeScoreWidth(scores, weights, selectedWeights) {
    let scoreWidth = {}
    for (const [key, score] of Object.entries(scores)) {
        scoreWidth[key] = (selectedWeights[key]) ? Math.round(score * weights[key] * 100) : 0
    }
    return scoreWidth
}

function computeTotal(scores, weights, selectedWeights) {
    let sum = 0
    for (const [key, score] of Object.entries(scores)) {
        if (selectedWeights[key]) sum += score * weights[key] 
    }
    return sum
}

export default ExtractionHeatmap
