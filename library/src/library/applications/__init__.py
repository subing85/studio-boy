# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:01:Saturday-03:22:21:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe applications launch commands.

import optparse

from apis import studio
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    """
    :description
        studio-pop application commands. To set the environments and launch application.
     
    :examples
        \u2022 pipe --get-apps    
            get the available applications under the configure
                :param None
                
    
    """
    
    parser = optparse.OptionParser(
        usage="usage: %prog [options] studio-pop application launch commands.",
        version="0.0.1",
    )
 
    option_list = [
        optparse.make_option(
            "--get-apps",
            dest="getApplications",
            action="store_true",
            default=False,
            help="get all studio-pop configure applications.",
        ),
    ] 
    
    if options.getApplications:
        appls.getApplications()
        return     
    
    
    
#===============================================================================

#     :examples
#         \u2022 pipe --get-apps
#             get the available applications under the configure
#                 :param None
# 
#         \u2022 pipe --set-envs "maya2018"
#                 :param <str>, name of the application
# 
#         \u2022 pipe --get-app-envs
#             to get the application environments.
# 
#         \u2022 pipe launch "login"
#             to launch the login application.
# 
#         \u2022 pipe launch "project"
#             to launch the create project application.
# 
#         \u2022 pipe launch "tasks"
#             to launch the create project tasks application.
# 
#         \u2022 pipe launch "launcher"
#             to launch the launcher application.
# 
#         \u2022 pipe launch "maya2018"
#             to launch the specific application.
# 
#         \u2022 pipe python "Z:/devkit/pipeline/example/launchMaya.py"
#             to call python command.
# 
#     """
# 
#     parser = optparse.OptionParser(
#         usage="usage: %prog [options] studio-pipe application launch commands.",
#         version="0.0.1",
#     )
# 
#     option_list = [
#         optparse.make_option(
#             "--get-apps",
#             dest="getApplications",
#             action="store_true",
#             default=False,
#             help="get all studio-pipe configure applications.",
#         ),
#         optparse.make_option(
#             "--set-envs",
#             dest="setEnvironments",
#             action="store",
#             help="to set the environments from application configure.",
#         ),
#         optparse.make_option(
#             "--get-app-envs",
#             dest="getEnvironments",
#             action="store_true",
#             default=False,
#             help="to get the set environments from application configure.",
#         ),
#         optparse.make_option(
#             "--launch",
#             dest="launch",
#             action="store",
#             help="to launch specific studio-pipe application.",
#         ),
#         optparse.make_option(
#             "--path",
#             dest="path",
#             action="store",
#             help="input parameter of the directory.",
#         ),
#     ]
# 
#     parser.add_options(option_list)
#     (options, args) = parser.parse_args()
# 
#     login = studio.Login()
#     appls = studio.Applications()
# 
#     if not login.isValidLogin():
#         print("\n")
#         LOGGER.warning(
#             'login and try, use this event pipe --set-username "_ _ _"'
#         )
#         print("\n")
#         return
# 
#     if options.getApplications:
#         appls.getApplications()
#         return
# 
#     if options.setEnvironments:
#         appls.setEnvironments(
#             options.setEnvironments, path=options.path
#         )
#         return
# 
#     if options.getEnvironments:
#         appls.getEnvironments()
#         return
# 
#     if options.launch:
#         appls.startLaunch(options.launch)
#         return
#===============================================================================


if __name__ == "__main__":
    execute()
