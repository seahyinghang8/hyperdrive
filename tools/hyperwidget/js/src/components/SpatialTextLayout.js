import React from 'react'

import './SpatialTextLayout.css'

const FONT_SIZE_TO_PIXEL_WIDTH = 0.62
const FONT_SIZE_SCALE = 0.9

function SpatialTextLayout(props) {
    return (
        <div className='spatial-layout-container' style={getParentStyle(props.page, props.image, props.showImg, props.scale)}>
            {
                props.showLines && props.page.lines.map((line_dict, idx) => {
                    const line = lineDictToLine(line_dict)
                    const lineState = props.lineStates[props.lineStateArr[idx]]
                    const lineStyle = lineState['style']
                    const showTooltip = lineState['showTooltip']
                    const showText = lineState['showText']
                    const popover = lineState['popover']
                    const showPopover = popover !== undefined
                    let className = 'ocr-line'
                    let tooltipText = ''
                    if (showTooltip) {
                        className += ' hyper-tooltip'
                        const showStats = lineState['showStats']
                        if (showStats)
                            tooltipText = ` left:${line.left + line.width / 2} | top:${line.top + line.height / 2}`
                        else
                            tooltipText = line.text
                    }
                    if (showPopover) {
                        className += ' hyper-popover'
                        const xNorm = (line.left + line.width / 2) / props.page.width
                        if (xNorm < 0.2) {
                            className += ' hyper-popover-right'
                        } else if (xNorm > 0.8) {
                            className += ' hyper-popover-left'
                        } else {
                            className += ' hyper-popover-top'
                        }
                        if (lineState['popoverLock']) {
                            className += ' lock'
                        }
                    }

                    return (
                        <div 
                            style={getLinePosStyle(line, props.scale)}
                            onClick={props.lineOnClick}
                            className={className}
                            key={idx}
                            line-index={idx}
                            data-hyper-tooltip={tooltipText}
                        >
                            <div
                                style={getLineTextStyle(line, props.scale, lineStyle)}
                                line-index={idx}
                            >
                                { showText && line.text }
                            </div>
                            { showPopover && (
                                <div className='hyper-popover-container'>
                                    {popover}
                                </div>
                            )}
                        </div>
                    )
                })
            }
        </div>
    )
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

function getParentStyle(page, image, showImg, scale) {
    const imgUrl = showImg ? `data:image/jpeg;base64, ${image}` : ''
    return  {
        width: page.width * scale,
        height: page.height * scale,
        backgroundImage: `url("${imgUrl}")`,
    }
}

function getLinePosStyle(line, scale) {
    return {
        left: line.left * scale,
        top: line.top * scale,
    }
}

function getLineTextStyle(line, scale, lineStyle) {
    const style = deepcopy(lineStyle)
    const fontHeight = line.height * FONT_SIZE_SCALE * scale
    const fontWidth = line.width * scale / line.text.length / FONT_SIZE_TO_PIXEL_WIDTH
    style['fontSize'] = Math.min(fontHeight, fontWidth)
    style['width'] = line.width * scale
    style['height'] = line.height * scale
    style['lineHeight'] =  `${line.height * scale}px`
    return style
}

function deepcopy(obj) {
    return JSON.parse(JSON.stringify(obj))
}

export default SpatialTextLayout
