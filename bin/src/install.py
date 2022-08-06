# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:30:Thursday-03:12:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe install (setup) primary global environments.

import os
import time
import tempfile
import optparse


def execute():
    parser = optparse.OptionParser(
        usage="usage: %prog\n\trun with out any parameter\
            setup the primary global environments",
        version="studio-pipe-install 0.0.1",
    )
    option_list = []
    parser.add_options(option_list)
    (options, args) = parser.parse_args()
    setHeader()
    contexts = getContext()
    install(contexts)
    findContexts(contexts=contexts)
    time.sleep(3)
    print("# install completed!...")


def setHeader():
    headers = [
        "Studio-Pipe installation",
        "Version : 0.0.1 Release.",
        "Last modified : 2021:December:30:Thursday-03:08:52:PM",
        "Author : Subin. Gopi (subing85@gmail.com)",
        "Description : setup the primary global environments",
        "Copyright (c) 2021, subing85@gmail.com All rights reserved.",
        "https://www.subins-toolkits.com",
    ]
    print("#" * 60)
    for header in headers:
        print(header)
    print("#" * 60)


def getContext():
    contexts = [
        {"name": "Project Directory", "env": "PROJECT-DIRNAME"},
        {"name": "Devkit Path", "env": "DEVKIT-PATH"},
    ]
    return contexts


def install(contexts):
    for each in contexts:
        override = "yes"
        if os.getenv(each["env"]):
            title = "\n{} {} \n\t{}".format(
                "Already setup up the",
                each["name"],
                'If you want to override press "yes" either "no"',
            )
            override = input(title)
        if override.lower() not in ["yes", "no"]:
            raise Exception("invalid input called <%s>" % override)
        if override.lower() == "yes":
            value = input("Enter the %s : " % each["name"])
            if not value:
                raise Exception("invalid input called <null>")
        else:
            value = os.getenv(each["env"])
        if not os.path.isabs(value):
            raise Exception(
                "invalid input called <%s>, should be directory"
                % value
            )
        each["value"] = os.path.abspath(value).replace("\\", "/")
    batch_file = create_batch(contexts)
    os.system("call %s" % batch_file)
    return True


def create_batch(context):
    batch_file = tempfile.mktemp(".bat", "pipe-install-env-")
    commands = []
    for each in context:
        command = "SETX %s %s" % (each["env"], each["value"])
        commands.append(command)
    with open(batch_file, "w") as file:
        file.write("\n".join(commands))
        return batch_file
    return None


def findContexts(contexts=None):
    contexts = contexts or getContext()
    print("\n\t<Global Environments>")
    for context in contexts:
        print(context["env"].rjust(25), ":", context["value"])
    print("\n")


if __name__ == "__main__":
    execute()
