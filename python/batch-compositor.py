import sys
import kernel

try:
    if len(sys.argv) < 2:
        print(kernel.usage())
    else:
        config_filename = sys.argv[1]
        if config_filename == "--help":
            print(kernel.help())
        else:
            config = kernel.load_config(config_filename)
            print(config.output_filename(7))
except Exception as ex:
    print("""
Fatal Error
-----------
{0}


Please execute this command to get a full documentation of this tool:
$ python3 {1} --help

""".format(ex, sys.argv[1]))
    sys.exit(1)
