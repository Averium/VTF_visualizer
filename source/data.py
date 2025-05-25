from os.path import join
from source.file import JsonFile


class PATH:
    DATA = "data"


COLORS = JsonFile(PATH.DATA, "colors")
CONFIG = JsonFile(PATH.DATA, "config")
VEHICLE = JsonFile(PATH.DATA, "vehicle")
