from apis import studio
from common import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Context(object):

    taskType = None
    config = dict()

    @classmethod
    def configContext(cls, taskType, name, typed):
        data = resources.getInputData(taskType)
        context = list(
            filter(
                lambda k: k["name"] == name and k["type"] == typed,
                data,
            )
        )
        if not context:
            LOGGER.warning(
                "could not found valid input taskType <%s> resource"
                % taskType
            )
            return
        cls.taskType = taskType
        cls.config = context[0]
        return cls.config

    @classmethod
    def userContext(cls, watermark=None):

        watermark = watermark or cls.config["watermark"]
        context = resources.searchContext(
            watermark, "name", value="user"
        )
        context = context[0].copy() if context else dict()

        task = studio.Tasks()
        task.authorization()
        user = task.currentUser()
        user_name = "%s %s" % (
            user.get("first_name"),
            user.get("last_name"),
        )
        user_type = task.getUserSecurityRole(user)
        marks = [
            {"email": user["email"]},
            {"name": user_name},
            {"type": user_type},
            {"date": resources.getDateTime()},
        ]
        context.pop("name")
        context["marks"] = marks
        return context

    @classmethod
    def taskContext(cls, task, watermark=None):
        watermark = watermark or cls.config["watermark"]
        context = resources.searchContext(
            watermark, "name", value="task"
        )
        context = context[0].copy() if context else dict()

        if task["parent"]["type"]:
            marks = [
                {"project": task["project"]["full_name"]},
                {"name": task["parent"]["name"]},
                {"id": task["id"]},
                {"category": task["link"][1]["name"]},
                {"type": task["parent"]["type"]["name"]},
                {"task": task["type"]["name"]},
            ]
        else:
            marks = [
                {"project": task["project"]["full_name"]},
                {"name": task["parent"]["name"]},
                {"id": task["id"]},
                {"category": task["link"][1]["name"]},
                {"task": task["type"]["name"]},
            ]
        context.pop("name")
        context["marks"] = marks
        return context

    @classmethod
    def frameContext(cls, frameRange, frame, fps, watermark=None):
        watermark = watermark or cls.config["watermark"]
        context = resources.searchContext(
            watermark, "name", value="frame"
        )
        context = context[0].copy() if context else dict()
        marks = [
            {"Range": "%s-%s" % (frameRange[0], frameRange[1])},
            {"Frame": frame},
            {"FPS": fps},
        ]
        context.pop("name")
        context["marks"] = marks
        return context

    @classmethod
    def imageContext(cls, projecti, foregroundi, config=None):
        config = config or cls.config

        backgroundi = resources.getBackgroundImage(
            cls.taskType.lower()
        )
        studioi = resources.getStudioImage()

        context = {
            "background": backgroundi,
            "foreground": foregroundi,
            "project": projecti,
            "studio": studioi,
            "resolution": config.get("resolution"),
            "project_size": config.get("project_size"),
            "studio_size": config.get("studio_size"),
            "project_positions": config.get("project_positions"),
            "studio_positions": config.get("studio_positions"),
        }
        return context
