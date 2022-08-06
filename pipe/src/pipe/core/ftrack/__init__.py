# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:54:25:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core ftrack.

import json
import ftrack_api

from pipe import resources
from pipe.core import logger
from pipe.core import inputs
from pipe.core import discipline

LOGGER = logger.getLogger(__name__)


class Connect(object):
    def __init__(self, entity=None, **kwargs):
        self.entity = entity
        self.disp = discipline.Connect()
        self.inpt = inputs.Connect(self.entity)

    def authorization(self):
        account = resources.getInputData("ftrack")
        self.session = ftrack_api.Session(
            server_url=account["url"],
            api_user=account["api_user"],
            api_key=account["api_key"],
        )

    @property
    def entities(self):
        entities = [
            "User",
            "Project",
            "ProjectSchema",
            "TaskTemplate",
        ]
        return entities

    @property
    def findEntities(self):
        self.authorization()
        entity = self.session.types
        entity = sorted(entity.keys())
        print(json.dumps(entity, indent=4))
        return entity

    @property
    def findFields(self):
        self.authorization()
        contents = list(
            filter(
                lambda k: k["id"] == self.entity, self.session.schemas
            )
        )
        if not contents:
            return None
        print(json.dumps(contents[-1], indent=4))
        return contents[-1]

    def searchCurrentEnvironments(self):
        config = self.inpt.get()
        envs = []
        for each in config:
            if not each.get("enable"):
                continue
            if not each.get("env"):
                continue
            envs.append(each["env"])
        return envs

    def searchEntityContext(self, id, active=False):
        if active:
            filter = 'where is_active = True and id = "%s"' % id
        else:
            filter = 'where id = "%s"' % id
        contexts = self.get(filter=filter)
        if not contexts:
            LOGGER.error('invalid "%s" id <%s>' % (self.entity, id))
            return None
        user_context = contexts.first()
        return user_context

    def searchUserContext(self, userid):
        filter = 'User where is_active = True and id = "%s"' % userid
        contexts = self.search(filter=filter)
        if not contexts:
            LOGGER.error("invalid user id <%s>" % userid)
            return None
        context = contexts.first()
        return context

    def getUserSecurityRole(self, context):
        security_role = context["user_security_roles"][0]
        role_name = security_role["security_role"]["name"]
        return role_name

    def hasSuperUser(self, userid):
        filter = 'User where is_active = True and id = "%s"' % userid
        contexts = self.search(filter=filter)
        if not contexts:
            LOGGER.error("invalid user id <%s>" % userid)
            return None
        self.usercontext = contexts.first()
        role = self.getUserSecurityRole(self.usercontext)
        super_user = self.disp.hasSuperUser(role, context=None)
        return super_user

    def search(self, filter, sort=False):
        contexts = self.session.query(filter)
        if sort:
            contexts = sorted(
                contexts, key=lambda k: (k["created_at"])
            )
        return contexts

    def get(self, filter=None, sort=False):
        if filter:
            filter = "%s %s" % (self.entity, filter)
        else:
            filter = self.entity
        contexts = self.session.query(filter)
        if sort:
            contexts = sorted(
                contexts, key=lambda k: (k["created_at"])
            )
        return contexts

    def update(self, typed, id):
        contexts = self.session.get(typed, id)
        return contexts

    def getone(self, id):
        context = self.session.get(self.entity, id)
        return context

    def getContext(self, context):
        contexts = []
        for each in context:
            data = {}
            for k, v in each.items():
                data[k] = v
            contexts.append(data)
        return contexts

    def remove(self, context):
        if not context:
            return
        name = context.get("name")
        id = context.get("id")
        entity_type = context.entity_type
        self.session.delete(context)
        self.session.commit()
        LOGGER.info(
            "removed <%s>, <%s>, <%s>" % (id, entity_type, name)
        )

    def removeAssetVersion(self, context):
        if context.entity_type != "AssetVersion":
            LOGGER.warning("current context does not AssetVersion")
            return
        id = context.get("id")
        asset_name = context["asset"]["name"]
        entity_type = context.entity_type
        version = context["metadata"].get("version")
        kind = context["metadata"].get("kind")
        self.session.delete(context)
        self.session.commit()
        LOGGER.info(
            "removed <%s>, <%s>, <%s>, <%s>, <%s>, <%s> "
            % (
                id,
                entity_type,
                version,
                context["version"],
                kind,
                asset_name,
            )
        )

    def serverLocation(self):
        serverLocation = self.session.query(
            'Location where name is "ftrack.server"'
        ).one()
        return serverLocation

    def findDependencyTasks(self, task, tasks=None):
        if isinstance(tasks, list):
            filter = "Task where %s and %s and %s and %s" % (
                "project_id = %s" % task["project_id"],
                "parent_id = %s" % task["parent_id"],
                "id != %s" % task["id"],
                'type.name in ("%s")' % '", "'.join(tasks),
            )
        elif tasks:
            filter = "Task where %s and %s and %s and %s" % (
                "project_id = %s" % task["project_id"],
                "parent_id = %s" % task["parent_id"],
                "id != %s" % task["id"],
                "type.name = %s" % tasks,
            )
        else:
            filter = "Task where %s and %s and %s" % (
                "project_id = %s" % task["project_id"],
                "parent_id = %s" % task["parent_id"],
                "id != %s" % task["id"],
            )
        dependency_tasks = self.search(filter)
        return dependency_tasks

    def createNote(self, task, context, components):
        if not context.get("author"):
            context["author"] = self.find_user_context()
        note = self.session.create("Note", context)
        task["notes"].append(note)
        server_location = self.serverLocation()
        for each in components:
            data = {
                "name": each["name"],
                "metadata": each["metadata"],
            }
            component = self.session.create_component(
                path=each["file"], data=data, location=server_location
            )
            component_context = {
                "component_id": component["id"],
                "note_id": note["id"],
            }
            self.session.create("NoteComponent", component_context)
        self.session.commit()
        return note

    def verbose(self, context):
        print("\n")
        for k, v in context.items():
            print(k.rjust(35), ":", v)
        print("\n")

    def removeAsset(self, project_id):
        filter = 'Asset where parent.project_id = "%s"' % project_id
        context = self.search(filter)
        for each in context:
            print("\nname", each["name"])
            print("id", each["id"])
            print("parent", each["parent"]["name"])
            self.session.delete(each)
            print("removed")

    def removeVersions(self, project_id):
        filter = (
            'AssetVersion where task.project_id = "%s"' % project_id
        )
        context = self.search(filter)
        for each in context:
            links = [x["name"] for x in each["link"]]
            print("\nlink", links)
            print("id", each["id"])
            print("task name", each["task"]["name"])
            self.session.delete(each)
            print("removed")

    def removeTasks(self, project_id):
        filter = 'Task where project_id = "%s"' % project_id
        context = self.search(filter)
        for each in context:
            links = [x["name"] for x in each["link"]]
            print("\nlink", links)
            print("id", each["id"])
            print("name", each["name"])
            self.session.delete(each)
            print("removed")

    def currentTaskStatus(self, task):
        project_schema = task["project"]["project_schema"]
        valid_statuses = project_schema.get_statuses("Task")
        statuses = {}
        for each in valid_statuses:
            statuses[each["name"]] = each
        return statuses

    def findStatus(self):
        valid_statuses = self.search("Status")
        statuses = {}
        for each in valid_statuses:
            statuses[each["name"]] = each
        return statuses

    def contextHeader(self, context):
        if not context:
            return None
        if not context.get("link"):
            return None
        headers = []
        if context.entity_type == "AssetVersion":
            headers = [
                context["task"]["project"]["name"],
                context["link"][1]["name"],
                context["link"][2]["name"],
                context["task"]["name"],
                context["metadata"]["version"],
                context["metadata"]["kind"],
            ]
        elif context.entity_type == "Task":
            headers = [context["project"]["name"]]
            headers.extend([k["name"] for k in context["link"][1:]])
        else:
            headers = [k["name"] for k in context["link"]]
        header = "|".join(headers)
        return header

    def searchSecurityRoles(self):
        contexts = self.search(filter="SecurityRole")
        return contexts

    def searchSecurityRoleByName(self, name):
        filter = 'SecurityRole where name = "%s"' % (name)
        contexts = self.search(filter=filter)
        if not contexts:
            return None
        return contexts[0]

    def searchSecurityRoleByNames(self, names):
        filter = 'SecurityRole where name in ("%s")' % '", "'.join(
            names
        )
        contexts = self.search(filter=filter)
        if not contexts:
            return None
        contexts = [each for each in contexts]
        return contexts

    def searchWriteSecurityRoles(self):
        valid_users = ["Administrator", "Project Manager", "API"]
        filter = 'SecurityRole where name in ("%s")' % '", "'.join(
            valid_users
        )
        contexts = self.search(filter=filter)
        return contexts

    def searchReadSecurityRoles(self):
        blocked_users = ["Restricted User"]
        valid_users = [
            "Administrator",
            "Project Manager",
            "API",
            "User",
        ]
        filter = 'SecurityRole where name in ("%s")' % '", "'.join(
            valid_users
        )
        contexts = self.search(filter=filter)
        return contexts

    def updateContext(self, context, **kwargs):
        for k, v in kwargs.items():
            context[k] = v
        self.session.commit()


if __name__ == "__main__":
    pass
