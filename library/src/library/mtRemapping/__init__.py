# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:30:Thursday-03:13:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe Command for maya texture remapping.

import os
import ast
import logging
import optparse
import subprocess


def execute():
    """
    :description
        studio-pipe Command for maya texture re-mapping.
        to re-map the maya texture source files

    :examples

        \u2022 pipe MtRemapping --source "maya file path" --files [""]
            :param --source <str>
                input parameter of the maya file path.

            :param --files <list>
                input parameter of the source-images file path.
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
        optparse.make_option(
            "--e",
            "--example",
            dest="example",
            action="store_true",
            default=False,
            help="example of command and parameters.",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    if options.example:
        command = "pipe remapping -s \"../Lookdev/work/batman.ma\" -f \"[['../lookdev/normal/sourceimages/suite.png', 'sourceimages/suite.png']]\""
        print(command)
        return

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

    sourceFiles = ast.literal_eval(options.files)

    process = subprocess.Popen(
        ["MtRemapping", "-s", options.source, "-f", str(sourceFiles)],
        shell=True,
        stdout=subprocess.PIPE,
    )
    process.wait()
    result = process.stdout.readlines()
    communicate = process.communicate()

    for each in result:
        print(each.decode("utf-8").replace("\r\n", ""))


if __name__ == "__main__":
    """
    pipe MtRemapping -s "Z:/projects/RAR/assets/boy/Lookdev/work/batman.ma" -f "[['Z:/templates/batman/lookdev/normal/sourceimages/suite.png', 'sourceimages/suite.png'], ['Z:/templates/batman/lookdev/normal/sourceimages/body.png', 'sourceimages/body.png'], ['Z:/templates/batman/lookdev/normal/sourceimages/face.png', 'sourceimages/face.png'], ['Z:/templates/batman/lookdev/normal/sourceimages/eye.png', 'sourceimages/face.png'], ['Z:/templates/batman/lookdev/normal/sourceimages/tongue.png', 'sourceimages/face.png'], ['Z:/templates/batman/lookdev/normal/sourceimages/belt.png', 'sourceimages/face.png']]"
    """
    execute()
