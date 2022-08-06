import os
import sys
import importlib

CURRENT_PATH = os.path.dirname(__file__)
VERSION = os.path.basename(os.path.dirname(CURRENT_PATH))
REPOSITORY = "library"


def MODULES():
    modules = []
    return modules


def RELOAD():
    invalids = []
    for index, each in enumerate(MODULES()):
        try:
            module = importlib.import_module(each)
            print("\t\t %s. %s" % (index + 1, module))
        except Exception as error:
            module = None
            print("\t\t %s reload error, %s" % (index + 1, error))
            invalids.append(error)
        if not module:
            continue
        if sys.version_info[:2] >= (3, 4):
            importlib.reload(module)
        else:
            reload(module)
    if invalids:
        return False
    return True
