import colorama

def show():
    print("The configuration file must be a JSON-formatted object of this type:")
    print("{")
    showComment("Host and port of a living Brayns instance.\nExample: r1i7n31.bbp.epfl.ch:28201")
    showAtt("braynsHostAndPort", "string")
    showComment("A folder where we will store temporary frames for movies.")
    showAtt("tempFolder", "string")
    showComment("""Processing a lot of movies will take a lot of time.
Therefore you can experience an unexpected end of connection with Brayns.
That's why, each time a movie has been processed successfuly, this value
will be incremented and the config file overwritten.
This way, the next time you execute this script, it will not process the
already processed movies twice.""")
    showAttOpt("firstMovieToProcess", "number")
    showComment("Radius multiplier for Soma.")
    showAttOpt("somaScale", "number")
    showComment("Final movie resolution.")
    showComment("Example: [1920, 1080]")
    showAtt("resolution", "[number, number]")
    showComment("Frames per second.")
    showAtt("fps", "number")
    showComment("Samples Per Pixel.")
    showComment("Incease the quality, but slows down the rendering.")
    showAtt("spp", "number")
    showComment("Array of movies to be generated.")
    showAtt("movies", "Array<{")
    showComment("Input circuit file full path.", 2)
    showAtt("circuit", "string", 2)
    showComment("Report name.", 2)
    showAtt("report", "string", 2)
    showComment("Cell ID to display.", 2)
    showAtt("gid", "number", 2)
    showComment("Spiking event duration in seconds.", 2)
    showAtt("spikeDuration", "number", 2)
    showComment("Actual movie duration will be 'spikeDuration' * 'slowMotionFactor'.", 2)
    showComment("Default to 1.", 2)
    showAtt("slowMotionFactor", "number", 2)
    showComment("Movie duration in seconds.", 2)
    showAtt("duration", "number", 2)
    showComment("[min, max] of the voltage in millivolts. Used for Transfer Function.", 2)
    showAtt("voltageRange", "[number, number]", 2)
    showComment("Example: \"EPSP attenuation\"", 2)
    showAtt("title", "string", 2)
    showComment("Example: \"L5 TTPC1\\ncADpyr\"", 2)
    showComment("You can use \"\\n\" to make the sub-title split on several lines.", 2)
    showAtt("subTitle", "string", 2)
    showComment("""Movies can have close ups on different parts of the neuron.
Default to false.""", 2)
    showAttOpt("showCloseUpAxon", "boolean", 2)
    showAttOpt("showCloseUpDendrites", "boolean", 2)
    showAttOpt("showCloseUpSoma", "boolean", 2)
    showComment("Name of the final movie. If the folder does not exist, it will be breated.", 2)
    showAtt("outputFilename", "string", 2)
    print("    }>")
    print("}")

def showAtt(name, type, indent=1):
    print(f"{(indent * 4) * ' '}{att(name)}: {value(type)}")

def showAttOpt(name, type, indent=1):
    print(f"{(indent * 4) * ' '}{att(name)}?: {value(type)}")

def showComment(txt, indent=1):
    for line in txt.split("\n"):
        print(f"{(indent * 4) * ' '}{dim('// ' + line)}")

def att(txt):
    return colorama.Fore.GREEN + str(txt) + colorama.Style.RESET_ALL

def dim(txt):
    return colorama.Style.DIM + str(txt) + colorama.Style.RESET_ALL

def value(txt):
    return colorama.Fore.YELLOW + str(txt) + colorama.Style.RESET_ALL
