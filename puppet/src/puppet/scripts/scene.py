from apis.studio import Versions
from common.collect import Context
from common.mayaScene import Scene
from common.scripts.scene import MayaSceneExport


class PuppetScene(MayaSceneExport):

    eventEnable = True
    eventName = "groomShaderScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        super(PuppetScene, cls).execute()

        task = cls.input["task"]
        filepath = cls.output["mayaScene"]

        dirname = Versions().kindPath("work", task=task)
        sourceimage = cls.output["config"]["relative-path"]

        Scene.remapping(
            filepath,
            dirname,
            create=False,
            relativedirname=sourceimage,
        )


class ImportPuppetShader(object):

    eventEnable = True
    eventName = "importPuppetShader"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "puppet").lower()
        outputLinks = cls.input.get("outputLinks")

        Context.configContext(taskType, "shader", "images")
        if not Context.config:
            LOGGER.info("invalid")
            return

        version = cls.currentVersion(cls, outputLinks)
        if not version:
            LOGGER.info("invalid version dependency(lookdev) version")
            return

        CreatePuppetShader.doIt(
            task=task, version=version, context=Context.config
        )

    @staticmethod
    def currentVersion(self, linkOutList):
        versions = linkOutList.get("versions")
        widget = linkOutList.get("widget")

        text = widget.currentText()
        if text not in linkOutList.get("versions"):
            return
        return linkOutList["versions"][text]



class PuppetPose(object):

    eventEnable = True
    eventName = "puppetPose"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "modeling").lower()
        LOGGER.info("%s, %s" % (task, taskType))

        Context.configContext(taskType, "pose", "sceneDescription")
        if not Context.config:
            LOGGER.info("invalid")
            return

        parent_name = task["parent"]["name"]

        dirname = Versions().kindPath("work", task=task)
        extension = Context.config.get("extension")
        label = Context.config.get("label")
        output = resources.setPathResolver(
            dirname, folders=["%s.%s" % (label, extension)]
        )

        input = {
            "nodetype": Context.config.get("nodetype"),
            "pattern": Context.config.get("pattern"),
            "mode": Context.config.get("mode"),
        }

        filepath = Scene.exportPuppetPose(output, **input)

        cls.output["pose"] = filepath
        LOGGER.info("success, %s" % filepath)
        return
