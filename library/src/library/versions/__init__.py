# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:03:Monday-07:04:23:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe project task version commands.

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe project task version commands.
        task version download from the current check-in project.
        make sure to login with your user name and check-in with respective project.

    :example
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --submit --versions "0.0.1"
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --publish --versions "0.0.1"
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --submit
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --publish
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --versions "0.0.1"
        \u2022 pipe --download-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7"
            download and deploy the version from specific task level.
                :param <str> task id
                :param --submit or --publish <bool>
                :param --versions <str> task version

        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965" --submit --versions "0.0.1"
        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965" --publish --versions "0.0.1"
        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965" --submit
        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965" --publish
        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965" --versions "0.0.1"
        \u2022 pipe --download-step "02deb816-3d1d-4fd6-be67-4eeffe25d965"
            download and deploy the versions from specific step level.
                :param <str> step id
                :param --submit or --publish <bool>
                :param --versions <str> task version

        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596" --submit --versions "0.0.1"
        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596" --publish --versions "0.0.1"
        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596" --submit
        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596" --publish
        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596" --versions "0.0.1"
        \u2022 pipe --download-category "f4f2db60-de1b-4c75-9647-c05dfd05a596"
            download and deploy the versions from specific category level.
                :param <str> category id
                :param --submit or --publish <bool>
                :param --versions <str> task version

        \u2022 pipe --download-all --submit --versions "0.0.1"
        \u2022 pipe --download-all --publish --versions "0.0.1"
        \u2022 pipe --download-all --submit
        \u2022 pipe --download-all --publish
        \u2022 pipe --download-all --versions "0.0.1"
        \u2022 pipe --download-all
            download and deploy the versions from specific category level.
                :param <bool>
                :param --submit or --publish <bool>
                :param --versions <str> task version
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio pipe versions event",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--download-task",
            dest="downloadTask",
            action="store",
            type="string",
            help="download and deploy the version from specific task level.",
        ),
        optparse.make_option(
            "--download-step",
            dest="downloadStep",
            action="store",
            type="string",
            help="download and deploy the versions from specific step level.",
        ),
        optparse.make_option(
            "--download-category",
            dest="downloadCategory",
            action="store",
            type="string",
            help="to download specific task form the current project",
        ),
        optparse.make_option(
            "--download-all",
            dest="downloadAll",
            action="store_true",
            default=False,
            help="to download specific task form the current project",
        ),
        optparse.make_option(
            "--submit",
            dest="submit",
            action="store_true",
            default=False,
            help="input parameter for kind type submit",
        ),
        optparse.make_option(
            "--publish",
            dest="publish",
            action="store_true",
            default=False,
            help="input parameter for kind type publish",
        ),
        optparse.make_option(
            "--versions",
            dest="versions",
            action="store",
            type="string",
            help="submit or publish semantic version type such as Major, Minor, Patch",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    login = studio.Login()
    stats = studio.Status()
    vers = studio.Versions()
    proj = studio.Project()

    if not login.isValidLogin():
        print("\n")
        LOGGER.warning(
            'login and try, use this event pipe --set-username "_ _ _"'
        )
        print("\n")
        return

    if not stats.isInProject():
        print("\n")
        LOGGER.warning(
            'not check-in the project, use this event pipe --set-project "_ _ _"'
        )
        print("\n")
        return

    kind = None
    if options.publish:
        kind = "publish"
    if options.submit:
        kind = "submit"

    if options.downloadTask:
        components = vers.downloadVersions(
            taskid=options.downloadTask,
            kind=kind,
            versions=options.versions,
            progressbar=None,
        )
        return

    if options.downloadStep:
        components = vers.downloadVersions(
            stepid=options.downloadStep,
            kind=kind,
            versions=options.versions,
            progressbar=None,
        )
        return

    if options.downloadCategory:
        proj.authorization()
        category = proj.findCategory(options.downloadCategory)
        components = vers.downloadVersions(
            categoryid=category["id"],
            kind=kind,
            versions=options.versions,
            progressbar=None,
        )
        return

    if options.downloadAll:
        components = vers.downloadVersions(
            kind=kind, versions=options.versions, progressbar=None
        )
        return


if __name__ == "__main__":
    execute()
