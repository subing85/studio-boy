# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:03:Monday-05:58:59:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe project task commands.

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe project task commands.
        to create query and edit the tasks in the current check-in project
        make sure to login with your user name and check-in with respective project.

    :example
        \u2022 pipe --get-my-tasks
            get the user assigned tasks.
                :param None

        \u2022 pipe --get-task-dependency "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7"
            get available dependency tasks of the specified task.
                :param <str> task id

        \u2022 pipe --get-task-id "assets.apple.ConceptArt"
            get the task id from the name of the task.
                :param <str> task long name, separated by dots

        \u2022 pipe --start-my-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7"
            set the task status to start mode.
                :param <str> task id

        \u2022 pipe --submit-my-task  "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --versionType "patch" --path "Z:/templates/art" --comment "tests submit"
            submit the user task for review.
                :param <str> task id
                :param --versions <str> "major" or "minor" or "patch"
                :param --path <str> root directory of the source files
                :param --comment <str> submit comments (optional)

        \u2022 pipe --clear-submits "e8b702d4-85a1-4ea1-9df3-e570663eb285"
            delete the all submission from the specified task.
                :param <str> task id

        \u2022 pipe --decline-user-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --versions "0.0.1" --comment "tests decline"
            set the task and submit version status to decline mode.
                :param <str> task id
                :param --versions <str> submit version to decline (optional)
                :param --comment <str> submit comments (optional)

        \u2022 pipe --approved-user-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --comment "tests approved"
        \u2022 pipe --approved-user-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --versions "0.0.1" --comment "tests approved"
            set approve the task submit version (approved mode).
                :param <str> task id
                :param --versions <str> submit version to decline (optional)
                :param --comment <str> submit comments (optional)

        \u2022 pipe --publish-user-task "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7" --versionType "patch" --comment "tests publish"
            publish the approved the task submit version (publish mode).
                :param <str> task id
                :param --versions <str> submit version to decline (optional)
                :param --comment <str> submit comments (optional)

        \u2022 pipe --clear-publishes "1212eb35-bfc9-46ee-ba7e-3bcd4c446af7"
            delete the all publish from the specified task.
                :param <str> task id
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio pipe task event",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--get-my-tasks",
            dest="getMyTasks",
            action="store_true",
            default=False,
            help="get the user assigned tasks.",
        ),
        optparse.make_option(
            "--get-task-dependency",
            dest="getTaskDependency",
            action="store",
            type="string",
            help="get available dependency tasks of the specified task.",
        ),
        optparse.make_option(
            "--get-task-id",
            dest="getTaskId",
            action="store",
            type="string",
            help="get the task id from the name of the task.",
        ),
        optparse.make_option(
            "--start-my-task",
            dest="startMyTask",
            action="store",
            type="string",
            help=" to register my task start data",
        ),
        optparse.make_option(
            "--submit-my-task",
            action="store",
            type="string",
            dest="submitMytask",
            help="submit the user task for review.",
        ),
        optparse.make_option(
            "--clear-submits",
            dest="clearSubmits",
            action="store",
            type="string",
            help="delete the all submission from the specified task.",
        ),
        optparse.make_option(
            "--decline-user-task",
            dest="declineUserTask",
            action="store",
            type="string",
            help="set the task and submit version status to decline mode.",
        ),
        optparse.make_option(
            "--approved-user-task",
            dest="approvedUserTask",
            action="store",
            type="string",
            help="set approve the task and submit version (approved mode).",
        ),
        optparse.make_option(
            "--publish-user-task",
            dest="publishUserTask",
            action="store",
            type="string",
            help=" to publish and register user task",
        ),
        optparse.make_option(
            "--clear-publish",
            dest="clearPublish",
            action="store",
            type="string",
            help="delete the all publish from the specified task.",
        ),
        optparse.make_option(
            "--versionType",
            dest="versionType",
            action="store",
            type="string",
            help="input parameter for submit or publish semantic version type such as Major, Minor, Patch",
        ),
        optparse.make_option(
            "--versions",
            dest="versions",
            action="store",
            type="string",
            help="input parameter for current version",
        ),
        optparse.make_option(
            "--path",
            action="store",
            type="string",
            dest="path",
            help="submit or publish input files directory",
        ),
        optparse.make_option(
            "--kind",
            action="store",
            type="string",
            dest="kind",
            help="input parameter for kind type (submit or publish)",
        ),
        optparse.make_option(
            "--comment",
            action="store",
            type="string",
            dest="comment",
            help="input parameter for comment",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    task = studio.Tasks()
    login = studio.Login()
    stats = studio.Status()

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

    if options.getMyTasks:
        templates = task.getMyTasks()
        return

    if options.getTaskDependency:
        task.getTaskDependency(options.getTaskDependency)
        return

    if options.getTaskId:
        task.getTaskId(options.getTaskId)
        return

    if options.startMyTask:
        task.startMyTask(options.startMyTask)
        return

    if options.submitMytask:
        results = task.releaseKindTask(
            options.submitMytask,
            "submit",
            version=options.versionType,
            path=options.path,
            comments=options.comment,
        )
        return

    if options.clearSubmits:
        results = task.clearTaskKinds(options.clearSubmits, "submit")
        return

    if options.declineUserTask:
        results = task.declineUserTask(
            options.declineUserTask,
            version=options.versions,
            comment=options.comment,
        )
        return

    if options.approvedUserTask:
        results = task.approvedUserTask(
            options.approvedUserTask,
            version=options.versions,
            comment=options.comment,
        )
        return

    if options.publishUserTask:
        results = task.releaseKindTask(
            options.publishUserTask,
            "publish",
            version=options.versionType,
            comment=options.comment,
        )
        return

    if options.clearPublish:
        results = task.clearTaskKinds(options.clearPublish, "publish")
        return


if __name__ == "__main__":
    execute()
