import sys
import kernel.config
from PIL import Image

def load_config(filename):
    return kernel.config.load(filename)

def process(config):
    for frame_index in range(config.nb_frames):
        print("Processing frame {0} / {1} ...".format(frame_index + 1, config.nb_frames))
        (width, height) = config.output_dimension
        output = Image.new('RGBA', (width, height))
        process_frame(config, frame_index, output)
        output_filename = config.output_filename(frame_index)
        if output_filename[-4:] == ".jpg":
            output = output.convert("RGB")
        output.save(output_filename)
        if "--preview" in sys.argv:
            output.show()
            break

def process_frame(config, frame_index, output):
    for layer_index in range(len(config.layers)):
        layer = config.layers[layer_index]
        try:
            layer["image"] = layer["images"][frame_index]
            process_layer(config, layer, output)
        except Exception as ex:
            raise Exception("Error while processing layer #{0} of frame #{1}:\n{2}".format(layer_index, frame_index, ex))

def process_layer(config, layer, output):
    (w_out, h_out) = output.size
    input = Image.open(layer["image"])
    scale = compute_contain_scale(input, output, layer["size"]) * layer["scale"]
    (w_in, h_in) = input.size
    input = input.resize((int(w_in * scale), int(h_in * scale)), Image.LANCZOS)
    (x_out, y_out) = scr_to_img(layer["x"], layer["y"], output)
    (x_center, y_center) = layer["center"]
    (x_in, y_in) = scr_to_img(x_center, y_center, input)
    x = int(x_out - x_in)
    y = int(y_out - y_in)
    clip = (0, 0, w_out, h_out)
    if "clip" in layer:
        (xx, yy) = scr_to_img(layer["clip"]["x"], layer["clip"]["y"], output)
        w = layer["clip"]["width"] * w_out
        h = layer["clip"]["height"] * h_out
        if w <= 0:
            w = h
        elif h <= 0:
            h = w
        clip = (xx - w / 2, yy - h / 2, w, h)
    draw_image(output, input, x, y, clip)

def draw_image(output, input, x, y, clip):
    (w_out, h_out) = output.size
    (w_in, h_in) = input.size
    (x_clip, y_clip, w_clip, h_clip) = clip

    # *_out is the output region in which the drawing must be contained.
    x1_out = max(0, x_clip)
    y1_out = max(0, y_clip)
    x2_out = min(w_out - 1, x_clip + w_clip)
    y2_out = min(h_out - 1, y_clip + h_clip)

    # *_in is the region the input wants to occupy before clipping.
    x1_in = x
    y1_in = y
    x2_in = x + w_in
    y2_in = y + h_in

    # Test if input is completely outside the output clipping box.
    if x1_out > x2_in: return
    if y1_out > y2_in: return
    if x2_out < x1_in: return
    if y2_out < y1_in: return

    # Coords of the top/left corner of the cropped image into the output one.
    x_out = max(x1_in, x1_out)
    y_out = max(y1_in, y1_out)
    x1_crop = max(0, x1_out - x1_in)
    y1_crop = max(0, y1_out - y1_in)
    x2_crop = w_in - max(0, x2_in - x2_out)
    y2_crop = h_in - max(0, y2_in - y2_out)

    crop = (x1_crop, y1_crop, x2_crop, y2_crop)
    cropped_input = input.crop(crop)

    x_out = int(x_out)
    y_out = int(y_out)

    if input.mode == "RGBA":
        output.alpha_composite(cropped_input, (x_out, y_out))
    else:
        output.paste(cropped_input, (x_out, y_out))

def scr_to_img(x, y, image):
    (w, h) = image.size
    x = (x + 1) / 2
    y = (1 - y) / 2
    return (x * w, y * h)

def compute_contain_scale(input, output, type):
    (w_in, h_in) = input.size
    (w_out, h_out) = output.size
    scale_w = w_out / w_in
    scale_h = h_out / h_in
    if type == "cover":
        return max(scale_w, scale_h)
    else:
        return min(scale_w, scale_h)


def usage():
    return """
The compositor needs one and only one argument: the JSON config filename.

Starting process:
    python3 {0} config.json

Just previewing the first frame:
    python3 {0} config.json --preview

Detailed help:
    python3 {0} --help

""".format(sys.argv[0])

def help():
    return """
The configuration file must be in JSON format and its type must be conform to this:

{
    output: {
        width: number,
        height: number,
        // Output folder.
        folder: string,
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

Here is an example:

{
    "output": {
        "width": 800, "height": 600, "folder": "output", "template": "final*.jpg", "pad": 4
    },
    "filmstrips": {
        "main": { "folder": "input", "template": "frame-*.png" }
    },
    "layers": [
        { "image": "gfx/background.jpg", "size": "cover" },
        { "image": "#main", "size": "contain", "x": -0.5, "y": 0 },
        { "image": "gfx/zoom-back.png", "size": "cover" },
        {
            "image": "#main", "size": "contain", "scale": 2.0,
            "x": 0.5, "y": 0.5,
            "clip": { "x": 0.6, "y": 0.5, "height": 0.4 }
        },
        { "image": "gfx/zoom-front.png", "size": "cover" },
        {
            "image": "gfx/logo.png", "size": "contain",
            "x": 1, "y": -1, "center": [1, -1], "scale": 0.2
        }
    ]
}

For each frame, the tool paints all the layers in order.

The first layer will just "cover" the output with a background image.
  >  { "image": "gfx/background.jpg", "size": "cover" }
All the images pathes are relative to the JSON configuration file.

The second layer will use a frame of the filmstrip with key "main".
  >  { "image": "#main", "size": "contain", "x": -0.5, "y": 0 }
The coords (x,y) are in image space. bottom/left corner is (-1,-1),
top/right corner is (+1,+1) and center is (0,0).

In the fourth layer we use scaleing and clipping.
  >  {
  >      "image": "#main", "size": "contain", "scale": 2.0,
  >      "x": 0.5, "y": 0.5,
  >      "clip": { "x": 0.6, "y": 0.5, "height": 0.4 }
  >  }

"""
