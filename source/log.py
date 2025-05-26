

class Log:

    PREFIX = "FRAMEWORK"

    INFO = f"{PREFIX}[INFO]:"
    ERROR = f"{PREFIX}[ERROR]:"

    @classmethod
    def info(cls, message):
        print(cls.INFO, message)

    @classmethod
    def error(cls, message):
        print(cls.ERROR, message)
