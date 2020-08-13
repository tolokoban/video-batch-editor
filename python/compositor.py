#!/usr/bin/python3

import sys
import kernel
import kernel.style
import traceback

try:
    if len(sys.argv) < 2:
        print(kernel.usage())
    else:
        config_filename = sys.argv[1]
        if config_filename == "--help":
            print(kernel.help())
        else:
            config = kernel.load_config(config_filename)
            kernel.process(config)
except Exception as ex:
    print("""
Fatal Error
-----------
{0}


Please execute this command to get a full documentation of this tool:
$ python3 {1} --help

Or this one to get more technical details on the error:
$ python3 {1} config.json --debug

""".format(kernel.style.error(str(ex)), sys.argv[1]))
    if "--debug" in sys.argv:
        print(kernel.style.red(traceback.format_exc()))
        print()
    sys.exit(1)
