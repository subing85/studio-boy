# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:17:07:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe python api.

import os

from pipe import core
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

import importlib

importlib.reload(core)


class Login(core.Login):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

    def setUsername(self, username, path=None):
        self.authorization()
        context = self.findByName(username)
        if not context:
            LOGGER.warning("invalid user name")
            return False
        environments = self.appendEnvironmentValue(context)
        self.createBatch(environments, path=path)
        self.writeHistory(context)
        return True

    def getUsername(self):
        environments = self.searchCurrentEnvironments()
        print("\n")
        LOGGER.info("Studio-Pipe Login Environments")
        print("\n")
        for each in environments:
            print("\t", each.rjust(25), ": ", os.getenv(each))
        print("\n")
        return environments

    def getAllUsers(self):
        self.authorization()
        print("\n")
        contexts = self.searchUsers()
        if not contexts:
            LOGGER.error("not find any users in ftrack")
            return
        LOGGER.info("registered users are")
        print("\n")
        for context in contexts:
            print("Email:".rjust(15), context["email"])
            print("Username:".rjust(15), context["username"])
            print("id:".rjust(15), context["id"])
            print("Status:".rjust(15), context["is_active"])
            print(
                "User Type:".rjust(15), context["user_type"]["name"]
            )
            role = context["user_security_roles"][0]["security_role"][
                "name"
            ]
            print("User Role:".rjust(15), role)
            print("entity".rjust(15), "User")
            print("\n")

    def loginHistory(self):
        history = self.readHistory()
        print("\n")
        LOGGER.info("your login history")
        if not history:
            LOGGER.warning("not found login history")
            return
        for each in history:
            print("\t", " ".join(each))
        print("\n")
        return history

    def getUserContext(self, userid=None):
        userid = userid or self.userid
        self.authorization()
        context = self.findById(userid)
        if not context:
            LOGGER.warning("invalid user id")
            return None
        return context

    def isSuperUser(self, userid=None):
        userid = userid or self.userid
        self.authorization()
        superuser = self.hasSuperUser(userid)
        return superuser

    def isValidLogin(self):
        if not self.userid:
            return False
        self.context = self.getUserContext(self.userid)
        if not self.context:
            return False
        return True

    def isLogin(self):
        if self.userid:
            return True
        return False


class Project(core.Project):
    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)

    def createNewProject(self, *args, **kwargs):
        name = args[0]
        fullname = args[1]
        schema = args[2]
        thumbnail = kwargs.get("thumbnail", None)

        self.authorization()
        print("\n")
        LOGGER.info("project inputs")
        print("\n")
        print("name:".rjust(15), name)
        print("Full Name:".rjust(15), fullname)
        print("Template:".rjust(15), schema)
        print("thumbnail:".rjust(15), thumbnail)
        valid, message, result = self.createProject(
            name, fullname, schema, thumbnail=thumbnail, commit=True
        )
        print("\n")
        return valid, message, result

    def deleteProject(self, name):
        self.authorization()
        context = self.findByName(name)
        print("\n")
        if not context:
            LOGGER.warning(
                "not found such project called %s:" % (name)
            )
            print("\n")
            return
        self.remove(context)
        print("\n")

    def getAllProjects(self):
        self.authorization()
        contexts = self.searchProjects()
        print("\n")
        if not contexts:
            LOGGER.warning("not find any projects in ftrack")
            print("\n")
            return
        LOGGER.info("available projects are")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("Full Name:".rjust(15), context["full_name"])
            print("id:".rjust(15), context["id"])
            print("Status:".rjust(15), context["status"])
            created_at = context["created_at"].format(
                "YYYY-MM-DD HH:mm:ss ZZ"
            )
            print("Created at:".rjust(15), created_at)
            created_by = "%s [%s]" % (
                context["created_by"]["username"],
                context["created_by"]["email"],
            )
            print("Created by:".rjust(15), created_by)
            print("\n")
        return contexts

    def setProject(self, name, path=None):
        self.authorization()
        project = self.findByName(name)
        if not project:
            print("\n")
            LOGGER.warning(
                "Not found such project called %s:" % (name)
            )
            return
        environments = self.environments(project)
        self.createBatch(environments, path=path)
        return project

    def _setProject(self, name):
        self.authorization()
        project = self.findByName(name)
        if not project:
            print("\n")
            LOGGER.warning(
                "Not found such project called %s:" % (name)
            )
            return
        environments = self.environments(project)
        self.createEnviron(environments)
        return project

    def getProject(self):
        environments = self.searchCurrentEnvironments()
        print("\n")
        LOGGER.info("studio-pipe project environments")
        print("\n")
        for each in environments:
            print("%s:" % each.rjust(20), os.getenv(each))
        print("\n")
        return environments

    def getCurrentProject(self):
        self.authorization()
        current_project = self.currentProject()
        return current_project

    def getProjectTemplates(self):
        self.authorization()
        contexts = self.searchSchemas()
        print("\n")
        LOGGER.info(
            "available project template(schema) types in ftrack"
        )
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), "ProjectSchema")
            print("\n")
        return contexts

    def getProjectTemplate(self, id=None):
        id = id or self.projectid
        print("\n")
        if not id:
            LOGGER.warning(
                "not register the project in the pipe-studio"
            )
            return
        self.authorization()
        project = self.findById(id)
        context = self.projectSchema(project)
        if not context:
            LOGGER.warning(
                "not find any schema in the project <%s>"
                % project["name"]
            )
            print("\n")
            return
        LOGGER.info("current project template (schema) in ftrack\n")
        print("\n")
        print("name:".rjust(15), context["name"])
        print("id:".rjust(15), context["id"])
        print("entity:".rjust(15), "ProjectSchema")
        print("Project Name:".rjust(15), project["name"])
        print("\n")
        return context

    def getProjectCategories(self, id=None):
        id = id or self.projectid
        print("\n")
        if not id:
            LOGGER.warning(
                "not register the project in the pipe-studio"
            )
            print("\n")
            return
        self.authorization()
        project = self.findById(id)
        contexts = self.validCategories(project)
        if not contexts:
            LOGGER.warning(
                "not find any categories in the project <%s>"
                % project["name"]
            )
            print("\n")
            return
        print("\n")
        LOGGER.info("available projects categories in ftrack are")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("Type:".rjust(15), context.entity_type)
            print(
                "Project:".rjust(15), context["project"]["full_name"]
            )
            created_at = context["created_at"].format(
                "YYYY-MM-DD HH:mm:ss ZZ"
            )
            print("Created at:".rjust(15), created_at)
            created_by = "%s [%s]" % (
                context["created_by"]["username"],
                context["created_by"]["email"],
            )
            print("Created by:".rjust(15), created_by)
            print("\n")
        return contexts


class Attributes(core.Attributes):
    def __init__(self, **kwargs):
        super(Attributes, self).__init__(**kwargs)

        self.authorization()

    def getAllAttributes(self):
        contexts = self.searchAttributes()
        print("\n")
        LOGGER.info("Custom attributes")
        for context in contexts:
            print("\n")
            print("key:".rjust(15), context["key"])
            print("label:".rjust(15), context["label"])
            print("id:".rjust(15), context["id"])
            print("core:".rjust(15), context["core"])
            print("sort:".rjust(15), context["sort"])
            print("entity type:".rjust(15), context["entity_type"])
            print(
                "object type:".rjust(15),
                context["object_type"]["name"],
            )
            print(
                "object id:".rjust(15), context["object_type"]["id"]
            )
            print("type:".rjust(15), context["type"]["name"])
            break
        return contexts

    def getAttribute(self, label, **kwargs):
        context = self.searchAttribute(label, **kwargs)
        print("\n")
        if not context:
            LOGGER.warning("not found <%s> Custom attributes" % label)
        print("key:".rjust(15), context["key"])
        print("label:".rjust(15), context["label"])
        print("id:".rjust(15), context["id"])
        print("core:".rjust(15), context["core"])
        print("sort:".rjust(15), context["sort"])
        print("entity type:".rjust(15), context["entity_type"])
        print(
            "object type:".rjust(15), context["object_type"]["name"]
        )
        print("object id:".rjust(15), context["object_type"]["id"])
        print("type:".rjust(15), context["type"]["name"])
        return context

    def deleteAttribute(self, label, **kwargs):
        context = self.searchAttribute(label, **kwargs)
        print("\n")
        if not context:
            LOGGER.warning(
                "not able to remove <%s> Custom attributes" % label
            )
            return None
        self.remove(context)

    def createNewAttribute(self, **kwargs):
        context = self.createAttribute(**kwargs)
        print("\n")
        if not context:
            LOGGER.warning("not able to create new custom attributes")
            return
        LOGGER.infor("Created new custom attributes")
        print("key:".rjust(15), context["key"])
        print("label:".rjust(15), context["label"])
        print("id:".rjust(15), context["id"])
        print("core:".rjust(15), context["core"])
        print("sort:".rjust(15), context["sort"])
        print("entity type:".rjust(15), context["entity_type"])
        print(
            "object type:".rjust(15), context["object_type"]["name"]
        )
        print("object id:".rjust(15), context["object_type"]["id"])
        print("type:".rjust(15), context["type"]["name"])
        return context

    def createProjectCustomAttributes(self):
        self.createProjectAttributes()


class Applications(core.Applications):
    def __init__(self, **kwargs):
        super(Applications, self).__init__(**kwargs)

    def getApplications(self):
        applications = self.findApplications(add=True)
        LOGGER.info("studio-pipe configure applications")
        for application in applications:
            label = "{}: {}".format(
                "label".rjust(10), application.get("label")
            )
            command = "{}: {}".format(
                "event".rjust(10), application.get("name")
            )
            status = "{}: {}".format(
                "status".rjust(10), application.get("enable")
            )
            location = "{}: {}".format(
                "location".rjust(10),
                os.path.expandvars(application.get("location")),
            )
            print(label)
            print(command)
            print(status)
            print(location)
            print("\n")

    def setEnvironments(self, application, path=None):
        path = path or os.getenv("TEMP-APPS-ENVS")
        self.createEnvironments(application, path=path)

    def startLaunch(self, application, location=None, thread=True):
        self.setEnvironments(application)
        self.getEnvironments()
        if not location:
            configure = self.searchApplication(application)
            if not configure:
                configure = self.appendNewApplication(application)
            location = configure.get("location")
        if not location:
            LOGGER.warning(
                "<%s> application location is not describe in the configure"
                % application
            )
            return
        self.launch(location, thread=thread)

    def verboseEnvironments(self, configure, application):
        if not configure.get("envs"):
            return
        LOGGER.info("<%s environments>" % application)
        for each in configure["envs"]:
            key = each.get("env")
            if not os.getenv(key):
                LOGGER.error(
                    "env error, not find the env called %s" % key
                )
                continue
            values = os.getenv(key).split(os.pathsep)
            if len(values) == 1:
                env = "{}: {}".format(key.rjust(25), values[0])
                print(env)
            else:
                env = "{}:".format(key.rjust(25))
                print(env)
                for value in values:
                    print("".rjust(25), ":", value)
        print("\n")
        location = configure.get("location")


class Steps(core.Steps):
    def __init__(self, **kwargs):
        super(Steps, self).__init__(**kwargs)

    def getStepTemplates(self):
        self.authorization()
        contexts = self.searchTaskTemplates()
        print("\n")
        if not contexts:
            LOGGER.error(
                "not find task templates in the current project"
            )
            return
        LOGGER.info(
            "task templates from in the current project schema in ftrack"
        )
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def getStepTemplate(self, name):
        self.authorization()
        context = self.searchTaskTemplate(name)
        print("\n")
        if not context:
            LOGGER.warning(
                "not find <%s> task template in the current project"
                % name
            )
            return
        return context

    def isAssetExists(self, name):
        self.authorization()
        context = self.searchAsset(name)
        print("\n")
        LOGGER.info(
            "whether an asset with the given name <%s> exists\n"
            % name
        )
        if context:
            print(
                "asset is already exists:".rjust(25), context["name"]
            )
            print("id:".rjust(25), context["id"])
            print("type:".rjust(25), context["type"]["name"])
            print("type id:".rjust(25), context["type"]["id"])
            print("entity:".rjust(25), context.entity_type)
        else:
            print("asset does not exists:".rjust(25), name)
        print("\n")
        return context

    def createNewAsset(self, name, typed, template, **kwargs):
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        self.authorization()
        print("\n")
        valid, message, [asset, asset_tasks] = self.createAsset(
            name,
            typed,
            template,
            thumbnail=thumbnail,
            description=description,
        )
        if not valid:
            print("\n")
            return valid, message, None
        LOGGER.info("created new asset")
        self.verboseCommit(
            "asset", asset, template=template, children=asset_tasks
        )
        LOGGER.info(message)
        print("\n")
        return valid, message, asset

    def updateExistsAsset(self, step, typed, template, **kwargs):
        name = kwargs.get("name") or None
        description = kwargs.get("description") or None
        thumbnail = None
        metadata = kwargs.get("metadata") or None

        print("\n")
        valid, message, [asset, asset_tasks] = self.updateAsset(
            step,
            typed,
            template,
            name=name,
            thumbnail=thumbnail,
            description=description,
            metadata=metadata,
        )
        if not valid:
            print("\n")
            return valid, message, None
        LOGGER.info("updated the asset")
        self.verboseCommit(
            "asset", asset, template=template, children=asset_tasks
        )
        LOGGER.info(message)
        print("\n")
        return valid, message, asset

    def deleteAsset(self, name):
        self.authorization()
        print("\n")
        valid = self.deleteAssets(name)
        if not valid:
            LOGGER.warning(
                "not found such asset called <%s> in the current check-in project"
                % (name)
            )
            print("\n")
            return valid
        print("\n")
        return valid

    def getAssetByName(self, name):
        self.authorization()
        context = self.searchAsset(name)

        return context
        print("\n")

    def getAssets(self, typed):
        self.authorization()
        contexts = self.searchAssetsByType(typed)
        print("\n")
        LOGGER.info("assets from current check-in project")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("type:".rjust(15), context["type"]["name"])
            print("type-id:".rjust(15), context["type"]["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def getAssetTypes(self):
        self.authorization()
        contexts = self.searchAssetTypes()
        print("\n")
        if not contexts:
            LOGGER.error(
                "not find asset types in the current project"
            )
            return
        LOGGER.info("current check-in project asset types")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("sort:".rjust(15), context["sort"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def isSequenceExists(self, name):
        self.authorization()
        print("\n")
        context = self.searchSequence(name)
        LOGGER.info(
            "whether a sequence with the given name <%s> exists\n"
            % name
        )
        if context:
            print(
                "sequence is already exists:".rjust(30),
                context["name"],
            )
            print("id:".rjust(30), context["id"])
            print("entity:".rjust(30), context.entity_type)
        else:
            print("sequence does not exists:".rjust(30), name)
        print("\n")
        return context

    def createNewSequence(self, name, **kwargs):
        range = kwargs.get("range", None)
        timeunit = kwargs.get("timeunit", None)
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        metadata = kwargs.get("metadata", None)

        self.authorization()
        print("\n")
        valid, message, sequence = self.createSequence(
            name,
            thumbnail=thumbnail,
            description=description,
            timeunit=timeunit,
            range=range,
            metadata=metadata,
        )
        if not valid:
            print("\n")
            return valid, message, None
        LOGGER.info("create new sequence")
        print("\n")
        print("name:".rjust(15), sequence["name"])
        print("Id:".rjust(15), sequence["id"])
        print("entity:".rjust(15), sequence.entity_type)
        print("\n")
        LOGGER.info(message)
        print("\n")
        return valid, message, sequence

    def updateExistsSequence(self, step, **kwargs):
        name = kwargs.get("name") or None
        range = kwargs.get("range") or None
        timeunit = kwargs.get("timeunit") or None
        thumbnail = kwargs.get("thumbnail") or None
        description = kwargs.get("description") or None
        metadata = kwargs.get("metadata") or None

        print("\n")
        valid, message, sequence = self.updateSequence(
            step,
            name=name,
            range=range,
            timeunit=timeunit,
            thumbnail=thumbnail,
            description=description,
            metadata=metadata,
        )
        if not valid:
            print("\n")
            return valid, message, None

        LOGGER.info("updated the sequence")
        print("\n")
        print("name:".rjust(15), sequence["name"])
        print("Id:".rjust(15), sequence["id"])
        print("entity:".rjust(15), sequence.entity_type)
        print("\n")
        LOGGER.info(message)
        print("\n")
        return valid, message, sequence

    def deleteSequence(self, name):
        self.authorization()
        print("\n")
        valid = self.deleteSequences(name)
        if not valid:
            LOGGER.warning(
                "not found such sequence called <%s> in the current check-in project"
                % (name)
            )
            print("\n")
            return valid
        print("\n")
        return valid

    def getSequences(self, name):
        self.authorization()
        contexts = self.searchSequenceByName(name)
        print("\n")
        LOGGER.info("sequences from current check-in project")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def isShotExists(self, name, parent):
        self.authorization()
        context = self.searchShot(name, parent)
        print("\n")
        LOGGER.info(
            "whether an shot with the given name <%s> exists\n" % name
        )
        if context:
            print(
                "shot is already exists:".rjust(35), context["name"]
            )
            print("id:".rjust(35), context["id"])
            print("entity:".rjust(35), context.entity_type)
            print("parent:".rjust(35), context["parent"]["name"])
            print("parent id:".rjust(35), context["parent"]["id"])
            print(
                "parent entity:".rjust(35),
                context["parent"].entity_type,
            )
        else:
            print("shot does not exists:".rjust(35), name)
        print("\n")
        return context

    def createNewShot(self, name, parent, template, **kwargs):
        range = kwargs.get("range", None)
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        metadata = kwargs.get("metadata") or None
        self.authorization()
        print("\n")
        valid, message, [shot, shot_tasks] = self.createShot(
            name,
            parent,
            template,
            range=range,
            thumbnail=thumbnail,
            description=description,
            metadata=metadata,
        )
        if not valid:
            print("\n")
            return valid, message, None
        LOGGER.info("create new shot")
        self.verboseCommit(
            "shot", shot, template=template, children=shot_tasks
        )
        LOGGER.info(message)
        print("\n")
        return valid, message, shot

    def updateExistsShot(self, step, template, **kwargs):
        name = kwargs.get("name") or None
        range = kwargs.get("range") or None
        timeunit = kwargs.get("timeunit") or None
        thumbnail = kwargs.get("thumbnail") or None
        description = kwargs.get("description") or None
        metadata = kwargs.get("metadata") or None

        print("\n")
        valid, message, shot = self.updateShot(
            step,
            template,
            name=name,
            range=range,
            timeunit=timeunit,
            thumbnail=thumbnail,
            description=description,
            metadata=metadata,
        )
        if not valid:
            print("\n")
            return valid, message, None

        LOGGER.info("updated the sequence")
        print("\n")
        print("name:".rjust(15), shot["name"])
        print("Id:".rjust(15), shot["id"])
        print("entity:".rjust(15), shot.entity_type)
        print("\n")
        LOGGER.info(message)
        print("\n")
        return valid, message, shot

    def deleteShot(self, parent, name):
        self.authorization()
        print("\n")
        valid = self.deleteShots(parent, name)
        if not valid:
            LOGGER.warning(
                "not found such shot called <%s - %s> in the current check-in project"
                % (parent, name)
            )
            print("\n")
            return valid
        print("\n")
        return valid

    def getShots(self, parent, name):
        self.authorization()
        contexts = self.searchShotByName(parent, name)
        print("\n")
        LOGGER.info("shot from current check-in project sequence")
        print("\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("Parent:".rjust(15), context["parent"]["name"])
            print("entity:".rjust(15), context.entity_type)
            print("parent:".rjust(15), context["parent"]["name"])
            print("parent id:".rjust(15), context["parent"]["id"])
            print(
                "parent entity:".rjust(15),
                context["parent"].entity_type,
            )
            print("\n")
        return contexts

    def getTasks(self, template):
        self.authorization()
        contexts = self.searchTasks(template)
        print("\n")
        if not contexts:
            LOGGER.error(
                "not find the steps from <%s> template." % template
            )
            print("\n")
            return
        LOGGER.info(
            "available task are in the <%s> template\n" % template
        )
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def getStepTasks(self, step):
        self.authorization()
        contexts = self.searchStepTasks(step)
        print("\n")
        if not contexts:
            LOGGER.error(
                "not find the tasks from the step <%s> current check-in project."
                % step
            )
            print("\n")
            return
        LOGGER.info(
            "available tasks are in the <%s> current check-in project.\n"
            % step
        )
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def getStepsTempalteNames(self, id=None):
        self.authorization()
        contexts = self.searchTaskTemplates()
        names = [each["name"] for each in contexts]
        return names

    def getAssetTypeNames(self, id=None):
        id = id or self.project_id
        if not id:
            print(
                "\n\twarning: not register the project in the pipe-studio"
            )
            return
        self.authorization()
        project = self.currentProject(id)
        contexts = self.searchAssetTypes(project)
        names = [each["name"] for each in contexts]
        return names

    def getAssetNames(self, typed, id=None):
        id = id or self.project_id
        if not id:
            print(
                "\n\twarning: not register the project in the pipe-studio"
            )
            return
        self.authorization()
        project = self.currentProject(id)
        contexts = self.searchAssets(project, typed=typed)
        names = [each["name"] for each in contexts]
        return names

    def getAllTasks(self, id=None):
        id = id or self.project_id
        if not id:
            print(
                "\n\twarning: not register the project in the pipe-studio"
            )
            return
        self.authorization()
        project = self.currentProject(id)
        contexts = self.searchAllTasks(project)
        print("\n\tavailable all task from the current project\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("sort:".rjust(15), context["sort"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def getStatus(self):
        self.authorization()
        contexts = self.searchStatus()
        print("\n\tentity status\n")
        for context in contexts:
            print("name:".rjust(15), context["name"])
            print("id:".rjust(15), context["id"])
            print("entity:".rjust(15), context.entity_type)
            print("\n")
        return contexts

    def verboseCommit(self, *args, **kwargs):
        key = args[0]
        parent = args[1]
        template = kwargs.get("template", None)
        children = kwargs.get("children", [])
        print("\n")
        print("name:".rjust(15), parent["name"])
        print("id:".rjust(15), parent["id"])
        if parent.get("type"):
            print("type:".rjust(15), parent["type"])
        if template:
            print("template:".rjust(15), template)
        print("entity:".rjust(15), parent.entity_type)
        if not children:
            return
        print("\n\t\t%s <%s> tasks\n" % (key, parent["name"]))
        for child in children:
            print("name:".rjust(25), child["name"])
            print("id:".rjust(25), child["id"])
            print("entity:".rjust(25), child.entity_type)
            print("\n")


class Status(core.Status):
    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)

    def getTaskStatus(self):
        self.authorization()
        contexts = self.searchTaskStatus()
        print("\n")
        if not contexts:
            LOGGER.error(
                "not find task status in the current project."
            )
            return
        LOGGER.info("project task status are")
        for context in contexts:
            print("\n")
            print("name:".rjust(15), context["name"])
            print("active:".rjust(15), context["is_active"])
            print("color:".rjust(15), context["color"])
            print("sort:".rjust(15), context["sort"])
        print("\n")


class Tasks(core.Tasks):
    def __init__(self, **kwargs):
        super(Tasks, self).__init__(**kwargs)

        self.tab = 15

    def verboseTask(self, context, tab=15):
        tab = tab or self.tab
        header = self.contextHeader(context)
        print("\n")
        print("header:".rjust(tab), header)
        print("task name:".rjust(tab), context["name"])
        print("id:".rjust(tab), context["id"])
        print("type:".rjust(tab), context.entity_type)
        print("status:".rjust(tab), context["status"]["name"])
        created_at = context["created_at"].format(
            "YYYY-MM-DD HH:mm:ss ZZ"
        )
        print("created at:".rjust(tab), created_at)
        created_by = "%s [%s]" % (
            context["created_by"]["username"],
            context["created_by"]["email"],
        )
        print("created by:".rjust(tab), created_by)

    def verboseVersions(self, context, tab=15):
        header = self.contextHeader(context)
        print("\n")
        print("header:".rjust(tab), header)
        print("id:".rjust(tab), context["id"])
        print("type:".rjust(tab), context.entity_type)
        print("status:".rjust(tab), context["status"]["name"])
        print("kind:".rjust(tab), context["metadata"].get("kind"))
        print(
            "version:".rjust(tab), context["metadata"].get("version")
        )
        print("status:".rjust(tab), context["metadata"].get("status"))
        print(
            "status-by:".rjust(tab),
            context["metadata"].get("status-by"),
        )
        print(
            "status-at:".rjust(tab),
            context["metadata"].get("status-at"),
        )
        print("task id:".rjust(tab), context["task"]["id"])
        print("asset id:".rjust(tab), context["asset"]["id"])

    def getMyTasks(self, projectid=None, userid=None, **kwargs):
        projectid = projectid or self.projectid
        userid = userid or self.userid
        names = kwargs.get("names", None)
        self.authorization()
        print("\n")
        user = self.currentUser(userid=userid)
        security_role = self.getUserSecurityRole(user)
        contexts = self.searchTasks(
            projectid,
            userid,
            privilege=True,
            name=[],
            sorted_by=True,
            names=names,
        )
        if not contexts:
            LOGGER.warning(
                "not find any steps for user <%s>" % user["username"]
            )
            print("\n")
            return
        LOGGER.info(
            "available steps for user <%s>" % user["username"]
        )
        LOGGER.info("user role <%s>" % security_role)
        for context in contexts:
            self.verboseTask(context)
        print("\n")
        return contexts

    def getTasks(self, *args, **kwargs):
        projectid = args[0]
        userid = args[1]
        privilege = kwargs.get("privilege", True)
        name = kwargs.get("name", True)
        sorted_by = kwargs.get("sorted_by", False)
        self.authorization()
        contexts = self.searchTasks(
            projectid,
            userid,
            privilege=privilege,
            name=name,
            sorted_by=sorted_by,
        )
        return contexts

    def getTaskDependency(self, taskid):
        self.authorization()
        task = self.currentTask(taskid)
        contexts = self.searchDependencyTasks(task)
        print("\n")
        LOGGER.info("task details")
        self.verboseTask(task)
        print("\n")
        if not contexts:
            LOGGER.warning("not find any dependency tasks")
            print("\n")
            return
        LOGGER.info("available dependency task are,")
        for context in contexts:
            self.verboseTask(context, tab=25)
            print("\n")
        return contexts

    def getTaskId(self, longname):
        self.authorization()
        context = self.searchTaskByName(longname)
        print("\n")
        if not context:
            LOGGER.warning(
                'not find any task with this name "%s"' % longname
            )
            return
        LOGGER.info('available step with this name "%s"' % longname)
        self.verboseTask(context[0])
        print("\n")
        return context

    def startMyTask(self, taskid, userid=None):
        self.authorization()
        print("\n")
        task, message = self.startTask(taskid, userid=userid)
        if not task:
            LOGGER.warning(message)
            print("\n")
            return None, message
        self.verboseTask(task)
        print("\n")
        return task, message

    def releaseKindTask(self, taskid, kind, **kwargs):
        self.authorization()
        print("\n")
        task, asset_version, message = self.releaseTask(
            taskid, kind, **kwargs
        )
        if not asset_version:
            LOGGER.warning(message)
            print("\n")
            return None, None, message
        self.verboseVersions(asset_version, tab=22)
        print("\n")
        return task, asset_version, message

    def clearTaskKinds(self, taskid, kind, userid=None):
        self.authorization()
        print("\n")
        valid, message = self.removeTaskKinds(
            taskid, kind, userid=userid
        )
        if not valid:
            LOGGER.warning(message)
            print("\n")
            return
        print("\n")
        return valid, message

    def declineUserTask(self, taskid, **kwargs):
        self.authorization()
        print("\n")
        task_context, version_context, message = self.declinedTask(
            taskid, **kwargs
        )
        if not task_context:
            LOGGER.warning(message)
            print("\n")
            return None, None, message
        self.verboseTask(task_context)
        self.verboseVersions(version_context, tab=22)
        print("\n")
        return task_context, version_context, message

    def approvedUserTask(self, taskid, **kwargs):
        self.authorization()
        print("\n")
        task_context, version_context, message = self.approvedTask(
            taskid, **kwargs
        )
        if not task_context:
            LOGGER.warning(message)
            print("\n")
            return
        self.verboseTask(task_context)
        self.verboseVersions(version_context, tab=15)
        print("\n")
        return task_context, version_context, message
    
    def getTaskHeader(self, taskid):
        self.authorization()
        currentTask = self.currentTask(taskid)
        header = self.contextHeader(currentTask)
        return header

class Versions(core.Versions):
    def __init__(self, **kwargs):
        super(Versions, self).__init__(**kwargs)

    def downloadVersions(self, **kwargs):
        categoryid = kwargs.get("categoryid", None)
        stepid = kwargs.get("stepid", None)
        taskid = kwargs.get("taskid", None)
        kind = kwargs.get("kind", None)
        versions = kwargs.get("versions", None)
        progressbar = kwargs.get("progressbar", None)

        self.authorization()
        print("\n")
        components = self.startDownloadVersions(
            categoryid=categoryid,
            stepid=stepid,
            taskid=taskid,
            kind=kind,
            versions=versions,
            progressbar=progressbar,
        )
        print("\n")
        return components

    def toDownload(self, component, dirname, **kwargs):
        readOnly = kwargs.get("readOnly", True)
        self.authorization()
        filepath = self.toDownloadComponent(
            component, dirname, readOnly=readOnly
        )
        return filepath

    def getDependencyVersions(self, task, taskname, kind="publish"):
        self.authorization()
        versions = self.searchDependencyVersions(
            task, taskname, kind=kind
        )
        return versions

    def getLatestVersionPath(self, kind, task=None):
        self.authorization()
        versionpath = self.latestVersionPath(kind, task=task)
        return versionpath

    def getVersionPath(self, assetVersion):
        self.authorization()
        versionpath = self.versionPath(assetVersion, kind=None)
        return versionpath

    def getKindVersions(self, taskid, kind):
        self.authorization()
        versions = self.searchKindVersions(taskid=taskid, kind=kind)
        return versions or list()

    def getKindVersionsContext(self, taskid, kind):
        versions = self.getKindVersions(taskid, kind)
        versionsContext = list()
        for each in versions:
            path, current_version = self.versionPath(each)
            context = {
                "version": each,
                "path": path,
                "name": current_version,
            }
            versionsContext.append(context)
        return versionsContext


class Language(core.Language):
    def __init__(self, **kwargs):
        super(Language, self).__init__(**kwargs)

    def setLanguage(self, language, key="name"):
        environments = self.environments(language, key=key)
        self.createEnviron(environments)
        return environments

    def getLanguage(self, language, key="name"):
        environments = self.searchCurrentEnvironments(
            language, key=key
        )
        print("\n")
        LOGGER.info("studio-pipe language environments")
        print("\n")
        for each in environments:
            print("%s:" % each.rjust(20), os.getenv(each))
        print("\n")
        return environments


class Discipline(core.Discipline):
    def __init__(self, **kwargs):
        super(Discipline, self).__init__(**kwargs)


class Components(core.Components):
    def __init__(self, **kwargs):
        super(Components, self).__init__(**kwargs)

    def getComponents(self, components, **kwargs):
        components = self.findComponents(components, **kwargs)
        return components


class Kinds(core.Kinds):
    def __init__(self, **kwargs):
        super(Kinds, self).__init__(**kwargs)


class Inputs(core.Inputs):
    typed = None

    def __init__(self, typed=typed, **kwargs):
        super(Inputs, self).__init__(typed, **kwargs)


class Event(core.Event):
    def __init__(self, item, **kwargs):
        super(Event, self).__init__(item, **kwargs)


class Media(core.Media):
    def __init__(self, **kwargs):
        super(Media, self).__init__(**kwargs)


if __name__ == "__main__":
    pass
