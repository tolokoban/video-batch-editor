import React from "react"
import Tfw from 'tfw'

import "./error.css"

const Touchable = Tfw.View.Touchable

interface IErrorProps {
    className?: string,
    content: string
}

export default class Error extends React.Component<IErrorProps, {}> {
    private handleClick = () => {
        Tfw.Factory.Dialog.error(this.props.content)
    }

    render() {
        const classes = [
            'view-Error', 'thm-bgSD',
            Tfw.Converter.String(this.props.className, "")
        ]

        return (<Touchable className={classes.join(' ')}
                           title={this.props.content}
                           onClick={this.handleClick}>
            <div>{ this.props.content }</div>
        </Touchable>)
    }
}
