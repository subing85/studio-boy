from apis import studio
from common import resources
from pipe.core import logger
from apis.studio import Versions
from common.pipefile import Create
from common.collect import Context
from common.mayaRender import LiveRender

LOGGER = logger.getLogger(__name__)


class LookdevLook(object):

    eventEnable = True
    eventName = "lookdevLook"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "lookdev").lower()

        Context.configContext(taskType, "image", "render")
        if not Context.config:
            return

        userContext = Context.userContext()
        taskContext = Context.taskContext(task)

        temp_directory = Create.tempDirectory(taskType)

        parent_name = task["parent"]["name"]

        filepath = resources.setPathResolver(temp_directory, folders=[parent_name])
        foregroundi = cls.createForeground(cls, filepath, **Context.config)

        projecti = resources.getProjectImage(task["project"])
        imageContext = Context.imageContext(projecti, foregroundi)

        context = imageContext
        context["watermarks"] = [userContext, taskContext]

        filepath = Versions().kindPath("work", task=task)
        filename = Context.config.get("label", parent_name)
        extension = Context.config.get("outputExtension", "jpg")

        output = resources.setPathResolver(
            filepath, folders=["%s.%s" % (filename, extension)]
        )

        Create.directory(output)

        meda = studio.Media()
        meda.createImage(output, **context)
        LOGGER.info("success, %s" % output)
        cls.output["image"] = output

    def createForeground(self, filepath, **kwargs):
        inputs = {
            "fstart": kwargs.get("frame", 1001),
            "fend": kwargs.get("frame", 1001),
            "padding": kwargs.get("padding", 5),
            "extension": kwargs.get("extension", "tga"),
            "compression": kwargs.get("compression", "Targa"),
            "widthHeight": kwargs.get("resolution", [1024, 1024]),
            "percent": kwargs.get("percent", 100),
            "quality": kwargs.get("quality", 100),
            "filepath": filepath,
        }
        images = LiveRender.FrameByFrame(**inputs)
        return images[-1]
