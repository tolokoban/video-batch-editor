import Tfw from 'tfw'
import { ITask } from './types'

export default class Task {
    private readonly data: ITask

    constructor(content: string) {
        try {
            const data = Tfw.PermissiveJSON.parse(content)
            if (!data) throw "Data is null or undefined!"
            if (!data.output) throw "Mising attribute 'output'!"
            if (!data.output.width) throw "Mising number attribute 'width'!"
            if (!data.output.height) throw "Mising number attribute 'height'!"
            if (!data.output.pad) throw "Mising number attribute 'pad'!"
            if (!data.output.path) throw "Mising number attribute 'path'!"
            if (!data.output.template) throw "Mising number attribute 'template'!"
            if (!Array.isArray(data.layers)) throw "Missing attribute 'layers[]'!"

            this.data = data
        } catch (ex) {
            throw ex
        }
    }
}
