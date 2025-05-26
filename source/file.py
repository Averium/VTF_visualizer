from fileinput import filename
from os.path import join
import json

from scipy.io import loadmat


class Dataclass:
    """
    This class is used to store data, imported from .json files,
    or dictionaries, and provide easy access to it.
    """

    def __init__(self, data: dict):
        self.builtin = None
        self.builtin = self.__dir__()
        self.fill(data)

    @property
    def data(self):
        return {key: getattr(self, key) for key in self.__dir__() if key not in self.builtin}

    def fill(self, data):
        for key in self.data:
            delattr(self, key)

        for key, value in data.items():
            setattr(self, key, value)



class File(Dataclass):

    EXTENSION = ""

    def __init__(self, root: str, filename: str):
        self.root = root
        self.filename = filename
        self.file = None

        super().__init__(self.load())

    def load(self) -> dict:
        return dict()

    @property
    def path(self):
        if self.filename.endswith(self.EXTENSION):
            return join(self.root, self.filename)
        else:
            return f"{join(self.root, self.filename)}{self.EXTENSION}"


class JsonFile(File):

    EXTENSION = ".json"

    def load(self):
        with open(self.path, "r") as self.file:
            return json.load(self.file)


class MatFile(File):

    EXTENSION = ".mat"

    def load(self):
        return loadmat(self.path)