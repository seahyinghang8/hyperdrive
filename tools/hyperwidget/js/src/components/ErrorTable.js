import React from 'react'

import './ErrorTable.css'


function ErrorTable(props) {
    const headers = ['Field', 'Doc Index', 'Actual Output', 'Expected']
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
                { Object.keys(props.errors).map(error_key => (
                    props.errors[error_key].map(row => (
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
