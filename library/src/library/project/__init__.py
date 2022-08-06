# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:31:Friday-09:42:18:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe create, query and check-in - project commands.

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe project commands.
        to create, query and check-in the projects.
        access the studio-pipe tool, make sure to check-in the project first.

    :examples
        \u2022 pipe --create-project "JOK, Jocker" --template "Animation" --icon "Z:/icons/jocker.png"
            to create the new project.
                :param <str> "short name, long name"
                :param --template <str>, Animation or VFX
                :param --icon <str>, icon path (optional)

        \u2022 pipe --delete-project "JOK"
            to delete the project from ftrack.
                :param <str> project short name

        \u2022 pipe --get-all-projects
            get all the available projects.
                :param None

        \u2022 pipe --set-project "MSH"
            to check-in the project.
                :param <str> project short name

        \u2022 pipe --get-project
            get the current check-in project.
                :param None

        \u2022 pipe --get-project-templates
            get the available project templates(schema).
                :param None

        \u2022 pipe --get-project-template
            get current check-in project template (schema).
                :param None

        \u2022 pipe --get-project-categories
            get the current check-in project categories (project children).
                :param None
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe event to create and query the project.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--create-project",
            dest="createProject",
            action="store",
            help="to create the new project.",
        ),
        optparse.make_option(
            "--delete-project",
            dest="deleteProject",
            action="store",
            help="to delete the project from ftrack.",
        ),
        optparse.make_option(
            "--get-all-projects",
            dest="getAllProjects",
            action="store_true",
            default=False,
            help="get all the available projects.",
        ),
        optparse.make_option(
            "--set-project",
            dest="setProject",
            action="store",
            help="to check-in the project.",
        ),
        optparse.make_option(
            "--get-project",
            dest="getProject",
            action="store_true",
            default=False,
            help="get the current check-in project.",
        ),
        optparse.make_option(
            "--get-project-templates",
            dest="getProjectTemplates",
            action="store_true",
            default=False,
            help="get the available project templates(schema).",
        ),
        optparse.make_option(
            "--get-project-template",
            dest="getProjectTemplate",
            action="store_true",
            default=False,
            help="get current check-in project template (schema).",
        ),
        optparse.make_option(
            "--get-project-categories",
            dest="getProjectCategories",
            action="store_true",
            default=False,
            help="get the current check-in project categories (project children).",
        ),
        optparse.make_option(
            "--template",
            dest="template",
            action="store",
            help="input parameter of the template.",
        ),
        optparse.make_option(
            "--icon",
            dest="icon",
            action="store",
            default=None,
            help="input parameter of the icon.",
        ),
        optparse.make_option(
            "--path",
            dest="path",
            action="store",
            help="input parameter of the directory.",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    login = studio.Login()
    projs = studio.Project()
    attr = studio.Attributes()

    if not login.isValidLogin():
        print("\n")
        LOGGER.warning(
            'login and try, use this event pipe --set-username "_ _ _"'
        )
        print("\n")
        return

    privilege_message = None

    if login.isSuperUser():
        if options.createProject:
            name, fullname = [
                each.strip()
                for each in options.createProject.split(",")
            ]
            projs.createNewProject(
                name,
                fullname,
                options.template,
                thumbnail=options.icon,
            )
            attr.createProjectCustomAttributes()
            return
        if options.deleteProject:
            projs.deleteProject(options.deleteProject)
            return
    else:
        privilege_message = (
            "user: %s do not have the privilege to access full control"
            % login.username
        )
        if options.createProject or options.deleteProject:
            print("\n")
            LOGGER.warning(privilege_message)
            print("\n")

    if options.getAllProjects:
        projs.getAllProjects()
        return

    if options.setProject:
        projs.setProject(options.setProject, options.path)
        return

    if options.getProject:
        if privilege_message:
            print("\n")
            LOGGER.warning(privilege_message)
        projs.getProject()
        return

    if options.getProjectTemplates:
        projs.getProjectTemplates()
        return

    if options.getProjectTemplate:
        projs.getProjectTemplate()
        return

    if options.getProjectCategories:
        projs.getProjectCategories()
        return


if __name__ == "__main__":
    execute()
