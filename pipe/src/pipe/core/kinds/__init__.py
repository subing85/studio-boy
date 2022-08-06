# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:54:35:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core kinds (submit, publish).

from pipe.core import inputs


class Entity(dict):

    # entity = dict()
    entity_type = "Kind"

    def __init__(self):
        #  Entity.__init__(self)
        super(Entity, self).__init__()

        self.__dict__ = dict()

    def updateContext(self, **kwargs):
        self.update(kwargs)


class Connect(inputs.Connect):
    typed = "kind"
    entity = Entity()

    def __init__(self, typed=typed, **kwargs):
        super(Connect, self).__init__(typed, **kwargs)

    def searchKindContext(self, kind):
        inputs = self.get()
        contexts = list(filter(lambda k: k["name"] == kind, inputs))
        if not contexts:
            return None
        return contexts[0]

    def findKindStatus(self, kind):
        context = self.searchKindContext(kind)
        if not context:
            return None
        return context.get("status")

    def findKindDependencyStatus(self, kind):
        context = self.searchKindContext(kind)
        if not context:
            return None
        return context.get("dependencyStatus")

    def findKindName(self, kind):
        context = self.searchKindContext(kind)
        if not context:
            return None
        return context.get("display-name")

    def setEntity(self, name, **kwargs):
        kind_versions = self.searchChildren(
            kwargs.get("parent"), name
        )
        context = {
            "name": name,
            "parent": kwargs.get("parent"),
            "children": kind_versions,
        }
        context.update(**kwargs)
        self.entity = Entity()
        self.entity.updateContext(**context)

    def searchChildren(self, task, kind):
        from pipe.core import versions

        self.vers = versions.Connect()
        self.vers.authorization()
        versions = self.vers.searchKindVersions(
            taskid=task["id"], kind=kind
        )
        return versions

    def getPrimaryKindList(self):
        kindList = []
        for each in self.get():
            if not each.get("primary"):
                continue
            kindList.append(each["name"])
        return kindList


if __name__ == "__main__":
    pass
