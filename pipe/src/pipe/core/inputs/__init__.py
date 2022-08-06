# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-12:42:30:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core resource inputs.

import os

from pipe import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Connect(object):
    def __init__(self, config, **kwargs):
        self.config = config.lower() if config else None

    @property
    def inputs(self):
        _inputs = resources.getInputData(self.config) or []
        return _inputs

    def getConfigPath(self):
        path = os.path.join(
            resources.getInputPath(), "%s.json" % self.config
        )
        return path

    def get(self):
        data = list(
            filter(
                lambda enable: enable["enable"] == True, self.inputs
            )
        )
        data = sorted(data, key=lambda k: (k["order"]))
        return data

    def values(self, key="name", data=None):
        data = data or self.get()
        names = []
        for each in data:
            names.append(each[key])
        return names

    def findSpecificConfig(self, name, contexts=None):
        contexts = contexts or self.get()
        specific_contexts = list(
            filter(lambda k: k.get("name") == name, contexts)
        )
        if not specific_contexts:
            return dict()
        return specific_contexts[0]

    def findEnvValue(self, key):
        context = self.findSpecificConfig(key)
        if not context:
            LOGGER.warning("unvalued <%s> configure" % self.config)
            return
        if not context.get("env"):
            LOGGER.warning(
                'not found "env" key in the <%s> configure'
                % (key, self.config)
            )
            return
        return context["env"]


if __name__ == "__main__":
    pass
