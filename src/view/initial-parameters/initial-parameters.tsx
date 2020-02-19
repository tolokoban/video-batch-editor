import React from "react"
import Tfw from 'tfw'

import MovieService from '../../service/movie'
import FileSystemService from '../../service/file-system'
import ErrorView from '../error'

import "./initial-parameters.css"

const Path = window.require('path')

const Button = Tfw.View.Button
const Flex = Tfw.Layout.Flex
const Icon = Tfw.View.Icon
const Input = Tfw.View.Input

const Storage = new Tfw.Storage.PrefixedLocalStorage("video-batch-editor")

interface IInitialParametersProps {
    className?: string,
    onProcess: (inputFiles: string[], outputFolder: string) => void
}
interface IInitialParametersState {
    inputFolder: string,
    outputFolder: string,
    ffmpegError: string,
    ffmpegVersion: string,
    errorInput: string,
    errorOutput: string,
    inputFiles: string[]
}

export default class InitialParameters extends React.Component<IInitialParametersProps, IInitialParametersState> {
    public state = {
        inputFolder: Storage.get('input-folder', '/home/petitjea/Videos/test'),
        outputFolder: Storage.get('output-folder', '/home/petitjea/Videos/test/out'),
        ffmpegError: '',
        ffmpegVersion: '',
        errorInput: 'Folder empty!',
        errorOutput: 'Folder empty!',
        inputFiles: []
    }

    async componentDidMount() {
        try {
            await this.checkFolders()
            const version = await MovieService.getVersion()
            this.setState({
                ffmpegVersion: `v${version.major}.${version.minor}.${version.patch}`
            })
        } catch (ex) {
            this.setState({ ffmpegError: `${ex}` })
        }
    }

    private checkFolders = async () => {
        const { inputFolder, outputFolder } = this.state
        let errorInput = ''
        let errorOutput = ''

        this.setState({ inputFiles: [] })
        try {
            if (inputFolder.trim().length === 0) {
                errorInput = 'Folder empty!'
            }
            else if (!FileSystemService.exists(inputFolder)) {
                errorInput = 'Folder not found!'
            }
            else if (!(await FileSystemService.isDir(inputFolder))) {
                errorInput = 'This is not a folder!'
            }
            else {
                Storage.set('input-folder', inputFolder)
                const files = await FileSystemService.listFiles(inputFolder)
                this.setState({ inputFiles: files })
            }
        } catch (ex) {
            errorInput = `${ex}`
        }

        try {
            if (outputFolder.trim().length === 0) {
                errorOutput = 'Folder empty!'
            }
            else if (!FileSystemService.exists(outputFolder)) {
                errorOutput = 'Folder not found!'
            }
            else if (!(await FileSystemService.isDir(outputFolder))) {
                errorOutput = 'This is not a folder!'
            }
            else {
                Storage.set('output-folder', outputFolder)
            }
        } catch (ex) {
            errorOutput = `${ex}`
        }

        this.setState({ errorInput, errorOutput })
    }

    private handleInputFolderChange = (inputFolder: string) => {
        this.setState({ inputFolder }, this.checkFolders)
    }

    private handleOutputFolderChange = (outputFolder: string) => {
        this.setState({ outputFolder }, this.checkFolders)
    }

    private handleProcess = async () => {
        const { inputFolder, inputFiles, outputFolder } = this.state
        this.props.onProcess(
            inputFiles.map(name => Path.join(inputFolder, name)),
            outputFolder
        )
    }

    render() {
        const classes = [
            'view-InitialParameters',
            'thm-bg1',
            Tfw.Converter.String(this.props.className, "")
        ]
        const {
            inputFolder, outputFolder,
            ffmpegError, ffmpegVersion,
            errorInput, errorOutput,
            inputFiles
        } = this.state

        return (<div className={classes.join(' ')}>
            <header className="thm-bgPD">
                Batch compositor
            </header>
            <section>
                <Input
                    label="Source folder"
                    value={inputFolder}
                    wide={true}
                    onChange={this.handleInputFolderChange} />
                {
                    inputFiles.length === 0 &&
                    <div className="error thm-fgSD">{errorInput}</div>
                }
                {
                    inputFiles.length > 0 &&
                    <div className="hint">{`Number of files: ${inputFiles.length}`}</div>
                }
                <Input
                    label="Destination folder"
                    value={outputFolder}
                    wide={true}
                    onChange={this.handleOutputFolderChange} />
                <div className="error thm-fgSD">{errorOutput}</div>
            </section>
            <footer className="thm-bg2">
                <Button
                    label="Process"
                    icon="play"
                    enabled={!errorInput && !errorOutput && inputFiles.length > 0}
                    onClick={this.handleProcess} />
                {
                    ffmpegError &&
                    <ErrorView content={ffmpegError} />
                }
                {
                    ffmpegVersion &&
                    <div className="faded">FFMPEG <b>{ffmpegVersion}</b> is available</div>
                }
                {
                    !ffmpegError && !ffmpegVersion &&
                    <Flex justifyContent="space-between" className="faded" wide={false}>
                        <Icon content="wait" animate={true} />
                        <div>Checking FFMPEG...</div>
                    </Flex>
                }
            </footer>
        </div>)
    }
}
