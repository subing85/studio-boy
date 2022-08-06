import os
import json
import shutil
from datetime import datetime

CURRENT_PATH = os.path.dirname(__file__)


def getPackages():
    contexts = getPackageContext()
    if not contexts:
        print("warning: not found any packages")
        return
    for each in contexts:
        path = os.path.join(CURRENT_PATH, each["name"], "src")
        path = os.path.abspath(path).replace("\\", "/")
        each["path"] = path
    return contexts


def getPackageContext():
    config_path = os.path.join(CURRENT_PATH, "config.json")
    if not os.path.isfile(config_path):
        raise IOError("not found path <%s>" % config_path)
    with open(config_path, "r") as file:
        contexts = json.load(file)
        if not contexts.get("enable"):
            return None
        return contexts.get("data")


def backup(source, target):
    for dir, folder, files in os.walk(source):
        target_dir = dir.replace(source, target)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        for file in files:
            source_file = os.path.join(dir, file)
            target_file = os.path.join(target_dir, file)
            print("\n\t", source_file)
            print("\t", target_file)
            shutil.copy2(source_file, target_file)


def backupFiles(source, target):
    if not os.path.isdir(target):
        os.mkdir(target)
    for each in os.listdir(source):
        source_file = os.path.join(source, each)
        if not os.path.isfile(source_file):
            continue
        target_file = os.path.join(target, each)
        print("\n\t", source_file)
        print("\t", target_file)
        shutil.copy2(source_file, target_file)


def create():
    backup_dirname = os.path.join(
        os.path.dirname(CURRENT_PATH),
        "backup",
        datetime.now().strftime("%Y-%m(%B)%d-%A-%I-%M-%S-%p"),
    )
    print(backup_dirname)
    packages = getPackages()
    for each in packages:
        print("\n", each["path"])
        backup(each["path"], backup_dirname)

    bin_path = os.path.join(CURRENT_PATH, "bin")
    bin_backup_dirname = os.path.join(backup_dirname, "bin")
    print("\n", bin_path)
    backup(bin_path, bin_backup_dirname)
    print("\n", CURRENT_PATH)
    backupFiles(CURRENT_PATH, backup_dirname)
    print("\nBackup", backup_dirname)
    print("Done!...............")


if __name__ == "__main__":
    create()
