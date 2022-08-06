# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved
# Author: Subin. Gopi (subing85@gmail.com)
# Studio-Pipe Project Management in-house Tool
# Last modified: 2022:January:03:Monday-07:31:28:PM.
# WARNING! All changes made in this file will be lost!
# Description: studio-pipe help event

import optparse
import importlib


def execute():
    """
    :description
        studio-pipe help commands.
            studio-pipe commands description and examples

    :examples
        \u2022 pipe helps
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe help event",
        version="0.0.1",
    )
    option_list = [
        optparse.make_option(
            "--helps",
            dest="helps",
            action="store_true",
            default=False,
            help=" to display the doc-string of the event library",
        )
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    if options.helps:
        modules = [
            "library.help",
            "library.login",
            "library.project",
            "library.applications",
            "library.steps",
            "library.tasks",
            "library.versions",
            "library.tests",
            "library.event",
            "library.mtRemapping",
        ]
        print("\n")
        for index, each in enumerate(modules):
            module = importlib.import_module(each)
            print("%s. %s" % (index + 1, each))
            print("    :file\n\t%s" % module.__file__)
            print(module.execute.__doc__)

        return


if __name__ == "__main__":
    execute()
