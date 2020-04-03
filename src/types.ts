export type ISize = "cover" | "contain" | "original"

export interface IPoint {
    x: number,
    y: number
}

export interface IDimension {
    width: number,
    height: number
}

export interface ITask {
    output: {
        width: number,
        height: number,
        // Output folder.
        path: string,
        // If the frames are named image001.png, image002.png, ...
        // template will be "image*.png", and the pad will be 3.
        // The start is the placeholder for the frame number.
        template: string,
        // Padding for frame index. Every frame index will be left padded
        // with zeros before replacing the "*" in the template to get
        // the final frame name.
        pad: number,
        // You can use a subset of the frames by defining
        // firstFrame and/or lastFrame.
        firstFrame?: number,
        lastFrame?: number
    }
    filmstrips: {
        [key: string]: {
            folder: string,
            // If the frames are named image001.png, image002.png, ...
            // template will be "image*.png".
            // The start is the placeholder for the frame number.
            template: string,
            // You can use a subset of the frames by defining
            // firstFrame and/or lastFrame.
            firstFrame?: number,
            lastFrame?: number
        }
    },
    layers: Array<{
        // If the name starts with a "#",
        // it is a filmstrip frame.
        image: string,
        // - cover: resized in order to cover entirely the output image.
        // - contain: resized as much possible still being contained in the output image.
        size: "cover" | "contain",
        // Coordinatesare defined in a square of side 2.0 surrounding the output image.
        // For example, if the output image is 640x480:
        //  - Top Left corner is: (-1,4/5).
        //  - Bottom Right corner is: (1,-4/5).
        x?: number,  // Center of the image. Default to 0.
        y?: number,  // Center of the image. Default to 0.
        center?: [number, number],  // By default the center is [0,0]. But it can be shifted.
        // If you want to make a perfect square of specific width, just set height to 0.
        // And of course, set width to 0 if you want a square with specific height.
        width?: number,  // Default to the width of output image.
        height?: number, // Default to the height of output image.
        // Scale is multiplied to the computed size.
        scale?: number,
        clip?: {
            // Same type of coordinates that the one used before.
            x?: number,      // Default to parent X.
            y?: number,      // Default to parent Y.
            center?: [number, number],  // Default to [0,0].
            width?: number,  // Default to parent Width.
            height?: number  // Default to parent Height.
        }
    }>
}
