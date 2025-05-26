import sys

from source.framework import Framework


def main(arguments = ()):

    framework = Framework()
    framework.start()

    for argument in arguments:
        if argument.endswith(".py"):
            continue
        framework.load_data(argument)


if __name__ == "__main__":
    main(sys.argv)