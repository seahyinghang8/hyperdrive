import React from 'react'

import './ErrorTable.css'

const ERROR_KEY = 'errors'


function ErrorTable(props) {
    const headers = ['Field', 'Doc Index', 'Actual Output', 'Expected']
    const error_dict = props.model.get(ERROR_KEY)
    return (
        <table className='table table-striped table-hover'>
            <thead>
                <tr>
                    { headers.map(header => (
                        <th key={header}>{header}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                { Object.keys(error_dict).map(error_key => (
                    error_dict[error_key].map(row => (
                        <tr key={Array.from(row).join('')}>
                            <td key={error_key}>{error_key}</td>
                            { row.map(data => (
                                <td key={data}>{data}</td>
                            ))}
                        </tr>
                    ))
                ))}
            </tbody>
        </table>
    )
}

export default ErrorTable
