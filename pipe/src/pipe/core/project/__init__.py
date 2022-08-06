# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:02:24:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core project.

import os
import copy

from pipe import utils
from pipe import resources

from pipe.core import logger
from pipe.core import ftrack
from pipe.core import inputs

LOGGER = logger.getLogger(__name__)


class Connect(ftrack.Connect):
    entity = "Project"

    def __init__(self, entity=entity, **kwargs):
        super(Connect, self).__init__(entity, **kwargs)
        self.context = dict()
        self.iconpath = resources.getIconPath()
        self.userid = os.getenv("PIPE-USER-ID")
        self.shot_input = inputs.Connect("shot")

    @property
    def projectid(self):
        env_key = self.inpt.findEnvValue("id")
        return os.getenv(env_key)

    @property
    def projectname(self):
        env_key = self.inpt.findEnvValue("name")
        return os.getenv(env_key)

    @property
    def projectfullname(self):
        env_key = self.inpt.findEnvValue("fullName")
        return os.getenv(env_key)

    @property
    def projectthumbnail(self):
        env_key = self.inpt.findEnvValue("thumbnail")
        return os.getenv(env_key)

    def environments(self, project):
        project_path = utils.setPathResolver(
            os.getenv("PROJECT-DIRNAME"),
            folders=[project.get("name")],
        )
        env_inputs = self.inpt.get()
        values = {
            "PROJECT-NAME": project.get("name"),
            "PROJECT-FULL-NAME": project.get("full_name"),
            "PROJECT-ID": str(project.get("id")),
            "PROJECT-THUMBNAIL": project.get("thumbnail")["id"],
            "PROJECT-PATH": project_path,
        }
        contexts = []
        for env, value in values.items():
            context = utils.updateInputValue(
                env_inputs, env, value, enable=True
            )
            contexts.append(context)
        return contexts

    def isInProject(self):
        if self.projectid:
            return True
        return False

    def projectSchema(self, project):
        return project.get("project_schema")

    def searchSchemas(self):
        filter = "ProjectSchema"
        contexts = self.search(filter)
        return contexts

    def searchProjects(self, reverse=True):
        contexts = self.get(filter=None)
        if reverse:
            contexts = sorted(
                contexts,
                key=lambda k: (k.get("created_at")),
                reverse=reverse,
            )
        return contexts

    def currentProject(self):
        context = self.findById(self.projectid)
        return context

    def findByName(self, name):
        filter = 'where name = "%s"' % (name)
        contexts = self.get(filter=filter)
        context = contexts.first()
        return context

    def findById(self, projectid):
        context = self.searchEntityContext(projectid)
        return context

    def createBatch(self, contexts, path=None):
        path = path or os.getenv("TEMP-USERNAME-ENVS")
        batch_file = utils.createBatch(contexts, path)
        return batch_file

    def createEnviron(self, contexs):
        utils.setEnvironment(contexs)

    def validCategories(self, project):
        return project.get("children")

    def isProjectExists(self, name):
        context = self.findByName(name)
        if context:
            return True
        return False

    def findSchema(self, name):
        filter = "ProjectSchema where name = %s" % name
        contexts = self.search(filter)
        context = contexts.first()
        return context

    def searchCategory(self, category, typed="categories"):
        category_input = inputs.Connect(typed)
        categories = category_input.get()
        if not category:
            return categories
        categories = list(
            filter(lambda k: k.get("name") == category, categories)
        )
        return categories

    # =====================================================================
    #     def shotCategory(self, context=None):
    #         context = context or self.searchCategory(None)
    #         sequence_context = list(filter(lambda k: k.get("name") == "sequence", context))
    #         shot_context = copy.deepcopy(sequence_context[0])
    #         shot_context["display-name"] = "Shots"
    #         shot_context["name"] = "shots"
    #         shot_context["order"] = 3
    #         shot_context["color"] = ([255, 85, 100],)
    #         shot_context["fontSize"] = (14,)
    #
    #         keys = ["name", "template", "fps", "fstart", "fend", "description", "assembly"]
    #         parameters = []
    #         for each in shot_context["parameter"]:
    #             if each["name"] not in keys:
    #                 continue
    #             each["parent"] = True
    #             parameters.append(each)
    #         shot_context["parameter"] = parameters
    #         return shot_context
    #
    #     def appendShotsCategory(self, context=None):
    #         context = context or self.searchCategory(None)
    #         shot_context = self.shotCategory(context=context)
    #         context.append(shot_context)
    #         return context
    # =====================================================================

    def searchCategoryByKey(self, key, value, contexts=None):
        contexts = contexts or self.searchCategory(None)
        contexts = list(
            filter(lambda k: k.get(key) == value, contexts)
        )
        if not contexts:
            return
        return contexts[0]

    def findCategory(self, category):
        project = self.findById(self.projectid)
        categories = self.validCategories(project)
        contexts = list(
            filter(lambda k: k["name"] == category, categories)
        )
        if not contexts:
            return None
        return contexts[0]

    def findValidCategory(self, category):
        config = self.searchCategory(category)
        if not config:
            return None
        context = self.findCategory(config[0].get("name"))
        return context

    def createProject(self, name, fullname, schema, **kwrags):
        thumbnail = kwrags.get("thumbnail")
        commit = kwrags.get("commit", False)
        print("\n")
        exists = self.isProjectExists(name)
        if exists:
            message = "already exists same project name <%s>" % name
            LOGGER.warning(message)
            return False, message, None
        project_schema = self.findSchema(schema)
        if not project_schema:
            message = "not found <%s> schema in ftrack" % schema
            LOGGER.warning(message)
            return False, message, None
        context = {
            "name": name,
            "full_name": fullname,
            "project_schema": project_schema,
            "created_by": None,
        }
        user_context = self.searchUserContext(self.userid)
        if user_context:
            context["created_by"] = user_context

        # create root of the project
        project = self.session.create(self.entity, context)
        if commit:
            self.session.commit()
        LOGGER.info("created new project")
        LOGGER.info("id: %s" % project["id"])
        LOGGER.info("name: %s" % project["name"])
        LOGGER.info("full name: %s" % project["full_name"])

        #  upload local thumbnail to the respective project
        thumbnail = utils.findThumbnail(thumbnail, "project")
        thumbnail_component = project.create_thumbnail(thumbnail)
        print("\n")
        thumbnail_name = os.path.basename(thumbnail)
        LOGGER.info("uploaded project thumbnail, %s" % thumbnail_name)

        # create sub-folder to the respective project
        categories = self.createCategories(
            project=project, user_context=user_context, commit=commit
        )
        LOGGER.info("create project process completed!...")
        return True, "created new project", [project, categories]

    def createCategories(self, **kwrags):
        user_context = kwrags.get(
            "user_context", self.searchUserContext(self.userid)
        )
        commit = kwrags.get("commit", False)
        project = kwrags.get("project") or self.currentProject()
        category_context = self.searchCategory(None)
        print("\n")
        LOGGER.info("create project categories")
        categories = []
        self.authorization()
        for each in category_context:
            context = {
                "project": project,
                "parent": project,
                "name": each["name"],
                "context_type": "task",
            }
            if user_context:
                context["created_by"] = user_context
            category = self.session.create(each["type"], context)
            categories.append(category)
            if commit:
                self.session.commit()
            print("\n")
            LOGGER.info("created category, %s" % category["name"])
            LOGGER.info("id: %s" % category["id"])
            # upload category icon
            iconpath = utils.setPathResolver(
                self.iconpath, folders=["%s.png" % each["name"]]
            )
            thumbnail_component = category.create_thumbnail(iconpath)
            print("\n")
            LOGGER.info(
                "uploaded category thumbnail, %s.png" % each["name"]
            )
        return categories

    def searchTaskTemplates(self):
        context = self.findById(self.projectid)
        schema = self.projectSchema(context)
        templates = schema["task_templates"]
        return templates

    def searchTaskTemplate(self, name):
        templates = self.searchTaskTemplates()
        template = list(
            filter(lambda k: k.get("name") == name, templates)
        )
        if not template:
            return None
        return template[0]

    def searchTaskStatus(self):
        context = self.findById(self.projectid)
        schema = self.projectSchema(context)
        statuses = schema["task_workflow_schema"]["statuses"]
        return statuses

    def searchAssetTypes(self):
        context = self.findById(self.projectid)
        schema = self.projectSchema(context)
        schema_type = schema["object_type_schemas"][1]["types"]
        asset_types = [each["task_type"] for each in schema_type]
        return asset_types

    def searchAssetType(self, name):
        asset_types = self.searchAssetTypes()
        contexts = list(
            filter(lambda k: k.get("name") == name, asset_types)
        )
        if not contexts:
            return None
        return contexts[0]

    def searchAllTasks(self):
        context = self.findById(self.projectid)
        schema = self.projectSchema(context)
        return schema["task_type_schema"]["types"]

    def searchTasks(self, template):
        templates = self.searchTaskTemplates()
        if template:
            contexts = list(
                filter(lambda k: k.get("name") == template, templates)
            )
        else:
            contexts = templates
        if not contexts:
            return None
        tasks = []
        for context in contexts:
            items = context["items"]
            tasks.extend([each["task_type"] for each in items])
        return tasks

    def searchStepTasks(self, step):
        filter = "Task where %s and %s" % (
            'project_id="%s"' % self.projectid,
            'parent.name="%s"' % step,
        )
        contexts = self.search(filter)
        return contexts

    def searchAssetsByType(self, typed):
        filter = 'AssetBuild where %s="%s"' % (
            "project_id",
            self.projectid,
        )
        if typed:
            filter += ' and type.name="%s"' % typed
        contexts = self.search(filter=filter)
        return contexts

    def searchAssetsByName(self, name):
        filter = 'AssetBuild where %s="%s"' % (
            "project_id",
            self.projectid,
        )
        if name:
            filter += ' and name="%s"' % name
        contexts = self.search(filter=filter)
        return contexts

    def hasAssetExists(self, name):
        context = self.searchAsset(name)
        if context:
            return True
        return False

    def searchAsset(self, name):
        filter = "AssetBuild where %s and %s" % (
            'project_id = "%s"' % self.projectid,
            'name is "%s"' % name,
        )
        context = self.search(filter=filter)
        context = context.first()
        return context

    def deleteAssets(self, name):
        contexts = self.searchAssetsByName(name)
        if not contexts:
            return False
        for context in contexts:
            self.remove(context)
        return True

    def validateTaskTemplate(self, template, step):
        if len(template["items"]) != len(step["children"]):
            return False

        steptypes = [each["type"] for each in step["children"]]

        for each in template["items"]:
            if each["task_type"] in steptypes:
                continue
            return False
            # print (each["task_type"], each["task_type"]["name"])
            # tasks.extend([each["task_type"] for each in context])
        return True

    def updateAsset(self, step, typed, template, **kwargs):
        name = kwargs.get("name") or None
        thumbnail = kwargs.get("thumbnail") or None
        description = kwargs.get("description") or None
        metadata = kwargs.get("metadata") or None

        self.authorization()
        asset_type = self.searchAssetType(typed)

        if not asset_type:
            message = (
                "not found asset type <%s> in the current project"
                % typed
            )
            LOGGER.warning(message)
            return False, message, [None, None]

        user_context = self.searchUserContext(self.userid)
        template_context = self.searchTaskTemplate(template)
        valid_template = self.validateTaskTemplate(
            template_context, step
        )

        asset_tasks = list()
        if not valid_template:
            for each in step["children"]:
                self.remove(each)
                self.session.commit()

            asset_tasks = self.createTasks(
                step, template, user_context=user_context
            )

        step["name"] = name if name else step["name"]
        step["type"] = (
            asset_type if asset_type else step["asset_type"]
        )
        step["description"] = (
            description if description else step["description"]
        )

        temlate_metadata = {
            "id": template_context["id"],
            "name": template_context["name"],
        }
        step["metadata"]["taskTemplate"] = str(temlate_metadata)

        if metadata:
            step["metadata"][metadata["key"]] = metadata["value"]

        step.session.commit()

        message = "update the asset and tasks process completed!..."
        LOGGER.info(message)
        return True, message, [step, asset_tasks]

    def createAsset(self, name, typed, template, **kwargs):
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        metadata = kwargs.get("metadata", None)

        asset_context = self.searchAsset(name)
        if asset_context:
            message = (
                "already exists same asset name <%s> in the <%s>"
                % (
                    name,
                    self.projectname,
                )
            )
            LOGGER.warning(message)
            return False, message, [None, None]

        category = self.findValidCategory("assets")
        if not category:
            message = "not found asset category in the ftrack"
            LOGGER.warning(message)
            return False, message, [None, None]

        asset_type = self.searchAssetType(typed)

        if not asset_type:
            message = (
                "not found asset type <%s> in the current project"
                % typed
            )
            LOGGER.warning(message)
            return False, message, [None, None]

        LOGGER.info("creating new asset")
        LOGGER.info("project id: %s" % self.projectid)
        LOGGER.info("project name: %s" % self.projectname)
        LOGGER.info("project full name: %s" % self.projectfullname)
        LOGGER.info("category: %s" % category["name"])
        LOGGER.info("asset type: %s" % asset_type["name"])
        current_project = self.currentProject()

        context = {
            "project": current_project,
            "parent": category,
            "name": name,
            "type": asset_type,
            "description": description,
            "metadata": dict(),
        }

        template_context = self.searchTaskTemplate(template)
        temlate_metadata = {
            "id": template_context["id"],
            "name": template_context["name"],
        }
        context["metadata"]["taskTemplate"] = str(temlate_metadata)

        if metadata:
            context["metadata"].update(metadata)

        user_context = self.searchUserContext(self.userid)
        if user_context:
            context["created_by"] = user_context

        # create asset item such as asset folder
        asset_context = self.session.create("AssetBuild", context)
        self.session.commit()
        print("\n")
        LOGGER.info("asset name: %s" % asset_context["name"])
        LOGGER.info("asset id: %s" % asset_context["id"])

        #  upload local asset thumbnail to the respective asset
        thumbnail = utils.findThumbnail(thumbnail, "assets")
        thumbnail_component = asset_context.create_thumbnail(
            thumbnail
        )
        print("\n")
        thumbnail_name = os.path.basename(thumbnail)
        LOGGER.info("uploaded asset thumbnail, %s" % thumbnail_name)
        asset_tasks = self.createTasks(
            asset_context, template, user_context=user_context
        )
        message = "create asset and tasks process completed!..."
        LOGGER.info(message)
        return True, message, [asset_context, asset_tasks]

    def createTasks(self, parent, template, **kwargs):
        user_context = kwargs.get("user_context", None)
        task_contexts = self.searchTasks(template)
        if not user_context:
            user_context = self.searchUserContext(self.userid)
        asset_tasks = []
        print("\n")
        LOGGER.info("task template type <%s>\n" % template)
        for task_contexts in task_contexts:
            context = {
                "name": task_contexts["name"],
                "type": task_contexts,
                "parent": parent,
            }
            asset_task = self.session.create("Task", context)
            self.session.commit()
            LOGGER.info("task name: %s" % asset_task["name"])
            LOGGER.info("task id: %s" % asset_task["id"])
            asset_tasks.append(asset_task)
            print("\n")
        return asset_tasks

    def searchSequenceByName(self, name):
        filter = 'Sequence where %s="%s"' % (
            "project_id",
            self.projectid,
        )
        if name:
            filter += ' and name="%s"' % name
        contexts = self.search(filter=filter)
        return contexts

    def searchSequenceById(self, id):
        filter = 'Sequence where %s="%s" and id="%s"' % (
            "project_id",
            self.projectid,
            id,
        )
        contexts = self.search(filter=filter)
        if not contexts:
            return None
        return contexts

    def searchSequence(self, name):
        filter = "Sequence where %s and %s" % (
            'project_id = "%s"' % self.projectid,
            'name is "%s"' % name,
        )
        contexts = self.search(filter=filter)
        context = contexts.first()
        return context

    def updateSequence(self, step, **kwargs):
        name = kwargs.get("name") or None
        range = kwargs.get("range") or None
        timeunit = kwargs.get("timeunit") or None

        thumbnail = kwargs.get("thumbnail") or None
        description = kwargs.get("description") or None
        metadata = kwargs.get("metadata") or None

        LOGGER.info("update exists sequence")
        LOGGER.info("project id: %s" % self.projectid)
        LOGGER.info("project name: %s" % self.projectname)
        LOGGER.info("project full name: %s" % self.projectfullname)

        step["name"] = name if name else step["name"]
        step["description"] = (
            description if description else step["description"]
        )

        step["custom_attributes"]["fps"] = (
            timeunit if timeunit else step["custom_attributes"]["fps"]
        )
        step["custom_attributes"]["fstart"] = (
            range[0] if range else step["custom_attributes"]["fstart"]
        )
        step["custom_attributes"]["fend"] = (
            range[1] if range else step["custom_attributes"]["fend"]
        )

        if timeunit:
            for shot in step["children"]:
                shot["custom_attributes"]["fps"] = timeunit

        if metadata:
            step["metadata"].update(metadata)

        step.session.commit()

        message = "update the sequence completed!..."
        LOGGER.info(message)
        return True, message, step

    def createSequence(self, name, **kwargs):
        range = kwargs.get("range") or self.getDefaultFrameRange()
        timeunit = kwargs.get("timeunit") or self.getDefaultTimeUnit()
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        metadata = kwargs.get("metadata", None)
        sequence_context = self.searchSequenceByName(name)
        if sequence_context:
            message = (
                "already exists same sequence name <%s> in the <%s>"
                % (
                    name,
                    self.projectname,
                )
            )
            LOGGER.warning(message)
            return False, message, sequence_context
        category = self.findValidCategory("sequence")
        if not category:
            message = "not found sequence category in the ftrack"
            LOGGER.warning(message)
            return False, message, None
        LOGGER.info("creating new sequence")
        LOGGER.info("project id: %s" % self.projectid)
        LOGGER.info("project name: %s" % self.projectname)
        LOGGER.info("project full name: %s" % self.projectfullname)
        LOGGER.info("category: %s" % category["name"])
        current_project = self.currentProject()
        context = {
            "project": current_project,
            "parent": category,
            "name": name,
            "description": description,
            "custom_attributes": {
                "fps": timeunit,
                "fstart": range[0],
                "fend": range[1],
            },
            "metadata": dict(),
        }

        if metadata:
            context["metadata"].update(metadata)

        user_context = self.searchUserContext(self.userid)
        if user_context:
            context["created_by"] = user_context
        sequence_context = self.session.create("Sequence", context)

        self.session.commit()

        #  upload local sequence thumbnail to the respective sequence
        thumbnail = utils.findThumbnail(thumbnail, "sequence")
        thumbnail_component = sequence_context.create_thumbnail(
            thumbnail
        )
        print("\n")
        thumbnail_name = os.path.basename(thumbnail)
        LOGGER.info(
            "uploaded sequence thumbnail, %s" % thumbnail_name
        )
        print("\n")
        message = "create new sequence process completed!..."
        LOGGER.info(message)
        return True, message, sequence_context

    def deleteSequences(self, name):
        contexts = self.searchSequenceByName(name)
        if not contexts:
            return False
        for context in contexts:
            self.remove(context)
        return True

    def getDefaultFrameRange(self):
        contexts = list(
            filter(
                lambda k: k["name"] == "frameRange",
                self.shot_input.get(),
            )
        )
        return contexts[0]["values"]

    def getTimeUnitContext(self):
        contexts = list(
            filter(
                lambda k: k["name"] == "timeUnits",
                self.shot_input.get(),
            )
        )
        if not contexts:
            return dict()
        return contexts[0]

    # =================================================================
    # def getTimeUnit(self):
    #     contexts = list(
    #         filter(
    #             lambda k: k["name"] == "timeUnits",
    #             self.shot_input.get(),
    #         )
    #     )
    #     if not contexts:
    #         return dict()
    #     return contexts[0]
    # =================================================================

    def getDefaultTimeUnitContext(self, context=None):
        context = context or self.getTimeUnitContext()
        if not context.get("value"):
            return
        timeunits = list(
            filter(
                lambda k: k["name"] == context["value"],
                context["values"],
            )
        )
        if not timeunits:
            return dict()
        return timeunits[0]

    def getDefaultTimeUnit(self):
        context = self.getDefaultTimeUnitContext()
        return context.get("value")

    def searchShotByName(self, parent, name):
        filter = 'Shot where %s="%s"' % ("project_id", self.projectid)
        if parent:
            filter += ' and parent.name="%s"' % parent
        if name:
            filter += ' and name="%s"' % name
        contexts = self.search(filter=filter)
        return contexts

    def searchShot(self, parent, name):
        contexts = self.searchShotByName(parent, name)
        context = contexts.first()
        return context

    def updateShot(self, step, template, **kwargs):
        name = kwargs.get("name") or None
        range = kwargs.get("range") or None
        timeunit = kwargs.get("timeunit") or None

        thumbnail = kwargs.get("thumbnail") or None
        description = kwargs.get("description") or None
        metadata = kwargs.get("metadata") or None

        self.authorization()
        user_context = self.searchUserContext(self.userid)
        template_context = self.searchTaskTemplate(template)
        valid_template = self.validateTaskTemplate(
            template_context, step
        )

        asset_tasks = list()
        if not valid_template:
            for each in step["children"]:
                self.remove(each)
                self.session.commit()

            asset_tasks = self.createTasks(
                step, template, user_context=user_context
            )

        LOGGER.info("update exists sequence")
        LOGGER.info("project id: %s" % self.projectid)
        LOGGER.info("project name: %s" % self.projectname)
        LOGGER.info("project full name: %s" % self.projectfullname)

        step["name"] = name if name else step["name"]
        step["description"] = (
            description if description else step["description"]
        )

        step["custom_attributes"]["fps"] = (
            timeunit if timeunit else step["custom_attributes"]["fps"]
        )
        step["custom_attributes"]["fstart"] = (
            range[0] if range else step["custom_attributes"]["fstart"]
        )
        step["custom_attributes"]["fend"] = (
            range[1] if range else step["custom_attributes"]["fend"]
        )

        if metadata:
            step["metadata"].update(metadata)

        step.session.commit()

        message = "update the shot completed!..."
        LOGGER.info(message)
        return True, message, step

    def createShot(self, name, parent, template, **kwargs):
        range = kwargs.get("range") or self.getDefaultFrameRange()
        thumbnail = kwargs.get("thumbnail", None)
        description = kwargs.get("description", None)
        fps = kwargs.get("timeunit") or self.getDefaultTimeUnit()
        metadata = kwargs.get("metadata", None)

        shot_context = self.searchShot(parent, name)
        if shot_context:
            message = (
                "already exists same shot name <%s> in the <%s>"
                % (
                    name,
                    self.projectname,
                )
            )
            LOGGER.warning(message)
            return False, message, [None, None]
        parent_contexts = self.searchSequenceByName(parent)
        if not parent_contexts:
            message = (
                "not found shot parent(sequence) <%s> in the ftrack"
                % parent
            )
            LOGGER.warning(message)
            return False, message, [None, None]
        parent_context = parent_contexts[0]
        LOGGER.info("creating new shot")
        LOGGER.info("project id: %s" % self.projectid)
        LOGGER.info("project name: %s" % self.projectname)
        LOGGER.info("project full name: %s" % self.projectfullname)
        LOGGER.info("parent: %s" % parent_context["name"])
        current_project = self.currentProject()

        context = {
            "project": current_project,
            "parent": parent_context,
            "name": name,
            "description": description,
            "custom_attributes": {
                "fps": fps,
                "fstart": range[0],
                "fend": range[1],
            },
            "metadata": dict(),
        }

        template_context = self.searchTaskTemplate(template)
        temlate_metadata = {
            "id": template_context["id"],
            "name": template_context["name"],
        }
        context["metadata"]["taskTemplate"] = str(temlate_metadata)

        if metadata:
            # context["metadata"][metadata["key"]] = metadata["value"]
            context["metadata"].update(metadata)

        user_context = self.searchUserContext(self.userid)
        if user_context:
            context["created_by"] = user_context
        shot_context = self.session.create("Shot", context)
        self.session.commit()

        #  upload local sequence thumbnail to the respective sequence
        thumbnail = utils.findThumbnail(thumbnail, "shot")
        thumbnail_component = shot_context.create_thumbnail(thumbnail)
        print("\n")
        thumbnail_name = os.path.basename(thumbnail)
        LOGGER.info("uploaded shot thumbnail, %s" % thumbnail_name)
        shot_tasks = self.createTasks(
            shot_context, template, user_context=user_context
        )
        message = "create shot process completed!..."
        LOGGER.info(message)
        return True, message, [shot_context, shot_tasks]

    def deleteShots(self, parent, name):
        contexts = self.searchShotByName(parent, name)
        if not contexts:
            return False
        for context in contexts:
            self.remove(context)
        return True


if __name__ == "__main__":
    os.environ["PROJECT-ID"] = "ad54bf94-ba83-41d3-899d-9ed3dc1ab699"

    from pprint import pprint

    con = Connect()
    con.authorization()

    # abc = con.update("Task", "024f5539-612d-4a7d-b63d-cd8ed8428f83")
    abc = con.update("Task", "46f087e9-3519-4cf8-bd62-936220ade441")
    con.verbose(abc)
    con.verbose(abc["metadata"])
    
#===================================================================================================
#     for each in abc["components"]:
# 
#         
#         if each["name"]=="mayafile":
#             print ("\n")
#             print (each["id"])
#             print (each["name"])
#             
#             metadata = each["metadata"]
#             
#             # metadata["filename"] = "generic"
#             
#             # con.session.commit()
#         
#             con.verbose(metadata)
#===================================================================================================

