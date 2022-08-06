# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-05:15:04:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe generic utility functions.

import os
import ast
import stat
import copy
import glob
import arrow
import shutil
import getpass
import pkgutil
import platform
import tempfile
import binascii
import importlib
import distutils
import webbrowser

from pipe import resources


def executePythonCommands(command):
    result = None
    exec(command)
    return result


def executeCommand(command):
    try:
        os.system(command)
    except Exception as error:
        raise OSError(str(error))


def findOperatingSystem():
    operating_system = "%s-%s" % (
        platform.system(),
        platform.architecture()[0],
    )
    return operating_system


def findDatetime():
    date_time = resources.getDateTime()
    return date_time


def findUser():
    current_user = getpass.getuser()
    return current_user


def findFileFormat(filepath):
    splitext = os.path.splitext(filepath)
    if not splitext[1]:
        return None
    return splitext[1]


def findFileNameAndFormat(filepath):
    filename, format = os.path.splitext(os.path.basename(filepath))
    return filename, format


def formatsToQFormats(formats):
    formats = "(*" + " *".join(formats) + ")"
    return formats


def collectSpecificFiles(directory, formats=None):
    valid_files = []
    if formats:
        for format in formats:
            files = glob.glob("%s/*%s" % (directory, format))
            valid_files.extend(files)
    else:
        valid_files = glob.glob("%s/*.*" % (directory))
    specific_files = []
    for each in valid_files:
        specific_files.append(setPathResolver(each))
    return specific_files


def setPathResolver(path, folders=[], suffix=None):
    expand_path = os.path.expandvars(path)
    if folders:
        expand_path = os.path.join(expand_path, *folders)

    if suffix:
        expand_path = os.path.join(expand_path, suffix)

    if not os.path.isabs(expand_path):
        return path
    resolved_path = os.path.abspath(expand_path).replace("\\", "/")
    return resolved_path


def setPathsResolver(paths):
    resolved_paths = []
    for path in paths:
        resolved_path = setPathResolver(path)
        if resolved_path in resolved_paths:
            continue
        resolved_paths.append(resolved_path)
    # resolved_paths = list(set(resolved_paths))
    return resolved_paths


def updateInputValue(contexts, env, value, enable=True):
    contents = list(filter(lambda k: k["env"] == env, contexts))
    if not contents:
        return
    result = copy.deepcopy(contents[0])
    result["value"] = value
    result["enable"] = enable
    return result


def getFileFormat(filepath):
    if not os.path.isabs(filepath):
        raise ValueError("invalid filepath")
    splitext = os.path.splitext(filepath)
    return splitext[-1]


def getFileName(filepath):
    if not os.path.isabs(filepath):
        raise ValueError("invalid filepath")
    name = os.path.splitext(os.path.basename(filepath))[0]
    return name


def findThumbnail(thumbnail, typed):
    if not thumbnail:
        thumbnail = setPathResolver(
            resources.getIconPath(),
            folders=["unknown-%s.png" % typed],
        )
        return thumbnail
    if os.path.isabs(thumbnail):
        if os.path.isfile(thumbnail):
            return thumbnail
    thumbnail = setPathResolver(
        resources.getIconPath(), folders=["unknown-%s.png" % typed]
    )
    return thumbnail


def findIconpath(prefix=None, suffix=None):
    if not prefix:
        iconpath = os.path.join(
            resources.getIconPath(), "unknown.png"
        )
        return iconpath
    if suffix:
        iconpath = os.path.join(
            resources.getIconPath(), "%s-%s.png" % (prefix, suffix)
        )
    else:
        iconpath = os.path.join(
            resources.getIconPath(), "%s.png" % prefix
        )
    if not os.path.isfile(iconpath):
        iconpath = os.path.join(
            resources.getIconPath(), "unknown.png"
        )
    return iconpath


def createBatch(contexts, path):
    if os.path.isfile(path):
        try:
            os.chmod(self.db, stat.S_IWRITE)
            os.remove(path)
        except Exception:
            pass
    commands = ["@echo off"]
    commands = []
    for each in contexts:
        command = "set %s=%s" % (each["env"], each["value"])
        os.environ[each["env"]] = each["value"]
        commands.append(command)
    with open(path, "w") as file:
        file.write("\n".join(commands))
        return path
    return None


def setEnvironment(inputs, insert=False):
    for each in inputs:
        if not each.get("enable"):
            continue
        if isinstance(each.get("value"), list):
            values = [
                each for each in each["value"] if each is not None
            ]
            if not os.getenv(each["env"]):
                paths = os.pathsep.join(values)
            else:
                values = []
                for x in each["value"]:
                    if x is None:
                        continue
                    if x in os.getenv(each["env"]):
                        continue
                    values.append(x)
                paths = os.pathsep + os.pathsep.join(values)
                paths = os.getenv(each["env"]) + paths
            os.environ[each["env"]] = paths
        else:
            if not each.get("value"):
                continue
            os.environ[each["env"]] = each["value"]


def setWinEnvironment(batch_file, inputs, insert=True):
    environments = []
    for each in inputs:
        if not each.get("enable"):
            continue
        if isinstance(each.get("value"), str):
            paths = [each["value"]]
        else:
            paths = each["value"]
        key = each.get("env")
        _paths = paths
        if insert:
            if os.getenv(key):
                exists_paths = os.getenv(key).split(os.pathsep)
                _paths.extend(exists_paths)
        _paths = list(set(_paths))
        environment = "set %s=%s" % (key, os.pathsep.join(_paths))
        environments.append(environment)
    with open(batch_file, "w") as file:
        file.write("\n".join(environments))
        return batch_file
    return False


def removeEnvValues(env, values):
    if not os.getenv(env):
        return
    extrude_envs = []
    for each in os.getenv(env).split(";"):
        if each in values:
            continue
        extrude_envs.append(each)
    os.environ[env] = os.pathsep.join(extrude_envs)
    return extrude_envs


def removeTempEnv(env):
    if not os.getenv("OVERRIDE-PIPE-ENV"):
        return
    values = os.getenv("OVERRIDE-PIPE-ENV").split(";")
    extrude_envs = removeEnvValues(env, values)
    return extrude_envs


def appendEnvValues(env, values):
    if not os.getenv(env):
        return
    current_values = os.getenv(env).split(";")
    extrude_value = []
    for each in values:
        if each in current_values:
            continue
        extrude_value.append(each)
    paths = os.pathsep + os.pathsep.join(extrude_value)
    os.environ[env] = os.getenv(env) + paths
    return extrude_value


def packages():
    packages = []
    if not os.getenv("PACKAGES"):
        return packages
    packages = os.getenv("PACKAGES").split(os.pathsep)
    return packages


def getPackages():
    context = []
    for each in packages():
        module = importlib.import_module(each)
        if not hasattr(module, "ENABLE"):
            continue
        context.append(module)
    return context


# =====================================================================
# def getPackages(root_path):
#     packages = []
#     for module_loader, name, ispkg in pkgutil.iter_modules([root_path]):
#         loader = module_loader.find_module(name)
#         module = loader.load_module(name)
#         if not hasattr(module, "ENABLE"):
#             continue
#         if not module.ENABLE:
#             continue
#         current_order = 0
#         if hasattr(module, "ORDER"):
#             current_order = module.ORDER
#         packages.append(module)
#     return packages
# =====================================================================


def detetePath(directory):
    os.chmod(directory, stat.S_IWRITE)
    for dir, folder, files in os.walk(directory):
        os.chmod(dir, stat.S_IWRITE)
        for file in files:
            filepath = setPathResolver(dir, folders=[file])
            os.chmod(filepath, stat.S_IWRITE)
            os.remove(filepath)
            print("\tremoved  exists file, %s" % filepath)
    shutil.rmtree(directory)


def deleteFiles(files):
    if isinstance(files, str):
        files = [files]
    for each in files:
        if os.path.isdir(each):
            try:
                shutil.rmtree(each)
            except Exception as error:
                pass
        if os.path.isfile(each):
            try:
                os.remove(each)
            except Exception as error:
                pass


def deleteFile(filepath):
    filepath = setPathResolver(filepath)
    if not os.path.isfile(filepath):
        return
    try:
        os.chmod(filepath, stat.S_IWRITE)
        valid = True
    except Exception as error:
        valid = False
    try:
        os.remove(filepath)
        valid = True
    except Exception as error:
        valid = False
    if valid:
        print("\tremoved  exists file, %s" % filepath)
    return valid


def setReadonly(directory):
    for dir, folder, files in os.walk(directory):
        os.chmod(dir, stat.S_IWRITE)
        for file in files:
            filepath = os.path.join(dir, file)
            os.chmod(filepath, stat.S_IREAD)
        os.chmod(dir, stat.S_IREAD)


def searchContext(input, key, value=None, first=False):
    if value:
        contexts = list(
            filter(
                lambda k: k.get(key) == value,
                input,
            )
        )
    else:
        contexts = list(
            filter(
                lambda k: k.get(key),
                input,
            )
        )
    if contexts and first:
        return contexts[0]
    return contexts


def searchConetxValues(key, context):
    values = list(map(lambda k: k.get(key), context))
    return values


def specialSearchContext(input, key, value=None, default=False):
    contexts = searchContext(input, key, value=value)
    if contexts:
        return contexts[0]
    context = contexts[0] if contexts else {key: default}
    return context


def encodeBinascii(input, size=40):
    input = bytes(str(input), "utf-8")
    code = binascii.b2a_hex(input).decode("utf-8")
    return code[0:size]


def _getFieldValue(context, filed, strDict=False):
    fields = filed.split(".")
    current = context
    for filed in fields:
        current = current.get(filed)
        if not current:
            return None
        if strDict and isinstance(current, str):
            current = ast.literal_eval(current)
    return current


def getContextFieldValue(context, filedlist):
    pass


def getFieldValue(context, filedlist, fieldchild=None):
    stack = filedlist.copy()
    stack.reverse()
    current = context
    while stack:
        child = stack.pop()
        if not current:
            current = None
            continue
        if child not in current:
            current = None
            continue
        current = current[child]
    if current:
        if fieldchild:
            if fieldchild in current:
                try:
                    current = ast.literal_eval(current)
                except Exception:
                    current = current
                if isinstance(current, dict):
                    current = current.get(fieldchild)
                else:
                    current = None
            else:
                current = None
        else:
            if isinstance(current, str):
                current = current
            elif isinstance(current, float):
                current = current
            elif isinstance(current, int):
                current = current
            elif isinstance(current, dict):
                current = current
            elif isinstance(current, list):
                current = current
            elif isinstance(current, arrow.Arrow):
                current = resources.getDateTimes(context=current)
            else:
                current = None
    else:
        current = None
    return current


def sortedVersions(versions, reverse=True):
    versionList = sorted(
        versions, key=distutils.version.StrictVersion, reverse=reverse
    )
    # sorted_versions.reverse()
    return versionList


def openLink(link):
    webbrowser.open(link)


def abc():
    fruit = "Apple"
    isApple = True if fruit == "Apple" else False


if __name__ == "__main__":
    pass
