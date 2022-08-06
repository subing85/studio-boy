from apis import studio
from common import resources
from pipe.core import logger

from apis.studio import Versions

from common.collect import Context
from common.pipefile import Create
from common.mayaRender import TimeUnit
from common.mayaRender import Playblast
from common.mayaRender import RenderCamera

LOGGER = logger.getLogger(__name__)


class ModelMovie(object):

    eventEnable = True
    eventName = "modelMovie"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input.get("task")
        taskType = cls.input.get("taskType", "modeling").lower()
        LOGGER.info("%s, %s" % (task, taskType))

        Context.configContext(taskType, "movie", "playblast")
        if not Context.config:
            return

        output = cls.createMovie(cls, task, taskType, Context.config)
        cls.output["movie"] = output
        LOGGER.info("success, %s" % output)
        return

    def createMovie(self, task, taskType, config):

        parent_name = task["parent"]["name"]
        temp_directory = Create.tempDirectory(taskType)

        filepath = resources.setPathResolver(
            temp_directory, folders=[parent_name]
        )
        image_sequence = self._createImageSequence(
            self, task, filepath, **config
        )

        filepath = Versions().kindPath("work", task=task)

        filename = Context.config.get("label", parent_name)
        extension = config.get("outputExtension", "mov")

        output = resources.setPathResolver(
            filepath, folders=["%s.%s" % (filename, extension)]
        )

        meda = studio.Media()

        movie_out = meda.createMove(
            image_sequence,
            output,
            fps=TimeUnit.scene(),
            resolution=config.get("resolution"),
        )

        Create.removeAll(temp_directory)
        return movie_out

    def _createImageSequence(self, task, filepath, **kwargs):
        foregrounds = self.createImageSequence(
            self, task, filepath, **kwargs
        )
        return foregrounds

    def createImageSequence(self, task, filepath, **kwargs):
        fstart, fend = kwargs.get("fstart", 1001), kwargs.get(
            "fend", 1090
        )
        kstart, kend = kwargs.get("kstart", 0), kwargs.get(
            "kend", -360
        )
        padding = kwargs.get("padding", 5)

        LOGGER.info("collecting context")
        userContext = Context.userContext()
        taskContext = Context.taskContext(task)

        projecti = resources.getProjectImage(task["project"])
        LOGGER.info(projecti)

        RenderCamera.create(fstart, fend, kstart, kend)

        foregrounds = list()
        fps = TimeUnit.scene()
        LOGGER.info("creating image sequence")

        media = studio.Media()

        for frame in range(fstart, fend + 1):
            inputs = {
                "format": kwargs.get("format", "image"),
                "widthHeight": kwargs.get("resolution", [1024, 1024]),
                "fstart": frame,
                "fend": frame,
                "extension": kwargs.get("extension", "tif"),
                "clearCache": kwargs.get("clearCache", False),
                "viewer": kwargs.get("viewer", False),
                "showOrnaments": kwargs.get("showOrnaments", False),
                "fp": TimeUnit.scene(),
                "percent": kwargs.get("percent", 100),
                "compression": kwargs.get("compression", "tif"),
                "quality": kwargs.get("quality", 100),
                "filepath": filepath,
            }

            images = Playblast.FrameByFrame(**inputs)

            if not images:
                LOGGER.error("not able to create playblast image")
                continue
            foreground = images[-1]

            imageContext = Context.imageContext(projecti, foreground)
            frameContext = Context.frameContext(
                [fstart, fend], frame, fps
            )
            context = imageContext
            context["watermarks"] = [
                userContext,
                taskContext,
                frameContext,
            ]

            media.createImage(foreground, **context)
            foregrounds.append(foreground)

        RenderCamera.delete()
        Create.removeFilepath(projecti)

        return foregrounds
