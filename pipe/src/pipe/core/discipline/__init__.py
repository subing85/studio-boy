# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:51:06:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core discipline.

from pipe.core import logger
from pipe.core import inputs

LOGGER = logger.getLogger(__name__)


class Connect(inputs.Connect):
    typed = "discipline"

    def __init__(self, typed=typed, **kwargs):
        super(Connect, self).__init__(typed, **kwargs)

    def searchDisciplineContext(self, role):
        discipline = list(
            filter(lambda k: k.get("name") == role, self.get())
        )
        if not discipline:
            LOGGER.warning("invalid role")
            return None
        return discipline[-1]

    def findPrivilege(self, role, context=None):
        context = context or self.searchDisciplineContext(role)
        if not context:
            LOGGER.warning("not able to find privilege")
            return None
        return context.get("privilege")

    def hasSuperUser(self, role, context=None):
        context = context or self.searchDisciplineContext(role)
        if not context:
            return False
        privilege = self.findPrivilege(role, context=context)
        if privilege == "super-user":
            return True
        return False


if __name__ == "__main__":
    pass
