import os
import shutil
import os.path

def clean_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path, False)
    os.mkdir(path)
