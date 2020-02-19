import React from "react"
import Tfw from 'tfw'

import Calc from '../../tool/calc'
import FileSystemService from '../../service/file-system'
import MovieService from '../../service/movie'

import "./process-all.css"

import OverlayURL from './overlay.png'

const FPS = 30

interface IProcessAllProps {
    className?: string,
    inputFiles: string[],
    outputFolder: string,
    width: number,
    height: number
}
interface IProcessAllState {
    progress: number
}

export default class ProcessAll extends React.Component<IProcessAllProps, IProcessAllState> {
    public state = {
        progress: 0
    }
    private readonly refCanvas: React.RefObject<HTMLCanvasElement> = React.createRef()
    private readonly refContainer: React.RefObject<HTMLDivElement> = React.createRef()
    private readonly overlay = new Image()

    async componentDidMount() {
        this.resize()
        window.addEventListener("resize", this.resize)

        await this.loadOverlay()

        for (const inputFile of this.props.inputFiles) {
            const info = await MovieService.getInfo(inputFile)
            const start = Number(info.format.start_time)
            const duration = Number(info.format.duration)
            await this.process(inputFile, start, duration)
        }
    }

    async loadOverlay() {
        return new Promise(resolve => {
            this.overlay.onload = resolve
            this.overlay.src = OverlayURL
        })
    }

    async process(inputFile: string, start: number, duration: number) {
        const canvas = this.refCanvas.current
        if (!canvas) return
        const ctx = canvas.getContext("2d")
        if (!ctx) return

        let time = start
        let frameIndex = 0
        while (time < start + duration) {
            const progress = (time - start) / duration
            this.setState({ progress })
            await this.processFrame(ctx, inputFile, time, progress)
            await this.saveFrame(canvas, frameIndex)
            time += 1 / FPS
            frameIndex++
        }
    }

    async saveFrame(canvas: HTMLCanvasElement, frameIndex: number) {
        const { outputFolder } = this.props
        const dataURL = canvas.toDataURL("image/jpeg", 90)
        const commaPosition = dataURL.indexOf(',')
        const base64 = dataURL.substr(commaPosition + 1)
        const data = atob(base64)
        const len = data.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = data.charCodeAt(i);
        }
        const filename = FileSystemService.join(outputFolder, `${pad(frameIndex)}.jpg`)
        await FileSystemService.save(filename, bytes)
    }

    /**
     * @param  ctx
     * @param  inputFile
     * @param  time      - In seconds.
     * @param  progress  - Between 0 and 1.
     */
    async processFrame(ctx: CanvasRenderingContext2D,
        inputFile: string,
        time: number,
        progress: number) {
        const { width, height, outputFolder } = this.props

        const frameFilename = FileSystemService.join(outputFolder, "tmp.png")
        await MovieService.extractFrameToPNG(
            inputFile, frameFilename, time
        )
        const frame = await FileSystemService.createImageFromFile(frameFilename)
        const transform = Calc.resizeToContain(
            frame.width, frame.height,
            width, height
        )
        ctx.clearRect(0, 0, width, height)
        ctx.drawImage(
            frame,
            transform.translateX,
            transform.translateY,
            frame.width * transform.scale,
            frame.height * transform.scale
        )
        ctx.drawImage(this.overlay, 0, 0)
        ctx.drawImage(
            frame,
            frame.width / 2 - 80,
            frame.height / 2 - 60,
            160, 120,
            600, 40,
            160, 120
        )
    }


    componentWillUnmount() {
        window.removeEventListener("resize", this.resize)
    }

    private resize = Tfw.Throttler(() => {
        const container = this.refContainer.current
        if (!container) return
        const canvas = this.refCanvas.current
        if (!canvas) return

        const { width, height } = this.props
        const rect = container.getBoundingClientRect()
        const transform = Calc.resizeToContain(
            width, height,
            rect.width - 32,
            rect.height - 32
        )
        canvas.style.width = `${transform.scale * width}px`
        canvas.style.height = `${transform.scale * height}px`
    }, 300)

    render() {
        const { width, height } = this.props
        const { progress } = this.state

        const classes = [
            'view-ProcessAll',
            'thm-bg1',
            Tfw.Converter.String(this.props.className, "")
        ]

        return (<div className={classes.join(' ')}>
            <header className='thm-bgPD'>Processing... {`${(progress * 100).toFixed(1)} %`}</header>
            <div ref={this.refContainer}>
                <canvas className="thm-ele-nav"
                    ref={this.refCanvas}
                    width={width} height={height}></canvas>
            </div>
        </div>)
    }
}


function pad(value: number, size: number = 6): string {
    let txt = `${value}`
    while (txt.length < size) txt = `0${txt}`
    return txt
}
