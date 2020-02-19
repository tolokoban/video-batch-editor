export default {
    resizeToContain,
    resizeToCover
}

export interface ITransform {
    scale: number,
    translateX: number,
    translateY: number
}

export type IAlign = "start" | "center" | "end"


function resizeToContain(srcW: number, srcH: number,
                         dstW: number, dstH: number,
                         align: IAlign = "center"): ITransform {
    const scaleX = dstW / srcW
    const scaleY = dstH / srcH
    const scale = Math.min(scaleX, scaleY)
    const newW = srcW * scale
    const newH = srcH * scale

    switch (align) {
        case "start":
            return {
                scale,
                translateX: 0,
                translateY: 0
            }
        case "end":
            return {
                scale,
                translateX: scaleX > scaleY ? (dstW - newW) : 0,
                translateY: scaleX > scaleY ? 0 : (dstH - newH)
            }
        default:  // Center.
            return {
                scale,
                translateX: scaleX > scaleY ? (dstW - newW) / 2 : 0,
                translateY: scaleX > scaleY ? 0 : (dstH - newH) / 2
            }
    }
}


function resizeToCover(srcW: number, srcH: number,
                       dstW: number, dstH: number,
                       align: IAlign = "center"): ITransform {
    const scaleX = dstW / srcW
    const scaleY = dstH / srcH
    const scale = Math.max(scaleX, scaleY)
    const newW = srcW * scale
    const newH = srcH * scale

    switch (align) {
        case "start":
            return {
                scale,
                translateX: 0,
                translateY: 0
            }
        case "end":
            return {
                scale,
                translateX: scaleX > scaleY ? -(dstW - newW) : 0,
                translateY: scaleX > scaleY ? 0 : -(dstH - newH)
            }
        default:  // Center.
            return {
                scale,
                translateX: scaleX > scaleY ? -(dstW - newW) / 2 : 0,
                translateY: scaleX > scaleY ? 0 : -(dstH - newH) / 2
            }
    }
}
