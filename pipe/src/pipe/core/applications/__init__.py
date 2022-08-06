# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:47:39:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core application launcher.

import os
import copy
import threading
import subprocess

from pipe import utils
from pipe.core import logger
from pipe.core import inputs

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Connect(inputs.Connect):
    config = "applications"

    def __init__(self, config=config, **kwargs):
        super(Connect, self).__init__(config, **kwargs)

        self.applicationName = {
            "enable": True,
            "env": "PIPE-APPLICATION-NAME",
            "value": None,
        }

    def getLauncherConfig(self):
        context = {
            "label": "Pipe-Launcher",
            "name": "launcher",
            "enable": True,
            "location": "%LIBRARY-PATH%/library/applications/launcher.bat",
        }
        return context

    def getLoginConfig(self):
        context = {
            "label": "Pipe-Login",
            "name": "login",
            "enable": True,
            "location": "%LIBRARY-PATH%/library/applications/login.bat",
        }
        return context

    def findApplications(self, add=False):
        applications = self.get()
        if add:
            launcher_context = self.getLauncherConfig()
            login_context = self.getLoginConfig()
            applications.insert(0, launcher_context)
            applications.insert(0, login_context)
        return applications

    def searchApplication(self, name):
        applications = self.findApplications(add=True)
        context = self.findSpecificConfig(name, contexts=applications)
        return context

    def appendNewApplication(self, name):
        context = {
            "name": "mysteps",
            "enable": True,
            "location": "%LIBRARY-PATH%/library/applications/{}.bat".format(
                name
            ),
            "icon": "%s.png" % name,
        }
        return context

    def findEnvironments(self, context):
        contexts = []
        if not context.get("envs"):
            return contexts
        contexts = list(
            filter(lambda k: k.get("enable"), context["envs"])
        )
        if not contexts:
            return None
        self.applicationName["value"] = context.get("name")
        environments = [self.applicationName]

        for context in contexts:
            exists_values = []

            if os.getenv(context["env"]):
                exists_values = os.getenv(context["env"]).split(
                    os.pathsep
                )

            if isinstance(context.get("value"), list):
                new_values = context.get("value")
            else:
                new_values = [context.get("value")]

            values = exists_values + new_values

            values = utils.setPathsResolver(values)

            pprint(values)

            paths = os.pathsep.join(values)
            environment = copy.deepcopy(context)
            environment["value"] = paths
            environments.append(environment)
        return environments

    def createEnvironments(self, name, path=None):
        applications = self.searchApplication(name)
        environments = self.findEnvironments(applications)
        self.createBatch(environments, path=path)

    def createBatch(self, contexts, path=None):
        path = path or os.getenv("TEMP-APPS-ENVS")
        batch_file = utils.createBatch(contexts, path)
        # os.system(batch_file)
        return batch_file

    def setOverrideEnvironments(self, contexts):
        for context in contexts:
            if not context.get("enable"):
                continue
            override_env = context["override"]
            new_values = context["value"]
            if os.getenv(override_env):
                exists_values = os.getenv(override_env).split(
                    os.pathsep
                )
            exists_values = utils.setPathsResolver(exists_values)
            new_values = utils.setPathsResolver(new_values)
            values = exists_values + new_values
            os.environ[override_env] = os.pathsep.join(values)
            LOGGER.info(
                "override the env %s with %s"
                % (override_env, new_values)
            )

    def getEnvironments(self, application=None):
        application = application or os.getenv(
            "PIPE-APPLICATION-NAME"
        )
        if not application:
            LOGGER.warning("could not find such application")
            return
        context = self.searchApplication(application)
        contexts = []
        if not context.get("envs"):
            return contexts
        contexts = utils.searchContext(
            context["envs"], "enable", value=True
        )
        if not contexts:
            return None
        contexts.append(self.applicationName)
        print("\n")
        LOGGER.info("<%s environments>" % application)
        print("\n")
        for each in contexts:
            key = each.get("env")
            if not os.getenv(key):
                LOGGER.error(
                    "env error, not find the env called %s" % key
                )
                continue

            values = os.getenv(key).split(os.pathsep)
            if len(values) == 1:
                env = "{}: {}".format(key.rjust(24), values[0])
                print(env)
            else:
                env = "{}:".format(key.rjust(24))
                print(env)
                for value in values:
                    print("".rjust(23), ":", value)
        print("\n")

    def launch(self, location, thread=True):
        command = utils.setPathResolver(location)
        if not os.path.isfile(command):
            raise ValueError(
                "not found application exe file <%s>" % command
            )
        if not thread:
            self.executeCommand(command)
            return
        self.thread_state = threading.Condition()
        self.palyThread = threading.Thread(
            target=self.executeCommand, args=([command])
        )
        self.palyThread.daemon = True
        self.palyThread.start()

    def executeCommand(self, command):
        print("\n")
        LOGGER.info("execute the event: %s" % command)
        print("\n")
        command = r"%s" % command
        subprocess.call(
            [command], stdout=None, shell=False, stderr=None
        )
        # for testing exception os.startfile(r'%s' % event)


if __name__ == "__main__":
    pass
