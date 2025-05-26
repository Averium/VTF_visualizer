from os.path import join
from os import getcwd
from source.file import JsonFile


class PATH:
    ROOT = getcwd()
    DATA = join(ROOT, "data")


COLORS = JsonFile(PATH.DATA, "colors")
CONFIG = JsonFile(PATH.DATA, "config")
VEHICLE = JsonFile(PATH.DATA, "vehicle")
