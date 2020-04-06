import pathlib

class Filmstrip:
    def __init__(self, filmstrip):
        folder = filmstrip["folder"]
        template = filmstrip["template"]
        path = pathlib.Path(folder)
        if not path.is_dir():
            raise Exception("Filmstrip folder does not exists: {}".format(folder))
        files = [str(x.absolute()) for x in path.glob(template)]
        files.sort()
        self.files = files

    def count(self):
        return len(self.files)

    def get_frame_path(self, frame_number):
        return self.files[frame_number]
