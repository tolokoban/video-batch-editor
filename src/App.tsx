import React from 'react'
import Tfw from 'tfw'

import InitialParameters from './view/initial-parameters'
import ProcessAll from './view/process-all'

import './App.css'

Tfw.Theme.register("default", {
    bg0: '#bcd',
    bg3: '#fff',
    bgP: '#0f71b7'
})
Tfw.Theme.apply("default")


interface IState {
    page: string,
    inputFiles: string[],
    outputFolder: string
}

class App extends React.Component<{}, IState> {
    state = { page: "params", inputFiles: [], outputFolder: '' }

    private handleProcess = (inputFiles: string[], outputFolder: string) => {
        this.setState({ page: "process", inputFiles, outputFolder })
        /*
        for (const file of inputFiles) {
            const info = await MovieService.getInfo(file)
            console.info("info=", file, info);
            const outputFile = Path.join(outputFolder, "snapshot.png")
            await MovieService.extractFrameToPNG(
                path, outputFile, 1
            )
            */
    }

    render() {
        const { page, inputFiles, outputFolder } = this.state

        return (
            <div className="App thm-bg0">
                <Tfw.Layout.Stack value={page}>
                    <InitialParameters key="params" onProcess={this.handleProcess} />
                    <ProcessAll
                        key="process"
                        width={800} height={600}
                        inputFiles={inputFiles}
                        outputFolder={outputFolder} />
                </Tfw.Layout.Stack>
            </div>
        );
    }
}

export default App
