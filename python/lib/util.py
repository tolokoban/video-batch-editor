import json

def parse_json(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError as ex:
        raise Exception("This is not a valid JSON file:\n{}\n{}".format(ex.msg, show_error(content, ex.lineno, ex.colno)))
    except Exception as ex:
        raise Exception("This is not a valid JSON file:\n{}".format(ex))

def load_file_content(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
        return data
    except Exception as ex:
        raise FileNotFoundError("Unable to read file \"{0}\": {1}".format(filename, ex))

def save_file_content(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
    except Exception as ex:
        raise FileNotFoundError("Unable to write file \"{0}\": {1}".format(filename, ex))

def show_error(content, line_num, col_num):
    content_lines = content.split("\n")
    start = max(0, line_num - 4)
    end = min(len(content_lines), line_num + 3)
    lines = content_lines[start:end]
    out = f"\n"
    current_line_number = start + 1
    for line in lines:
        out = out + "{0}: {1}\n".format(pad(current_line_number, 3), line)
        if line_num == current_line_number:
            out = out + "--- {0}^\n".format(" " * col_num)
        current_line_number = current_line_number + 1
    return out

def pad(number, padding, fill="0"):
    text = str(number)
    while len(text) < padding:
        text = f"{fill}{text}"
    return text
