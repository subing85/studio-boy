# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:05:37:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks.

import os
import time

from pipe.core import login
from pipe.core import logger

from pipe.core import ftrack
from pipe.core import versions
from pipe.core import dependency
from pipe.core.tasks import start
from pipe.core.tasks import submit
from pipe.core.tasks import publish
from pipe.core.tasks import declined
from pipe.core.tasks import approved

LOGGER = logger.getLogger(__name__)


class Connect(ftrack.Connect):
    entity = "Task"

    def __init__(self, entity=entity, **kwargs):
        super(Connect, self).__init__(entity, **kwargs)
        self.logn = login.Connect()
        self.vers = versions.Connect()
        self.depd = dependency.Connect()

    @property
    def projectid(self):
        self.inpt.config = "project"
        env_key = self.inpt.findEnvValue("id")
        return os.getenv(env_key)

    @property
    def userid(self):
        self.inpt.config = "user"
        env_key = self.inpt.findEnvValue("id")
        return os.getenv(env_key)

    def currentProject(self, projectid=None):
        projectid = projectid or self.projectid
        context = self.update("Project", projectid)
        return context

    def currentUser(self, userid=None):
        userid = userid or self.userid
        context = self.searchUserContext(userid)
        return context

    def currentTask(self, taskid):
        context = self.update(self.entity, taskid)
        return context

    def statusList(self, task):
        statuses = self.currentTaskStatus(task)
        return statuses

    def currentStatus(self, task):
        return task["status"]

    def taskFilter(
        self, projectid, userid, privilege, names=None, pattern=None
    ):
        filter = 'Task where project_id = "%s"' % projectid
        if privilege:
            self.logn.authorization()
            superuser = self.logn.hasSuperUser(userid)
            if not superuser:
                filter += (
                    ' and assignments any (resource.id = "%s")'
                    % userid
                )
        if names:
            filter += ' and name in ("%s")' % '", "'.join(names)
        if pattern:
            filter += " and %s" % pattern
        return filter

    def searchTasks(self, projectid, userid, **kwargs):
        privilege = kwargs.get("privilege", False)
        sort = kwargs.get("sort", False)
        pattern = kwargs.get("pattern", False)
        names = kwargs.get("names", None)

        filter = self.taskFilter(
            projectid, userid, privilege, pattern=pattern, names=names
        )
        contexts = self.search(filter=filter, sort=sort)
        return contexts

    def searchDependencyTasks(self, task):
        contexts = self.depd.dependencies(task)
        if not contexts:
            return None
        return contexts

    def dependencyTasksStatus(self, task):
        contexts = self.searchDependencyTasks(task)
        status = []
        if not contexts:
            return status
        status = [k["status"]["state"]["name"] for k in contexts]
        return status

    def hasDependencyTasksStatus(self, task, status):
        tasks_status = self.dependencyTasksStatus(task)

        print(tasks_status)
        if not status:
            return True

        print(tasks_status.count(status), len(tasks_status))
        result = tasks_status.count(status) == len(tasks_status)
        return result

    def searchTaskByName(self, longname):
        links = longname.split(".")
        filter = self.setParentFilter(links, self.projectid)
        contexts = self.search(filter=filter)
        if not contexts:
            return None
        return contexts

    def setParentFilter(self, links, projectid):
        links.reverse()
        filter = 'Task where %s = "%s" and %s = "%s"' % (
            "project_id",
            projectid,
            "type.name",
            links[0],
        )
        parent = ""
        for each in links[1:]:
            parent += "parent."
            key = "%sname" % parent
            parent_filter = ' and %s = "%s"' % (key, each)
            filter += parent_filter
        return filter

    def searchTask(self, projectid, taskid, userid=None):
        filter = 'Task where %s = "%s" and %s = "%s"' % (
            "project_id",
            projectid,
            "id",
            taskid,
        )
        if userid:
            filter += (
                ' and assignments any (resource.id = "%s")' % userid
            )
        contexts = self.search(filter=filter)
        if not contexts:
            return None
        return contexts[0]

    def startTask(self, taskid, userid=None):
        userid = userid or self.userid
        task = self.searchTask(self.projectid, taskid, userid=userid)
        if not task:
            message = "not find such task context, check your task assignments"
            return None, message
        start.TASKS_OBJECT = self
        user = self.searchUserContext(userid)
        update_task, message = start.execute(
            task, user, timestamp=time.time()
        )
        return update_task, message

    def releaseTask(self, taskid, kind, **kwargs):
        userid = kwargs.get("userid", self.userid)
        release_userid = None if kind == "publish" else userid
        task = self.searchTask(
            self.projectid, taskid, userid=release_userid
        )
        if not task:
            message = "not find such task context, check your task assignments"
            return None, None, message
        kwargs["userid"] = userid
        if kind == "publish":
            publish.TASKS_OBJECT = self
            task, asset_version, message = publish.execute(
                task, **kwargs
            )
        else:
            submit.TASKS_OBJECT = self
            task, asset_version, message = submit.execute(
                task, **kwargs
            )
        return task, asset_version, message

    def removeTaskKinds(self, taskid, kind, userid=None):
        userid = userid or self.userid
        self.logn.authorization()
        superuser = self.logn.hasSuperUser(userid)
        if not superuser:
            email = self.logn.usercontext["email"]
            message = "permission denied current user <%s>" % email
            return False, message
        task = self.searchTask(self.projectid, taskid, userid=None)
        if not task:
            message = "invalid task-id"
            return False, message
        self.vers.authorization()
        contexts = self.vers.searchKindVersions(
            kind=kind, taskid=task["id"]
        )
        if not contexts:
            message = "not found any %s version in the task <%s>" % (
                kind,
                taskid,
            )
            return False, message
        assets, components = [], []
        header = self.contextHeader(task)
        LOGGER.warning("Remove the task asset versions")
        print("\n")
        for context in contexts:
            if context["asset"] not in assets:
                assets.append(context["asset"])
            if context["components"] not in components:
                components.extend(context["components"])
            self.removeAssetVersion(context)
        print("\n")
        LOGGER.info("Remove the task asset entity")
        for each in assets:
            self.remove(each)
        print("\n")
        LOGGER.info("Remove the task components")
        for component in components:
            _component = self.update(
                component.entity_type, component["id"]
            )
            if not _component:
                continue
            self.remove(component)
        print("\n")
        LOGGER.info("Remove done!...")
        start.TASKS_OBJECT = self
        update_task = start.execute(task, self.logn.usercontext)
        return True, None

    def declinedTask(self, taskid, **kwargs):
        userid = kwargs.get("userid", self.userid)
        version = kwargs.get("version")
        comment = kwargs.get("comment")
        task = self.searchTask(self.projectid, taskid, userid=None)
        if not task:
            message = "not find such task context, check your task assignments"
            return None, None, message
        declined.TASKS_OBJECT = self
        declined.VERSN_OBJECT = self.vers
        user = self.searchUserContext(userid)
        task_context, asset_version, message = declined.execute(
            task,
            version,
            user,
            timestamp=time.time(),
            comment=comment,
        )
        return task_context, asset_version, message

    def approvedTask(self, taskid, **kwargs):
        userid = kwargs.get("userid", self.userid)
        version = kwargs.get("version")
        task = self.searchTask(self.projectid, taskid, userid=None)
        if not task:
            message = "not find such task context, check your task assignments"
            return None, None, message
        approved.TASKS_OBJECT = self
        approved.VERSN_OBJECT = self.vers
        user = self.searchUserContext(userid)
        task_context, asset_version, message = approved.execute(
            task, version, user, timestamp=time.time()
        )
        return task_context, asset_version, message

    def currentVersion(self, id):
        context = self.session.get("AssetVersion", id)
        return context

    def isMyTask(self, task, userid=None):
        userid = userid or self.userid
        if not userid:
            LOGGER.warning("invalid user id")
            return
        for each in task["assignments"]:
            if each["resource_id"] == userid:
                return True
        return False


if __name__ == "__main__":
    con = Connect()
    con.authorization()

    task = con.update("Task", "b53f93d7-84c2-4752-9e21-6b21027c1762")

    abc = con.hasDependencyTasksStatus(task, "Done")

    print(abc)
