# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:30:Thursday-03:13:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe Command for maya texture remapping.

import os
import ast
import stat
import logging
import optparse


def execute():
    """
    :description
        studio-pipe Command for maya texture re-mapping.
        to re-map the maya texture maps

    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe texture re-mapping commands.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "-s",
            "--source",
            dest="source",
            action="store",
            type="string",
            help="maya scene file path",
        ),
        optparse.make_option(
            "-f",
            "--files",
            dest="files",
            action="store",
            type="string",
            help="files path of the source images",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    if not options.source:
        logging.warning(
            'TypeError: missing 1 required positional argument: "-s or --source"'
        )
        return

    if not options.files:
        logging.warning(
            'TypeError: missing 1 required positional argument: "-f or --files"'
        )
        return

    mayaFilepath = pathResolver(options.source)
    sourceFiles = ast.literal_eval(options.files)

    print("\nstudio-pipe maya texture re-mapping")
    print("\ninput values")
    print("mayaFilepath", mayaFilepath)
    print("sourceFiles", sourceFiles, "\n")

    if not sourceFiles:
        logging.warning("TypeError: invalid files parameter value")
        return

    status = os.stat(mayaFilepath)[0]
    if not status & stat.S_IWRITE:
        filemode = stat.S_IREAD  # read only mode
    else:
        filemode = stat.S_IWRITE  # write mode
    os.chmod(mayaFilepath, stat.S_IWRITE)

    with open(mayaFilepath, "r") as scene:
        data = scene.read()
        for each in sourceFiles:
            source = each[0]
            mode = "absolute"
            if source not in data:
                print(
                    "\tcould not find %s in the scene from absolute mode"
                    % source
                )
                source = hasFromProject(source)
                mode = "relative"
                if not source:
                    print(
                        "\tcould not able to handle with current project"
                    )
                    continue
            if source not in data:
                print(
                    "\tcould not find %s in the scene from relative mode"
                    % source
                )
                continue
            data = data.replace(source, each[1])
            print(
                "\treplace with %s-mode from %s to %s"
                % (mode, source, each[1])
            )
        with open(mayaFilepath, "w") as scene:
            scene.write(data)
        os.chmod(mayaFilepath, filemode)
        print("\nsucceed!..\n")
        return
    print("\nfaild!..\n")


def hasFromProject(directory):
    projectPath = os.getenv("PROJECT-PATH")
    if not directory.startswith(projectPath):
        return None
    paths = directory.split(projectPath)
    if len(paths) != 2:
        return None
    mayaRelativePath = "%s/%s" % (projectPath, paths[-1])
    return mayaRelativePath


def pathResolver(path):
    expand_path = os.path.expandvars(path)
    if not os.path.isabs(expand_path):
        logging.warning("invalid path %s" % path)
        return None
    resolved_path = os.path.abspath(expand_path).replace("\\", "/")
    if not os.path.exists(resolved_path):
        logging.warning("could not find the path %s" % resolved_path)
        return None
    return resolved_path


if __name__ == "__main__":
    execute()
