from common.shader import SearchShaders
from common.shader import SetDefultShader


class IsDefault(object):

    eventEnable = True
    eventName = "queryIsDefaultShader"
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
        invalidShader = SearchShaders.doIt()
        if invalidShader:
            return False, "found invalid shader", invalidShader
        return True, "not found invalid shader", invalidShader


class SetDefault(object):
    eventEnable = True
    eventName = "setDefaultShader"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.default()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def default(cls):
        valid, result = SetDefultShader.doIt(geometries=list())
        return (
            valid,
            "Set the defult shader to the all geometries",
            result,
        )
