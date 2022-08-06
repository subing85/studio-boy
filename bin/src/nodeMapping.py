# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:May:31:Thursday-03:13:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe Command for maya pipe node remapping.

import os
import ast
import stat
import logging
import optparse


def execute():
    """
    :description
        studio-pipe Command for maya pipe node remapping.

    :example
        pipe python nodeMapping.py -s "Z:/projects/RAR/assets/raja/Puppet/work/raja1.ma" -c "{'project': 'Ranj and Rani', 'id': '56abf682-88ba-4ab4-83ab-fd733fcec391', 'name': 'rani', 'typed': 'character', 'taskName': 'puppet', 'taskId': '779d13ee-21dc-468d-9ddf-6573ebbd2e4e', 'version': '0.1.0', 'startFrame': None, 'endFrame': None, 'framePerSecond': None, 'assembly': None, 'description': 'test'}"
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
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

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

    mayaFilepath = pathResolver(options.source)
    context = ast.literal_eval(options.context)

    print("\nstudio-pipemaya pipe node re-mapping")
    print("\ninput values")
    print("mayaFilepath", mayaFilepath)
    print("context", context, "\n")

    print("context", type(context))
    if not isinstance(context, dict):
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
        fromScene = None
        fromInput = None

        for each in data.split(";"):
            for line in metadataContext():
                if line not in each:
                    continue
                fromScene = each.strip()
                fromInput = line
                break
        if not fromScene:
            logging.warning(
                '\tcould not find "metadata" attribute from the scene'
            )
            return

        newLine = '%s "%s"' % (fromInput, str(context))
        data = data.replace(fromScene, newLine)

        with open(mayaFilepath, "w") as scene:
            scene.write(data)
        os.chmod(mayaFilepath, filemode)
        print("\nsucceed!..\n")
        return

    print("\nfaild!..\n")


def metadataContext():
    context = [
        'setAttr ".md" -type "string"',
        'setAttr -l on ".md" -type "string"',
    ]

    return context


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
