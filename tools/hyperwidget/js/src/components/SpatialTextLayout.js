import React from 'react'

import './SpatialTextLayout.css'

const FONT_SIZE_TO_PIXEL_WIDTH = 0.62
const FONT_SIZE_SCALE = 0.9

function SpatialTextLayout(props) {
    return (
        <div className='spatial-layout-container' style={getParentStyle(props.page, props.showImg, props.scale)}>
            {
                props.showLines && props.page.lines.map((line, idx) => {
                    const lineState = props.lineStates[props.lineStateArr[idx]]
                    const bgColor = lineState['backgroundColor']
                    const showTooltip = lineState['showTooltip']
                    const showText = lineState['showText']
                    const popover = lineState['popover']
                    const showPopover = popover !== undefined
                    let className = 'ocr-line'
                    if (showTooltip) className += ' hyper-tooltip'
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
                    }
                    return (
                        <div 
                            style={getLinePosStyle(line, props.scale)}
                            onClick={props.lineOnClick}
                            className={className}
                            key={idx}
                            line-index={idx}
                            data-hyper-tooltip={line.text}
                        >
                            <div
                                style={getLineTextStyle(line, props.scale, bgColor)}
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


function getParentStyle(page, showImg, scale) {
    const imgUrl = showImg ? `data:image/jpeg;base64, ${page.b64_image}` : ''
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

function getLineTextStyle(line, scale, color) {
    const fontHeight = line.height * FONT_SIZE_SCALE * scale
    const fontWidth = line.width * scale / line.text.length / FONT_SIZE_TO_PIXEL_WIDTH
    const fontSize = Math.min(fontHeight, fontWidth)
    return {
        width: line.width * scale,
        height: line.height * scale,
        lineHeight: `${line.height * scale}px`,
        fontSize: fontSize,
        backgroundColor: color,
    }
}

export default SpatialTextLayout
