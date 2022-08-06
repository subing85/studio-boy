from common.mayaScene import GetAllHistory
from common.mayaScene import DeleteAllHistory
from common.mayaScene import GetNonDeformHistory
from common.mayaScene import DeleteAllNonDeformHistory


class Validate(object):

    eventEnable = True
    eventName = "queryHistory"
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
        context = GetAllHistory.doIt()
        if not context:
            return True, "could not found any history", list()
        result = []
        for each in context:
            result.append([each, context[each]])
        return False, "found history", result


class ValidateNonDeform(object):
    eventEnable = True
    eventName = "queryHistory"
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

        context = GetNonDeformHistory.doIt()
        if not context:
            return True, "could not found any history", list()
        result = []
        for each in context:
            result.append([each, context[each]])
        return False, "found history", result


class DeleteHistory(object):

    eventEnable = True
    eventName = "deleteHistory"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.delete()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def delete(self):
        context = DeleteAllHistory.doIt()
        if not context:
            return False, "could not found any history", list()
        result = []
        for each in context:
            result.append([each, context[each]])
        return True, "deleted history from the scene", result


class DeleteNonDeformHistory(object):

    eventEnable = True
    eventName = "deleteNoneHistory"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.delete()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def delete(self):
        context = DeleteAllNonDeformHistory.doIt()
        if not context:
            return False, "could not found any history", list()
        result = []
        for each in context:
            result.append([each, context[each]])
        return True, "deleted history from the scene", result
