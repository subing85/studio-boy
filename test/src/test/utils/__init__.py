import os
import sys
import types
import shutil
import pkgutil
import importlib
import subprocess

from pipe import utils
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def setPathResolver(path, folders=[]):
    resolved_path = utils.setPathResolver(path, folders=folders)
    return resolved_path


def pipelinePath():
    path = setPathResolver(os.getenv("PIPELINE-PATH"))
    return path


def hasPackage():
    if not os.getenv("PACKAGES"):
        LOGGER.error("could not find PACKAGES env value")
        return False
    if not os.getenv("PIPELINE-PATH"):
        LOGGER.error("could not find PIPELINE-PATH env value")
        return False
    return True


def getPackages():
    if not os.getenv("PACKAGES"):
        LOGGER.error("could not find PACKAGES env value")
        return False
    packages = os.getenv("PACKAGES").split(os.pathsep)
    return packages


def pypath():
    return os.path.expandvars("%PYTHON-EXE%")


def searchModules(dirname):
    modules = []
    for dir, folder, files in os.walk(dirname):
        for file in files:
            if not file.endswith(".py"):
                continue
            directory = setPathResolver(dir, folders=[file])
            modules.append(directory)
    return modules


def collectPackageModules(package):
    print("\npackage name: %s" % package)
    dirname = getPackageDirname(package)
    root = setPathResolver(pipelinePath(), [dirname, "src"])
    for dir, folder, files in os.walk(dirname):
        for file in files:
            current_file = setPathResolver(dir, [file])
            if not file.endswith(".py"):
                continue
            current_module = current_file.rsplit(root, 1)[-1]
            current_module = os.path.splitext(current_module)[
                0
            ].split("/")
            print('\t"%s"' % ".".join(current_module[1:]))


def getModuleFromName(package):
    try:
        module = importlib.import_module(package)
    except Exception as error:
        LOGGER.error("ModuleNotFoundError: %s" % error)
        module = None
    return module


def getPackageDirname(package):
    module = getModuleFromName(package)
    if not module:
        print("\tcould not found valid %s module" % package)
        return
    dirname = os.path.dirname(module.__file__)
    dirname = setPathResolver(dirname)
    return dirname


def loadDirectory(directory, verbose=True):
    if verbose:
        print("\t", directory)
    modules = []
    for module_loader, name, ispkg in pkgutil.iter_modules(
        [directory]
    ):
        loader = module_loader.find_module(name)
        module = loader.load_module(name)
        if verbose:
            print("\t\t", module)
        modules.append(module)
    return modules


def checkModules(verbose=True):
    if verbose:
        print(
            "\n##### Header: General module check ######################\n"
        )
    modules = []
    packages = getPackages()
    for index, each in enumerate(packages):
        dirname = getPackageDirname(each)
        if not dirname:
            continue
        if not os.path.isdir(dirname):
            continue
        for dir, folder, files in os.walk(dirname):
            if ".git" in dir:
                continue
            if "__pycache__" in dir:
                continue
            directory = utils.setPathResolver(dir)
            module = loadDirectory(directory, verbose=verbose)
            modules.extend(module)
    print("\n")
    return modules


def checkPackages():
    print(
        "\n##### Header: Package module check ######################\n"
    )
    if not hasPackage():
        return
    packages = getPackages()
    for index, each in enumerate(packages):
        if each not in ["pipe"]:
            continue
        module = getModuleFromName(each)
        if not module:
            continue
        if not hasattr(module, "REPOSITORY"):
            LOGGER.error(
                "%s. does not register REPOSITORY value, %s"
                % (index + 1, module.__package__)
            )
            continue
        if hasattr(module, "BYPASS"):
            if module.BYPASS:
                LOGGER.info(
                    "bypass the module called %s" % module.__package__
                )
                continue
        print("\t%s" % module)
        if sys.version_info[:2] >= (3, 4):
            importlib.reload(module)
        else:
            reload(module)

        if not hasattr(module, "RELOAD"):
            LOGGER.error(
                "%s. does not register RELOAD function, %s"
                % (index + 1, module.__package__)
            )
            continue
        invalid = module.RELOAD()
        if invalid:
            message = "success"
        else:
            message = (
                "reload error found in package [%s] sub modules"
                % (module.__name__)
            )
        print("\t%s" % message)
        print("\n")


def checkUnusedImport(modules=None):
    print(
        "\n##### Header: Unused imports and variables check ######################\n"
    )
    if not modules:
        modules = checkModules()
    for module in modules:
        if isinstance(module, types.ModuleType):
            filepath = setPathResolver(module.__file__)
        else:
            filepath = setPathResolver(module)
        process = subprocess.Popen(
            [pypath(), "-m", "autoflake", filepath],
            shell=False,
            stdout=None,
            stderr=None,
        )
        process.wait()
        communicate = process.communicate()
        result = process.returncode
    print("\n")


def checkBlackFormatting(module=None):
    print(
        "\n##### Header: Black formatter check ######################\n"
    )
    if not module:
        filepath = pypath()
    elif isinstance(module, types.ModuleType):
        filepath = setPathResolver(module.__file__)
    else:
        filepath = setPathResolver(module)
    print("filepath", filepath)
    process = subprocess.Popen(
        [pypath(), "-m", "black", "--check", filepath],
        shell=False,
        stdout=None,
        stderr=None,
    )
    process.wait()
    communicate = process.communicate()
    result = process.returncode
    print("\n")


def fixUnusedImport(modules=None):
    print(
        "\n##### Header: Unused imports and variables fix ######################\n"
    )
    if not modules:
        modules = checkModules()

    for module in modules:
        if isinstance(module, types.ModuleType):
            filepath = utils.setPathResolver(module.__file__)
        else:
            filepath = utils.setPathResolver(module)
        process = subprocess.Popen(
            [
                pypath(),
                "-m",
                "autoflake",
                "--in-place",
                "--remove-unused-variables",
                "--remove-all-unused-imports",
                filepath,
            ],
            shell=False,
            stdout=None,
            stderr=None,
        )
        process.wait()
        communicate = process.communicate()
        result = process.returncode
        print("\tremoved unused imports and variables, %s" % filepath)

    print("\n")


def cleanDevkit():
    print(
        "\n##### Header: Clean devkit packages ######################\n"
    )
    for dir, folder, files in os.walk(pypath()):
        for file in files:
            if not file.endswith(".pyc"):
                continue
            pyc = os.path.join(dir, file)
            os.remove(pyc)
            print("removed %s" % pyc)
        if dir.endswith("__pycache__"):
            shutil.rmtree(dir)
            print("removed %s" % dir)
    print("\n")


if __name__ == "__main__":
    abc = collectPackageModules("pipe")
    print(abc)
