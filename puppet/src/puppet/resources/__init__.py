import os


CURRENT_PATH = os.path.dirname(__file__)


def packagePath():
    return os.path.dirname(CURRENT_PATH)


def getScriptPath():
    return os.path.join(packagePath(), "scripts")


def getValidatePath():
    return os.path.join(packagePath(), "validate")


def getBakePath():
    return os.path.join(packagePath(), "bake")


if __name__ == "__main__":
    pass
