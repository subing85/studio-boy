from puppet.hierarchy import Asset


class Validate(object):

    eventEnable = True
    eventName = "puppetHierarchy"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.check()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def check(cls):
        invalid_nodes = Asset.validate()
        if not invalid_nodes:
            return True, "hierarchy is prefect", list()
        result = []
        for each in invalid_nodes:
            result.append([each, invalid_nodes[each]])
        return False, "found wrong hierarchy", result
