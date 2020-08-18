import os.path
import lib.util

def parse(config_filename):
    """Return a parsed JSON configuration file."""
    if config_filename == "" or config_filename == None:
        raise ValueError("Missing configuration filename!")
    try:
        cfg = lib.util.parse_json(
            lib.util.load_file_content(config_filename)
        )
        checkStr(cfg, "braynsHostAndPort")
        checkStr(cfg, "tempFolder")
        checkInt(cfg, "firstMovieToProcess", 0)
        checkFloat(cfg, "somaScale", 3)
        checkFloat(cfg, "materialSpecularExponent", 15)
        checkFloat(cfg, "materialGlossiness", 0.2)
        checkFloat(cfg, "materialEmission", 0.1)
        checkInt(cfg, "fps", 30)
        checkCouple(cfg, "resolution", [1920, 1080])
        movies = cfg["movies"]
        if cfg["firstMovieToProcess"] >= len(movies):
            raise Exception("There is nothing more to do in this configuration file!\nPlease reset the attribute \"firstMovieToProcess\" to 0.")
        if type(movies) != list:
            raise Exception("Attribute \"movies\" must be an array!")
        for movie in movies:
            index = 0
            try:
                checkStr(movie, "circuit")
                checkFileExists(movie["circuit"])
                checkStr(movie, "report")
                checkInt(movie, "gid")
                checkFloat(movie, "duration")
                checkInt(movie, "firstSimulationStep", 0)
                checkInt(movie, "lastSimulationStep")
                checkCouple(movie, "voltageRange", [-80, -10])
                checkStr(movie, "title", "")
                checkStr(movie, "subTitle", "")
                checkBool(movie, "showCloseUpAxon", False)
                checkBool(movie, "showCloseUpDendrites", False)
                checkBool(movie, "showCloseUpSoma", False)
                checkStr(movie, "outputFilename")
                index = index + 1
            except Exception as ex:
                raise Exception(f"Error in definition of movie #{index}:\n{str(ex)}")

    except Exception as ex:
        raise Exception(f"Invalid configuration file: {config_filename}\n{str(ex)}")
    return cfg


def check(data, name, default=None):
    if not name in data:
        if default != None:
            data[name] = default
        else:
            raise Exception(f"Missing attribute: {name}!")

def checkStr(data, name, default=None):
    check(data, name, default)
    value = data[name]
    if type(value) != str:
        raise Exception(f"Attribute \"{name}\" must be a string!")

def checkBool(data, name, default=None):
    check(data, name, default)
    value = data[name]
    if type(value) != bool:
        raise Exception(f"Attribute \"{name}\" must be a boolean!")

def checkInt(data, name, default=None):
    check(data, name, default)
    value = data[name]
    if type(value) != int:
        raise Exception(f"Attribute \"{name}\" must be an integer!")

def checkFloat(data, name, default=None):
    check(data, name, default)
    value = data[name]
    if type(value) != float and type(value) != int:
        raise Exception(f"Attribute \"{name}\" must be a float!")

def checkCouple(data, name, default=None):
    check(data, name, default)
    value = data[name]
    if type(value) != list:
        raise Exception(f"Attribute \"{name}\" must be a list of numbers!")
    if len(value) != 2:
        raise Exception(f"Attribute \"{name}\" must be a list of TWO numbers!")
    for sub_value in value:
        if type(sub_value) != int and type(sub_value) != float:
            raise Exception(f"Attribute \"{name}\" must be a list of TWO numbers!")

def checkFileExists(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"Circuit not found: {filename}\nBoth this script and Brayns must be able to access the circuit's file for read only.")
