import json

def parse_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError as ex:
        raise Exception("This is not a valid JSON file: {}\n\n{}".format(ex.msg, show_error(content, ex.lineno, ex.colno)))
    except Exception as ex:
        raise Exception("This is not a valid JSON file: {}".format(ex))

def loadFileContent(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return data
    except Exception as ex:
        raise Exception("Unable to read file \"{0}\": {1}".format(filename, ex))

def show_error(content, line_num, col_num):
    print("line = {0}, col = {1}".format(line_num, col_num))
    start = max(0, line_num - 4) - 1
    end = line_num
    lines = content.split("\n")[start:end]
    out = ""
    current_line_number = start + 1
    for line in lines:
        out = out + "{0}: {1}\n".format(pad(current_line_number, 3), line)
        if line_num == current_line_number:
            out = out + "    {0}^\n".format(" " * col_num)
        current_line_number = current_line_number + 1
    return out

def pad(number, padding):
    text = str(number)
    while len(text) < padding:
        text = "0{0}".format(text)
    return text
