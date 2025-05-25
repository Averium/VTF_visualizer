from os.path import join
import json


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

    def __init__(self, root: str, filename: str):
        self.root = root
        self.filename = filename

        self.path = join(root, filename)
        self.file = None
        super().__init__(self.load())

    def load(self) -> dict:
        return dict()


class JsonFile(File):

    EXTENSION = "json"

    def load(self):
        with open(f"{self.path}.{JsonFile.EXTENSION}", "r") as self.file:
            return json.load(self.file)
