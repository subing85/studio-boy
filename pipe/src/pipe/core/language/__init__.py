# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-12:42:39:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core language.

import json

from pipe import utils
from pipe.core import logger
from pipe.core import inputs

LOGGER = logger.getLogger(__name__)


class Connect(inputs.Connect):
    typed = "language"

    def __init__(self, typed=typed, **kwargs):
        super(Connect, self).__init__(typed, **kwargs)

    def findConfigure(self, language, key="name"):
        inputs = self.get()
        context = dict()
        contexts = list(
            filter(
                lambda k: k[key] == language,
                inputs,
            )
        )
        if not contexts:
            LOGGER.warning("invalid language <%s>" % language)
            return context
        context = contexts[0]
        return context

    def environments(self, language, key="name"):
        context = self.findConfigure(language, key=key)
        environments = [
            {
                "name": context.get("name"),
                "env": context.get("env"),
                "enable": True,
                "order": context.get("order"),
                "value": context.get("name"),
            }
        ]
        return environments

    def createEnviron(self, contexs):
        utils.setEnvironment(contexs)

    def searchCurrentEnvironments(self, language, key="name"):
        context = self.findConfigure(language, key=key)
        envs = []
        for each in [context]:
            if not each.get("enable"):
                continue
            if not each.get("env"):
                continue
            envs.append(each["env"])
        return envs


if __name__ == "__main__":
    pass
