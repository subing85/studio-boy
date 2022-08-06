# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:30:Thursday-03:13:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe Command Prompt.

import os
import json
import optparse

CURRENT_PATH = os.path.dirname(__file__)

DEVKIT_PATH = os.getenv("DEVKIT-PATH")
PROJECT_DIRNAME = os.getenv("PROJECT-DIRNAME")


def execute():
    parser = optparse.OptionParser(
        usage='usage: %prog\n\tto launch the studio pipe "Command Prompt"',
        version="studio-pipe-cmd 0.0.1",
    )
    option_list = []
    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    if not DEVKIT_PATH:
        raise Exception(
            'invalid "DEVKIT-PATH" install the pipe and try'
        )
        return None
    if not PROJECT_DIRNAME:
        raise Exception(
            'invalid "PROJECT-DIRNAME" install the pipe and try'
        )
        return None

    setHeader()
    contexts = getCoreContext()
    initializeCore(contexts)
    contexts = getPackageContext()
    initializePackages(contexts, python=False)
    print("\n# initialize the packages completed!...\n")
    os.system('cmd /k echo "<welcome to pipe command>"')


def setHeader():
    headers = [
        "Studio Pipe Startup",
        "Version : 0.0.1 Release.",
        "Last modified : 2021:December:29:Wednesday-07:26:15:PM",
        "Author : Subin. Gopi (subing85@gmail.com)",
        'Description : setup the studio pipe "Command Prompt"',
        "Copyright (c) 2021, https://www.subins-toolkits.com All rights reserved.",
    ]
    print("#" * 75)
    for header in headers:
        print(header)
    print("#" * 75)


def getCoreContext():
    input = getConfig()
    python_context = searchContext(input, "PYTHON_VERSION")
    python_version = python_context["value"]
    python_dirname = pathResolver(
        os.path.join(
            DEVKIT_PATH, "module/software/python", python_version
        )
    )
    contexts = [
        {
            "env": "BIN-PATH",
            "value": pathResolver(
                os.path.join(DEVKIT_PATH, "pipeline/bin")
            ),
        },
        {
            "env": "PIPELINE-PATH",
            "value": pathResolver(
                os.path.join(DEVKIT_PATH, "pipeline")
            ),
        },
        {
            "env": "RESOURCE-ROOT",
            "value": pathResolver(
                os.path.join(DEVKIT_PATH, "pipeline/resources")
            ),
        },
        {"env": "PYTHON-VERSION", "value": python_version},
        {"env": "PYTHON-DIRNAME", "value": python_dirname},
        {
            "env": "PYTHON-EXE",
            "value": pathResolver(
                os.path.join(python_dirname, "python.exe")
            ),
        },
        {
            "env": "PYTHON-LIB",
            "value": pathResolver(
                os.path.join(python_dirname, "lib")
            ),
        },
    ]
    contexts.extend(input)
    return contexts


def initializeCore(contexts):
    for context in contexts:
        os.environ[context["env"]] = context["value"]
    bin_context = list(
        filter(lambda k: k["env"] == "BIN-PATH", contexts)
    )
    if bin_context:
        path_context = update_path(bin_context[0]["value"])
        contexts.append(path_context)
    findCoreContexts(contexts)


def getPackageContext():
    pipline_path = os.getenv("PIPELINE-PATH")
    config_path = os.path.join(pipline_path, "config.json")
    if not os.path.isfile(config_path):
        raise IOError("not found path <%s>" % config_path)
    with open(config_path, "r") as file:
        contexts = json.load(file)
        if not contexts.get("enable"):
            return None
        data = contexts.get("data")
        contents = list(filter(lambda k: k.get("enable"), data))
        return contents


def initializePackages(contexts, python=False):
    pipeline_path = os.environ["PIPELINE-PATH"]
    if python:
        python_dirname = os.environ["PYTHON-DIRNAME"]
        python_paths = [
            python_dirname,
            "%s/%s" % (python_dirname, "Lib"),
            "%s/%s/%s" % (python_dirname, "Lib", "site-packages"),
        ]
    else:
        python_paths = []

    for each in contexts:
        pack_version = "%s-%s" % (each["env"], "VERSION")
        pack_path = "%s-PATH" % each.get("env")
        path = pathResolver(
            os.path.join(pipeline_path, each["name"], "src")
        )
        os.environ[pack_version] = each.get("version")
        os.environ[pack_path] = path
        python_paths.append(path)
        each["path"] = path
    packages = list(map(lambda k: k["name"], contexts))
    os.environ["PACKAGES"] = os.pathsep.join(packages)
    os.environ["PYTHONPATH"] = os.pathsep.join(python_paths)
    findPackageContexts(contexts)


def findCoreContexts(contexts):
    print("\n\t<Core Environments>")
    for context in contexts:
        if context["env"] == "PATH":
            continue
        print(
            context["env"].rjust(25), ":", os.getenv(context["env"])
        )
    print("PATH".rjust(25), ":", os.getenv("BIN-PATH"))


def findPackageContexts(contexts):
    print("\n\t<Package Environments>")
    for each in contexts:
        pack_version = "%s-%s" % (each["env"], "VERSION")
        pack_path = each.get("env")
        result = "%s: [%s, %s]" % (
            each["env"].rjust(25),
            os.getenv(pack_version),
            os.getenv(pack_path),
        )
        print(result)
    print("\n\t<Python Environments>")
    print("PYTHONPATH".rjust(25))
    for each in os.getenv("PYTHONPATH").split(os.pathsep):
        print("".rjust(24), ":", os.path.expandvars(each))


def update_path(path):
    context = {"env": "PATH", "value": path}
    exist_path = os.getenv("PATH").split(os.pathsep)
    if path in exist_path:
        return context
    paths = os.getenv("PATH") + os.pathsep.join([path])
    os.environ["PATH"] = paths
    return context


def getConfig():
    filepath = pathResolver(
        os.path.join(DEVKIT_PATH, "pipeline/bin/config.json")
    )
    if not os.path.isfile(filepath):
        raise IOError("not found path <%s>" % filepath)
    with open(filepath, "r") as file:
        data = json.load(file)
        if not data.get("enable"):
            return None
        context = list(
            filter(lambda k: k["enable"] == True, data["data"])
        )
        return context


def pathResolver(path):
    expand_path = os.path.expandvars(path)
    resolved_path = os.path.abspath(expand_path).replace("\\", "/")
    return resolved_path


def searchContext(input, value):
    context = list(
        filter(
            lambda k: k.get("env") == value and k.get("value"),
            input,
        )
    )
    if not context:
        return
    return context[0]


if __name__ == "__main__":
    execute()
