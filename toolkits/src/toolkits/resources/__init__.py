import os
import json
import pkgutil

CURRENT_PATH = os.path.dirname(__file__)


def getIconPath():
    return os.path.join(CURRENT_PATH, "icons")


def getInputPath():
    return os.path.join(CURRENT_PATH, "inputs")


def getInputData(name, enable=False):
    path = os.path.join(getInputPath(), "%s.json" % name)
    data = getData(path)
    if not data.get("enable"):
        return None
    if not enable:
        return data["data"]
    enabled_data = list(
        filter(lambda k: k["enable"] == True, data["data"])
    )
    return enabled_data


def getData(path):
    if not os.path.isfile(path):
        raise IOError("not found path <%s>" % path)
    with open(path, "r") as file:
        data = json.load(file)
        return data


def getPackages(root_path):
    packages = []
    for module_loader, name, ispkg in pkgutil.iter_modules(
        [root_path]
    ):
        loader = module_loader.find_module(name)
        module = loader.load_module(name)
        if not hasattr(module, "ENABLE"):
            continue
        if not module.ENABLE:
            continue
        current_order = 0
        if hasattr(module, "ORDER"):
            current_order = module.ORDER
        packages.append(module)
    return packages
