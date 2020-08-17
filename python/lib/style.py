import json
import colorama

colorama.init()

def red(txt):
    return colorama.Fore.RED + str(txt) + colorama.Style.RESET_ALL

def error(txt):
    return colorama.Back.RED + colorama.Fore.WHITE + box(txt) + colorama.Style.RESET_ALL

def box(txt, max_length=120):
    input_lines = str(txt).split("\n")
    length = 0
    output_lines = []
    for line in input_lines:
        while len(line) > max_length:
            length = max_length
            output_lines.append(line[:max_length])
            line = line[max_length:]
        length = max(length, len(line))
        output_lines.append(line)
    output = "+" + ("-" * (length + 2)) + "+\n"
    for line in output_lines:
        output = output + "| " + line + (" " * (length - len(line) + 1)) + "|\n"
    output = output + "+" + ("-" * (length + 2)) + "+"
    return output

def info(txt, more=""):
    return colorama.Fore.CYAN + txt + colorama.Style.BRIGHT + more + colorama.Style.RESET_ALL

def att(name, value="", indent=None):
    return name + colorama.Style.DIM + ": " + colorama.Style.RESET_ALL + colorama.Style.BRIGHT + json.dumps(value, indent=indent) + colorama.Style.RESET_ALL
