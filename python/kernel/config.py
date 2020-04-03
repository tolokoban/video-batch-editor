import pathlib
import kernel.util

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

    def __init__(self, data, working_directory):
        self.working_directory = working_directory
        self.check(data)
        self.parse_output(data)

    def parse_output(self, data):
        output = data["output"]
        self.output_dimension = [output["width"], output["height"]]
        self.output_folder = self.abs_dir(output["folder"],
            "Output folder not found or not a directory")
        self.output_template = output["template"].split("*")
        self.output_pad = output["pad"]

    def output_filename(self, frame_index):
        index = kernel.util.pad(frame_index, self.output_pad)
        return pathlib.Path(self.output_folder, index.join(self.output_template)).absolute()

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
            if "width" not in layer:
                layer["width"] = 2
            if "height" not in layer:
                layer["height"] = 2
            if "scale" not in layer:
                layer["scale"] = 1
            if "clip" in layer:
                clip = layer["clip"]
                if "x" not in clip:
                    clip["x"] = 0
                if "y" not in clip:
                    clip["y"] = 0
                if "width" not in clip:
                    clip["width"] = layer["width"]
                if "height" not in clip:
                    clip["height"] = layer["height"]


    def ensure_attributes_exist(self, data, attributes, prefix=""):
        for attrib in attributes:
            if attrib not in data:
                raise Exception("Missing mandatory config attribute: \"{0}{1}\"!".format(prefix, attrib))
