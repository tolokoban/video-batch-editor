const FS = window.require('fs')
const Path = window.require('path')

export default {
    createImageFromFile,
    deleteFile,
    exists,
    isDir,
    join,
    listFiles,
    save
}

function join(...path: string[]): string {
    return Path.join(...path)
}

async function deleteFile(path: string) {
    try {
        await FS.promises.unlink(path)
    } catch (ex) {
        console.error(`Unable to delete "${path}"!`, ex)
    }
}

async function createImageFromFile(path: string): Promise<HTMLImageElement> {
    const content = await FS.promises.readFile(path)
    const base64 = content.toString('base64')
    return new Promise((resolve, reject) => {
        const img = new Image()
        img.onload = () => {
            resolve(img)
        }
        img.onerror = () => {
            console.error(`Unable to load image "${path}"!`)
            reject(img)
        }
        img.src = `data:${getMimeType(path)};base64,${base64}`
    })
}

async function save(path: string, content: any) {
    await FS.promises.writeFile(path, content)
}

function getMimeType(filename: string): string {
    const name = filename.toLowerCase()
    if (name.endsWith('.png')) {
        return 'data:image/png'
    }
    if (name.endsWith('.gif')) {
        return 'data:image/gif'
    }
    return 'data:image/jpeg'
}

function exists(path: string): boolean {
    return FS.existsSync(path)
}


async function isDir(path: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
        try {
            if (!exists(path)) {
                resolve(false)
                return
            }

            FS.stat(path, (err: any, stats: any) => {
                if (err) {
                    reject(err)
                } else {
                    resolve(stats.isDirectory())
                }
            })
        } catch (ex) {
            reject(ex)
        }
    })
}

async function listFiles(path: string) {
    const filesAndFolders = await FS.promises.readdir(path)
    const files: string[] = []
    for (const name of filesAndFolders) {
        const isFile = !(await isDir(Path.join(path, name)))
        if (isFile) {
            files.push(name)
        }
    }
    files.sort()
    return files
}
