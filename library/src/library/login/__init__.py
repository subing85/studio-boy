# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved
# Author: Subin. Gopi (subing85@gmail.com)
# Studio-Pipe Project Management in-house Tool
# Last modified: 2021:December:30:Thursday-10:42:04:PM.
# WARNING! All changes made in this file will be lost!
# Description: studio-pipe user - login commands

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pipe login commands.
        to query and check-in the user to access the studio-pipe tools
        make sure this user should be added in your ftrack project.

    :examples
        \u2022 pipe --set-username "subingopi"
            check-in with your user account to access studio-pipe tools.
                :param <str> user name

        \u2022 pipe --get-username
            get the current check-in user account.
                :param None

        \u2022 pipe --get-all-users
            get all user from ftrack user register.
                :param None

        \u2022 pipe --login-history
            list out the login history of your current local system.
                :param None
    """

    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pipe user login commands.",
        version="0.0.1",
    )

    option_list = [
        optparse.make_option(
            "--set-username",
            dest="setUsername",
            action="store",
            help="check-in with your user account to access studio-pipe tools.",
        ),
        optparse.make_option(
            "--get-username",
            dest="getUsername",
            action="store_true",
            default=False,
            help="get the current check-in user account.",
        ),
        optparse.make_option(
            "--get-all-users",
            dest="getAllUsers",
            action="store_true",
            default=False,
            help="get all user from ftrack user register.",
        ),
        optparse.make_option(
            "--login-history",
            dest="loginHistory",
            action="store_true",
            default=False,
            help="list out the login history of your current local system.",
        ),
        optparse.make_option(
            "--path",
            dest="path",
            action="store",
            help="input parameter of the path.",
        ),
    ]

    parser.add_options(option_list)
    (options, args) = parser.parse_args()

    login = studio.Login()

    if options.setUsername:
        login.setUsername(options.setUsername)
        return

    if login.isValidLogin():
        if options.getUsername:
            login.getUsername()
            return

        if options.getAllUsers:
            if not login.isSuperUser():
                print("\n")
                LOGGER.warning(
                    "user: %s do not have the privilege to access full control"
                    % login.username
                )
                print("\n")
                return
            login.getAllUsers()
            return
    else:
        print("\n")
        LOGGER.warning(
            'login and try, use this event pipe --set-username "_ _ _"'
        )
        print("\n")
        return

    if options.loginHistory:
        login.loginHistory()
        return


if __name__ == "__main__":
    execute()
