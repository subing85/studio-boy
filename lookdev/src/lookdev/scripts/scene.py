from common import resources
from pipe.core import logger
from apis.studio import Versions
from common.collect import Context
from common.mayaScene import Scene

LOGGER = logger.getLogger(__name__)


class LookdevShader(object):

    eventEnable = True
    eventName = "lookdevShaderScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "lookdev").lower()
        LOGGER.info("%s, %s" % (task, taskType))

        for each in ["mayaShaderScene", "sceneDescription"]:

            Context.configContext(taskType, "scene", each)
            if not Context.config:
                LOGGER.info("invalid")
                return

            dirname = Versions().kindPath("work", task=task)
            extension = Context.config.get("extension")
            label = Context.config.get("label")
            output = resources.setPathResolver(
                dirname, folders=["%s.%s" % (label, extension)]
            )

            input = {
                "format": Context.config.get("format"),
                "readOnly": False,
                "preserve_rferences": Context.config.get("preserve_rferences"),
            }

            filepath = None
            sourceimage = Context.config.get("relative-path")
            if each == "mayaShaderScene":
                filepath = Scene.exportShader(output, **input)
                Scene.remapping(
                    filepath,
                    dirname,
                    create=True,
                    relativedirname=sourceimage,
                    relativepath=True,
                )

            if each == "sceneDescription":
                filepath = Scene.exportShaderSD(output, sourceimage, **input)

            cls.output[each] = filepath
            LOGGER.info("success, %s" % filepath)

        return


class LookdevScene(object):

    eventEnable = True
    eventName = "lookdevScene"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):

        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "lookdev").lower()
        LOGGER.info("%s, %s" % (task, taskType))

        Context.configContext(taskType, "scene", "mayaScene")
        if not Context.config:
            LOGGER.info("invalid")
            return

        parent_name = task["parent"]["name"]

        dirname = Versions().kindPath("work", task=task)
        extension = Context.config.get("extension", "ma")
        output = resources.setPathResolver(
            dirname, folders=["%s.%s" % (parent_name, extension)]
        )

        input = {
            "format": Context.config.get("format"),
            "readOnly": False,
            "preserve_rferences": Context.config.get("preserve_rferences"),
        }

        filepath = Scene.exportScene(output, **input)
        sourceimage = Context.config.get("relative-path")
        relativepath = resources.setPathResolver(dirname, folders=[sourceimage])
        Scene.remapping(
            filepath,
            dirname,
            create=False,
            relativedirname=sourceimage,
        )

        cls.output["mayaScene"] = filepath
        LOGGER.info("success, %s" % filepath)
        return
