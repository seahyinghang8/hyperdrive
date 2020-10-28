import React from 'react'

import './SpatialTextLayout.css'

const FONT_SIZE_TO_PIXEL_WIDTH = 0.62
const FONT_SIZE_SCALE = 0.9

function SpatialTextLayout(props) {
    return (
        <div className='spatial-layout-container' style={getParentStyle(props.page, props.showImg, props.scale)}>
            {
                props.showLines && props.page.lines.map((line, idx) => {
                    const bgColor = props.lineStates[props.lineStateArr[idx]]['backgroundColor']
                    const className = `${props.showTooltip ? 'hyper-tooltip' : ''} ocr-line`
                    return (
                        <div 
                            onClick={props.lineOnClick}
                            key={idx}
                            line-index={idx}
                            data-hyper-tooltip={line.text}
                            className={className}
                            style={getLineStyle(line, props.scale, bgColor)}
                        >
                            {!props.hideText && line.text}
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
        width: `${page.width * scale}px`,
        height: `${page.height * scale}px`,
        backgroundImage: `url("${imgUrl}")`,
    }
}


function getLineStyle(line, scale, color) {
    const font_height = line.height * FONT_SIZE_SCALE * scale
    const font_width = line.width * scale / line.text.length / FONT_SIZE_TO_PIXEL_WIDTH
    let font_size = Math.min(
        font_height,
        font_width
    )

    return {
        width: `${line.width * scale}px`,
        height: `${line.height * scale}px`,
        lineHeight: `${line.height * scale}px`,
        left: `${line.left * scale}px`,
        top: `${line.top * scale}px`,
        fontSize: font_size,
        backgroundColor: color,
    }
}

export default SpatialTextLayout
