import sys
import json
import lib.args
import lib.help
import lib.util
import lib.style
import lib.brayns
import lib.config
import lib.process
import traceback

try:
    print(lib.style.box("SSCx portal movie maker version 0.1.0"))
    args = lib.args.parse()
    if "help" in args.flags:
        lib.help.show()
        sys.exit(0)
    if args.config == None:
        raise ValueError("Configuration filename is missing!")
    cfg = lib.config.parse(args.config)
    if "preview" in args.flags:
        print(lib.style.info("No connection to Brayns: ", "preview mode!"))
        brayns = None
    else:
        brayns = lib.brayns.Brayns(cfg)
    if "test" in args.flags:
        cfg["firstMovieToProcess"] = 0
        lib.process.exec(cfg, brayns, args.flags)
    else:
        while lib.process.exec(cfg, brayns, args.flags):
            lib.util.save_file_content(args.config, json.dumps(cfg, indent=4))
    print(lib.style.info("Script has finished ", "successfuly!"))
except Exception as ex:
    print(f"""
{lib.style.error(str(ex))}

Execute this command to get a full documentation of this tool:
$ python3 {sys.argv[0]} --help

Or this one to get more technical details on the error:
$ python3 {sys.argv[0]} config.json --debug

""")
    if "--debug" in sys.argv:
        print(lib.style.red(traceback.format_exc()))
        print()
    sys.exit(1)
