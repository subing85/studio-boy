# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:May:31:Thursday-03:13:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe Command for maya pipe node remapping.

import os
import ast
import logging
import optparse
import subprocess


def execute():
    """
    :description
        studio-pipe Command for maya pipe node remapping.

    :example
        pipe python nodeMapping.py -s "Z:/projects/RAR/assets/raja/Puppet/work/raja1.ma" -c "{'project': 'Ranj and Rani', 'id': '56abf682-88ba-4ab4-83ab-fd733fcec391', 'name': 'rani', 'typed': 'character', 'taskName': 'puppet', 'taskId': '779d13ee-21dc-468d-9ddf-6573ebbd2e4e', 'version': '0.1.0', 'startFrame': None, 'endFrame': None, 'framePerSecond': None, 'assembly': None, 'description': 'test'}"

        \u2022 pipe NodeMapping --source "maya file path" --files dict()
            :param --source <str>
                input parameter of the maya file path.

            :param --context <dict>
                input metadata context.
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe maya pipe node re-mapping commands.",
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
            "-c",
            "--context",
            dest="context",
            action="store",
            type="string",
            help="re-mapping input context dictionary",
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

    if options.example == 1:
        command = "pipe ndRemapping -s \"../Lookdev/work/batman.ma\" -c \"{'project': 'Ranj and Rani', 'id': '56abf682-88ba-4ab4-83ab-fd733fcec391', 'name': 'rani', 'typed': 'character', 'taskName': 'puppet', 'taskId': '779d13ee-21dc-468d-9ddf-6573ebbd2e4e', 'version': '0.1.0', 'startFrame': None, 'endFrame': None, 'framePerSecond': None, 'assembly': None, 'description': 'test'}\""
        print(command)
        return

    if not options.source:
        logging.warning(
            'TypeError: missing 1 required positional argument: "-s or --source"'
        )
        return

    if not options.context:
        logging.warning(
            'TypeError: missing 1 required positional argument: "-c or --context"'
        )
        return

    context = ast.literal_eval(options.context)

    process = subprocess.Popen(
        ["NdMapping", "-s", options.source, "-c", str(context)],
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
    pipe NodeMapping -s "Z:/projects/RAR/assets/boy/Lookdev/work/batman.ma" -c "{'project': 'Ranj and Rani', 'id': '56abf682-88ba-4ab4-83ab-fd733fcec391', 'name': 'rani', 'typed': 'character', 'taskName': 'puppet', 'taskId': '779d13ee-21dc-468d-9ddf-6573ebbd2e4e', 'version': '0.1.0', 'startFrame': None, 'endFrame': None, 'framePerSecond': None, 'assembly': None, 'description': 'test'}"
    """
    execute()
