/**
 * To create a movie from images:
 * ffmpeg -i %04d.jpg -c:v libvpx -qmin 0 -qmax 50 -crf 10 -vf fps=30 input.webm
 */

import FileSystemService from './file-system'

const ChildProcess = window.require('child_process')

export default {
    extractFrameToPNG,
    getVersion,
    getInfo
}

export interface IVersion {
    major: number,
    minor: number,
    patch: number
}

interface IStreamInfo {
    id: number,
    codec_name: string,
    codec_long_name: string,
    profile: string,
    codec_type: string,
    codec_time_base: string,
    codec_tag_string: string,
    codec_tag: string,
    width: number,
    height: number,
    coded_width: number,
    coded_height: number,
    has_b_frames: number,
    start_time: string,
    duration: string,
    nb_frames: string
}

export interface IMovieInfo {
    streams: IStreamInfo[],
    format: {
        filename: string,
        nb_streams: number,
        nb_programs: number,
        format_name: string,
        format_long_name: string,
        start_time: string,
        duration: string,
        size: string,
        bit_rate: string,
        probe_score: number,
        tags: { [key: string]: string }
    }
}

const RX_VERSION = /ffmpeg version ([0-9]+)\.([0-9]+)\.([0-9]+)/ig

/**
 * Check the FFMPEG version and returns it if possible.
 * Otherwise, throw an exception.
 */
async function getVersion(): Promise<IVersion> {
    const stdout = await ffmpeg("-version")
    const matcher = RX_VERSION.exec(stdout)
    if (!matcher) throw stdout

    return {
        major: Number(matcher[1].trim()),
        minor: Number(matcher[2].trim()),
        patch: Number(matcher[3].trim())
    }
}


async function getInfo(path: string): Promise<IMovieInfo> {
    const textInfo = await ffprobe(
        `-v quiet -print_format json -show_format -show_streams -print_format json "${path}"`)
    return JSON.parse(textInfo)
}


async function extractFrameToPNG(inputFile: string,
                                 outputFile: string,
                                 positionInSeconds: number) {
    if (FileSystemService.exists(outputFile)) {
        console.warn("This file already exists! We will overwrite it.", outputFile)
        await FileSystemService.deleteFile(outputFile)
    }
    await ffmpeg(
        `-ss ${positionInSeconds} -i "${inputFile}" -c:v png -frames:v 1 "${outputFile}"`
    )
}


/**
 * Execute FFMPEG with some args and return the stdout content.
 */
async function ffmpeg(args: string = ""): Promise<string> {
    return new Promise((resolve, reject) => {
        ChildProcess.exec(`ffmpeg ${args}`, (error: string, stdout: string) => {
            if (error) {
                console.error(`ChildProcess.exec error: ${error}`);
                reject(error)
                return;
            }
            resolve(`${stdout}`)
        })
    })
}

/**
 * Execute FFPROBE with some args and return the stdout content.
 */
async function ffprobe(args: string = ""): Promise<string> {
    return new Promise((resolve, reject) => {
        ChildProcess.exec(`ffprobe ${args}`, (error: string, stdout: string) => {
            if (error) {
                console.error(`ChildProcess.exec error: ${error}`);
                reject(error)
                return;
            }
            resolve(`${stdout}`)
        })
    })
}
