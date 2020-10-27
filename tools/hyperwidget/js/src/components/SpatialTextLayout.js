import React from 'react'
import ReactTooltip from 'react-tooltip'

import './SpatialTextLayout.css'

const FONT_SIZE_SCALE = 0.9
const TAB_OFFSET = 44


function SpatialTextLayout(props) {
    ReactTooltip.rebuild();
    const selectedLineIdxs = props.selectedLineIdxs
    return (
        <div style={getParentStyle(props.page, props.showImg)}>
            {
                props.showLines && props.page.lines.map((line, index) => {
                    return (
                        <div onClick={props.lineOnClick}
                            key={index}
                            line-index={index}
                            data-tip={line.text}
                            data-for='preview'
                            className={`ocr-line ${selectedLineIdxs.includes(index) && 'ocr-line-selected'}`}
                            style={getLineStyle(line)}>
                            {!props.hideText && line.text}
                        </div>
                    )
                })
            }
            <ReactTooltip id='preview'/>
        </div>
    )
}


function getParentStyle(page, showImg) {
    let imgUrl = ""
    if (showImg) {
        imgUrl = `data:image/jpeg;base64, ${page.b64_image}`
    }
    return  {
        width: `${page.width}px`,
        height: `${page.height}px`,
        backgroundImage: `url("${imgUrl}")`
    }
}


function getLineStyle(line) {
    let font_size = Math.min(line.height, line.width / line.text.length) * FONT_SIZE_SCALE
    return {
        width: `${line.width}px`,
        height: `${line.height}px`,
        lineHeight: `${line.height}px`,
        left: `${line.left}px`,
        top: `${line.top + TAB_OFFSET}px`,
        fontSize: font_size,
    }
}

export default SpatialTextLayout
