from pipe.core import logger
from common.animCurve import SearchAnimCurve

LOGGER = logger.getLogger(__name__)


class IsExists(object):

    eventEnable = True
    eventName = "queryIsAnimationExists"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.collect()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def collect(cls):
        animations = SearchAnimCurve.doIt()
        if animations:
            return (
                False,
                "found animation curves in your scene",
                animations,
            )
        return (
            True,
            "could not found animation curves in your scene",
            animations,
        )


class Delete(object):

    eventEnable = True
    eventName = "deleteAnimation"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.collect()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def collect(cls):
        from maya import cmds

        cmds.undoInfo(openChunk=True)
        animations = SearchAnimCurve.doIt()
        result = []
        for node, animcurve in animations:
            cmds.delete(animcurve)
            result.append(animcurve)
        cmds.undoInfo(closeChunk=True)
        return (
            True,
            "delete the animation curves from the scene",
            result,
        )
