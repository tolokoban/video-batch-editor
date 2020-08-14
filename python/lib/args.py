import sys
import json

class Config:
    flags = []
    config = None

def parse():
    """Parse the arguments and return an object with two attributes:
    - config: configuration filename and path relative to this script.
    - flags: array of all the --options without the leading --."""
    output = Config()
    for arg in sys.argv[1:]:
        if arg[:2] == "--":
            output.flags.append(arg[2:])
        elif arg[0] == "-":
            raise ValueError(f"Single dash options are invalid: {arg}")
        elif output.config != None:
            raise ValueError(f"You must have only one configuration file: {arg}")
        else:
            output.config = arg
    return output
