# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-12:49:38:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core login.

import os
import tempfile

from pipe import utils
from pipe import resources
from pipe.core import ftrack


class Connect(ftrack.Connect):
    entity = "User"

    def __init__(self, entity=entity, **kwargs):
        super(Connect, self).__init__(entity, **kwargs)
        self.loginpath = os.path.join(
            tempfile.gettempdir(), "pipe-user-login.log"
        )

    @property
    def userid(self):
        env_key = self.inpt.findEnvValue("id")
        return os.getenv(env_key)

    @property
    def username(self):
        env_key = self.inpt.findEnvValue("username")
        return os.getenv(env_key)

    @property
    def email(self):
        env_key = self.inpt.findEnvValue("email")
        return os.getenv(env_key)

    @property
    def discipline(self):
        env_key = self.inpt.findEnvValue("email")
        return os.getenv(env_key)

    def searchUsers(self):
        filter = "User where is_active = True"
        contexts = self.search(filter=filter)
        return contexts

    def findByName(self, username):
        filter = (
            'User where is_active = True and username = "%s"'
            % username
        )
        contexts = self.search(filter=filter)
        context = contexts.first()
        return context

    def findById(self, userid):
        context = self.searchEntityContext(userid, active=False)
        return context

    def appendEnvironmentValue(self, context):
        environments = []
        for each in self.inpt.get():
            if each["name"] == "discipline":
                role_name = self.getUserSecurityRole(context)
                environment = {"env": each["env"], "value": role_name}
            else:
                environment = {
                    "env": each["env"],
                    "value": context[each["name"]],
                }
            environments.append(environment)
        return environments

    def writeHistory(self, context):
        date = resources.getDateTime()
        with (open(self.loginpath, "a")) as log:
            log.write(
                "login: %s: %s [%s]\n"
                % (date, context["username"], context["email"])
            )
            return True

    def readHistory(self):
        if not os.path.isfile(self.loginpath):
            return
        context = None
        with (open(self.loginpath, "r")) as log:
            context = log.readlines()
            context.reverse()
        if not context:
            return None
        history = []
        for each in context:
            lines = each.strip().split(" ")
            history.append(lines)
        return history

    def createBatch(self, contexts, path=None):
        path = path or os.getenv("TEMP-USERNAME-ENVS")
        batch_file = utils.createBatch(contexts, path)
        print(batch_file)
        return batch_file

    def getRole(self, userid=None):
        userid = userid or self.userid
        context = self.getUserContext(userid=userid)
        if not context:
            return
        role = self.getUserSecurityRole(context)
        return role


if __name__ == "__main__":
    pass
