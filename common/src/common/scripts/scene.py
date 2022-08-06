import os
import time

from common import resources
from pipe.core import logger

from apis.studio import Versions

from apis.studio import Tasks
from common.collect import Context
from common.hierarchy import Shot
from common.mayaScene import Scene
from common.pipefile import Create
from pipe.core.tasks import manifest

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class MayaSceneExport(object):

    eventEnable = True
    eventName = "mayaScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "modeling").lower()
        LOGGER.info("%s, %s" % (task, taskType))

        Context.configContext(taskType, "scene", "mayaScene")
        if not Context.config:
            LOGGER.info("invalid")
            return

        parent_name = task["parent"]["name"]

        dirname = Versions().kindPath("work", task=task)
        extension = Context.config.get("extension", "ma")

        if Context.config.get("entity-name"):
            filename = parent_name
        elif Context.config.get("label"):
            filename = Context.config.get("label")
        else:
            filename = parent_name

        output = resources.setPathResolver(
            dirname, folders=["%s.%s" % (filename, extension)]
        )

        input = {
            "format": Context.config.get("format"),
            "readOnly": False,
            "preserve_rferences": Context.config.get("preserve_rferences"),
        }

        filepath = Scene.exportScene(output, **input)
        cls.output["mayaScene"] = filepath
        cls.output["config"] = Context.config

        LOGGER.info("success, %s" % filepath)
        return


class BuildScene(object):

    eventEnable = True
    eventName = "buildScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()
    
    
    @staticmethod
    def sequence(task):
        return task["link"][2]["name"]
    
    @staticmethod
    def shot(task):
        return task["link"][3]["name"]

    @classmethod
    def execute(cls):
        items = cls.input.get("items")
        task = cls.input.get("task")
        taskType = cls.input.get("taskType")
        timestamp = cls.input.get("timestamp")
        
        download = cls.input.get("download")
        
        print ("download", download)
        
        if download:
            BuildScene.download(task["id"], items)
            # start to download
            
        return

        shotNode = Shot.getParent()

        if shotNode.isValid():
            Scene.updateFiles(items, rootNode=shotNode.name)

        else:
            sequence = BuildScene.sequence(task)
            shot = BuildScene.shot(task)
    
            kindPath = Versions().kindPath("work", task=task)
            comment = "%s shot build" % taskType
            manifest.create(task, kindPath, comment=comment, metadata=None, timestamp=timestamp)
            filepath = Create.resolvePath(kindPath, suffix="%s_%s" % (sequence, sequence))
            name = "%s_%s_%s" % (taskType, sequence, shot)

            Scene.newScene()
            parent = Shot.createNode(taskType, name)
            context = BuildScene.getContext(items)
            Scene.importFiles(context, parent, typed="reference")
            Scene.saveScene(filepath, timestamp=timestamp, force=True)

    @staticmethod
    def getContext(items):
        context= list()
        for each in items:
            entityContext = {
                "filepath": each.filepath,
                "name": each.name,
                }
            context.append(entityContext)
        return context
    
    @staticmethod
    def download(taskid, items):
        vers = Versions()
        for item in items:
            if not item.isCheckState():
                continue
            if os.path.isfile(item.filepath):
                LOGGER.info("already exists, %s" % item.filepath)
                continue
            vers.downloadVersions(
                taskid=item.taskEntity["id"],
                kind=item.kindName,
                versions=item.versionName,
                progressbar=None
            )


class LoadScene(object):
    eventEnable = True
    eventName = "loadScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        
        combobox = cls.input["widget"]
        
        taskid = Shot.getCurrentTaskId()
        if not taskid:
            return
        
        header = Tasks().getTaskHeader(taskid)
        
        for x in range(combobox.count()) :
            if header != combobox.itemText(x):
                continue
            combobox.setCurrentIndex(x)
        else:
            LOGGER.warning("Could not find shot, %s" % header)
            

        
        