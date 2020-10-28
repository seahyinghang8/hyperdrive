import React from 'react'
import SpatialTextLayout from './SpatialTextLayout'

import './ExtractionHeatmap.css'

const PAGE_KEY = 'page'
const FIELD_NAME_KEY = 'field_name'
const 


class ExtractionHeatmap extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
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

    // renderTab(showImg, showLines, hideText = false) {
    //     const page = this.props.model.get(PAGE_KEY)

    //     return (<SpatialTextLayout
    //         page={page}
    //         lineStateArr={this.state.lineStateArr}
    //         lineStates={LINE_STATES}
    //         lineOnClick={evt => {this.lineClickHandler(evt)}}
    //         showImg={showImg}
    //         showLines={showLines}
    //         hideText={hideText}
    //         scale={this.state.scale}
    //     />)
    // }

    render() {
        const field_name = this.props.model.get()
        const expected = this.props.model.get()
        return (
            <div ref={el => (this.container = el)}>
                <p>
                    Field Name: {field_name} \t
                    Expected Ouptput: {expected}
                </p>
            </div>
        )
    }
}

export default ExtractionHeatmap
