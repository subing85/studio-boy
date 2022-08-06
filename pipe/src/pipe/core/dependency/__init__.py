# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:25:39:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core task dependency.

from pipe.core import logger
from pipe.core import ftrack
from pipe.core import inputs
from pipe.core import versions

LOGGER = logger.getLogger(__name__)


class Connect(object):
    def __init__(self, task=None):
        super(Connect, self).__init__()

        self.task = task
        self.ftrk = ftrack.Connect()
        self.vers = versions.Connect()
        self.inputs = self.getInputs()

    def getInputs(self):
        inpt = inputs.Connect("dependency")
        return inpt.get()

    def getDependency(self, task_name):
        contents = list(
            filter(lambda k: k["task"] == task_name, self.inputs)
        )
        if not contents:
            LOGGER.warning("invalid task name <%s>" % task_name)
            return
        current_dependency = []
        if not contents[0].get("dependency"):
            return current_dependency
        for each in contents[0]["dependency"]:
            contents = list(
                filter(lambda k: k["task"] == each, self.inputs)
            )
            if not contents:
                continue
            current_dependency.append(contents[0])
        return current_dependency

    def getDependencyTasks(self, task=None):
        task = task or self.task
        dependency = self.getDependency(task["type"]["name"])

        if not dependency:
            return list()
        tasks = [each["task"] for each in dependency]
        return tasks

    def dependencies(self, task):
        tasks = self.getDependencyTasks(task)
        self.ftrk.authorization()
        dependency_tasks = self.ftrk.findDependencyTasks(
            task, tasks=tasks
        )
        if not dependency_tasks:
            return list()
        return dependency_tasks


if __name__ == "__main__":
    pass
