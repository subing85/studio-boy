from lookdev.shader import SearchLookdevShader
from lookdev.shader import SearchBrokenShaders


class IsLookdevShader(object):
    eventEnable = True
    eventName = "queryIsLookdevShader"
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
        context = SearchLookdevShader.doIt()
        if not context:
            return (
                True,
                "all geometries are assign to lookdev shader",
                list(),
            )
        result = []
        for each in context:
            result.append([each, context[each]])
        return False, "wrong shader assignment exists", result


class IsBrokenLookdevShader(object):
    eventEnable = True
    eventName = "queryIsBrokenLookdevShader"
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
        context = SearchBrokenShaders.doIt()
        if not context:
            return True, "could not found any broken shader", list()
        result = []
        for each in context:
            result.append([each, context[each]])
        return False, "found broken shaders", result
    

    
