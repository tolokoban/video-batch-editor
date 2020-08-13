import pathlib
import kernel.util
import kernel.filmstrip

def load(filename):
    try:
        content = kernel.util.loadFileContent(filename)
        path = pathlib.Path(filename).parent.absolute()
        data = kernel.util.parse_json(content)
        return Config(data, path)
    except Exception as ex:
        raise Exception("Trying to parse config file: {0}\n{1}".format(pathlib.Path(filename).absolute(), ex))

class Config:
    output_dimension = [0,0]
    output_folder = ""
    output_template = ["", ""]
    output_pad = 0
    filmstrips = {}
    nb_frames = 0
    layers = []

    def __init__(self, data, working_directory):
        self.working_directory = working_directory
        self.check(data)
        self.parse_output(data)
        self.parse_filmstrips(data)
        self.parse_layers(data)

    def parse_layers(self, data):
        layers = data["layers"]
        for layer_index in range(len(layers)):
            layer = layers[layer_index]
            try:
                image = layer["image"]
                if image[0] == '#':
                    images = self.get_images_from_filmstrip(image[1:])
                else:
                    images = self.get_images_from_image(image)
                layer["images"] = images
                self.layers.append(layer)
                if "clip" in layer:
                    clip = layer["clip"]
                    w = clip["width"]
                    h = clip["height"]
                    if w <= 0 and h <= 0:
                        raise Exception(
                            "For clip definition, either width or height must be strictly positive!\nYou provided: {0}"
                            .format(layer["clip"]))
            except Exception as ex:
                raise Exception("Bad definition of layer #{0}!\n{1}".format(layer_index, ex))

    def get_images_from_image(self, name):
        path = pathlib.Path(self.working_directory, name).absolute()
        if not path.is_file():
            raise Exception("Image not found: {0}".format(path))
        return [str(path)] * self.nb_frames

    def get_images_from_filmstrip(self, name):
        images = []
        filmstrip = self.filmstrips[name]
        if filmstrip == None:
            raise Exception("This filmstrip has not been defined: {0}".format(name))
        ratio = filmstrip.count() / self.nb_frames
        for i in range(self.nb_frames):
            images.append(filmstrip.get_frame_path(int(i * ratio)))
        return images

    def parse_filmstrips(self, data):
        filmstrips = data["filmstrips"]
        for key in filmstrips.keys():
            try:
                filmstrip = kernel.filmstrip.Filmstrip(filmstrips[key])
                self.filmstrips[key] = filmstrip
                self.nb_frames = max(self.nb_frames, filmstrip.count())
            except FileNotFoundError as ex:
                raise FileNotFoundError(f"Definition error in \"filmstrips/{key}\":\n{str(ex)}")

    def parse_output(self, data):
        output = data["output"]
        self.output_dimension = [output["width"], output["height"]]
        self.output_folder = self.abs_dir(output["folder"],
            "Output folder not found or not a directory")
        self.output_template = output["template"].split("*")
        self.output_pad = output["pad"]

    def output_filename(self, frame_index):
        index = kernel.util.pad(frame_index, self.output_pad)
        return str(pathlib.Path(self.output_folder, index.join(self.output_template)).absolute())

    def abs_dir(self, path, msg="Directory not found"):
        path = pathlib.Path(self.working_directory, path)
        if not path.is_dir():
            raise Exception("{0}: {1}\n$ mkdir -p {2}".format(msg, path.absolute(), path.absolute()))
        return path.absolute()

    def check(self, data):
        self.ensure_attributes_exist(data, ["output", "filmstrips", "layers"])
        output = data["output"]
        self.ensure_attributes_exist(
            output,
            ["width", "height", "folder", "template", "pad"],
            "output.")
        filmstrips = data["filmstrips"]
        for key in filmstrips.keys():
            filmstrip = filmstrips[key]
            self.ensure_attributes_exist(
                filmstrip,
                ["folder", "template"],
                "filmstrips.{0}.".format(key))
        layers = data["layers"]
        for layer_index in range(len(layers)):
            layer = layers[layer_index]
            self.ensure_attributes_exist(
                layer,
                ["image", "size"],
                "layers[{0}].".format(layer_index))
            if "x" not in layer:
                layer["x"] = 0
            if "y" not in layer:
                layer["y"] = 0
            if "center" not in layer:
                layer["center"] = (0,0)
            if "scale" not in layer:
                layer["scale"] = 1
            if "clip" in layer:
                clip = layer["clip"]
                if "x" not in clip:
                    clip["x"] = 0
                if "y" not in clip:
                    clip["y"] = 0
                if "width" not in clip:
                    clip["width"] = 0
                if "height" not in clip:
                    clip["height"] = 0

    def ensure_attributes_exist(self, data, attributes, prefix=""):
        for attrib in attributes:
            if attrib not in data:
                raise Exception("Missing mandatory config attribute: \"{0}{1}\"!".format(prefix, attrib))
