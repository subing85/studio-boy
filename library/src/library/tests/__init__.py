# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved
# Author: Subin. Gopi (subing85@gmail.com)
# Studio-Pipe Project Management in-house Tool
# Last modified: 2022:January:03:Monday-07:32:07:PM.
# WARNING! All changes made in this file will be lost!
# Description: studio-pipe source code test event

import os
import optparse

from pipe import utils
from test import core
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe test commands.
        test the studio-pipe source codes.

    :examples
        \u2022 pipe unittest
            source code unit-test.
                :param None

        \u2022 pipe unittest --get-package-modules "pipe"
            get the specific package modules.
                :param all

        \u2022 pipe unittest --check
            check the pipe env packages.
                :param None

        \u2022 pipe unittest --get-package-modules all
            get the all package modules.
                :param all

        \u2022 pipe black-check
            check the source code with black formatter.
                :param <str or None> file path or None

        \u2022 pipe black-fix
            fix the source code with black formatter.
                :param <str or None> file path or None

        \u2022 pipe unused-check
            check the source code with unused imports and variables.
                :param <str or None> file path or None

        \u2022 pipe unused-fix
            fix the source code with unused imports and variables.
                :param <str or None> file path or None

        \u2022 pipe clean
            remove pyc and cahche files.
                :param None
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe unit test event",
        version="0.0.1",
    )
    option_list = [
        optparse.make_option(
            "--unittest",
            dest="unitTest",
            action="store_true",
            default=False,
            help="to test the all packages",
        ),
        optparse.make_option(
            "--unused",
            dest="unused",
            action="store",
            type="string",
            help="to check the unused imports and variables",
        ),
        optparse.make_option(
            "--get-package-modules",
            dest="getPackModule",
            action="store",
            type="string",
            help="to get the module from specific package",
        ),
        optparse.make_option(
            "--check",
            dest="check",
            action="store_true",
            default=False,
            help="to test the all packages",
        ),
        optparse.make_option(
            "--fix",
            dest="fix",
            action="store_true",
            default=False,
            help="to test the all packages",
        ),
        optparse.make_option(
            "--clean",
            dest="clean",
            action="store_true",
            default=False,
            help="to test the all packages",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    unit = core.UnitTest()

    if options.unitTest:
        if options.getPackModule:
            unit.getPackageModles(options.getPackModule)
        if options.check:
            unit.check()
        else:
            unit.execute()

    if options.unused:
        if options.unused == "packages":
            modules = None
        else:
            filepath = utils.setPathResolver(options.unused)
            if os.path.isdir(filepath):
                modules = unit.searchModules(filepath)
            elif os.path.isfile(filepath):
                modules = [filepath]
            else:
                LOGGER.error(
                    "FileNotFoundError: system cannot find the path specified: %s"
                    % filepath
                )
                return
        if options.check:
            unit.checkUnusedImport(modules=modules)

        if options.fix:
            unit.fixUnusedImport(modules=modules)

    if options.clean:
        unit.cleanDevkit()
        return


if __name__ == "__main__":
    execute()
