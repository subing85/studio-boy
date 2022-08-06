from common.attributes import SearchDefultTransforms
from common.attributes import SearchUnLockedTransformAttributes


class IsDefault(object):

    eventEnable = True
    eventName = "queryIsDefaultAttribute"
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
        invalidAttributes = SearchDefultTransforms.doIt()
        if invalidAttributes:
            return (
                False,
                "could not found default values ",
                invalidAttributes,
            )
        return (
            True,
            "all transform object attributes are default values",
            invalidAttributes,
        )


class SetDefault(object):

    eventEnable = True
    eventName = "setDefaultAttribute"
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
        from maya import cmds

        invalidAttributes = SearchDefultTransforms.doIt()
        if not invalidAttributes:
            return (
                True,
                "all transform object attributes are default values",
                invalidAttributes,
            )
        attributes = []
        for attribute, value, default in invalidAttributes:
            cmds.setAttr(attribute, default)
            attributes.append([attribute, default, default])
        return True, "set to default values ", attributes


class IsLocked(object):

    eventEnable = True
    eventName = "queryIsLockedAttribute"
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

        invalid_nodes = SearchUnLockedTransformAttributes.doIt()
        if invalid_nodes:
            return (
                False,
                "geometry transformation attributes are not locked",
                invalid_nodes,
            )
        return (
            True,
            "all geometry transformation attributes are locked",
            invalid_nodes,
        )


class SetLocked(object):

    eventEnable = True
    eventName = "setLockedAttribute"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        valid, message, nodes = cls.locked()
        cls.output["valid"] = valid
        cls.output["message"] = message
        cls.output["nodes"] = nodes

    @classmethod
    def locked(cls):
        from maya import cmds

        cmds.undoInfo(openChunk=True)
        invalidNodes = SearchUnLockedTransformAttributes.doIt()
        if not invalidNodes:
            return (
                True,
                "all geometry transformation attributes are locked",
                invalidNodes,
            )

        nodelist = []
        for node, attribute in invalidNodes:
            attribute = "%s.%s" % (node, attribute)
            lock = cmds.getAttr(attribute, lock=True)
            if lock:
                continue
            cmds.setAttr(attribute, lock=True)
            nodelist.append(
                "locked transformation attribute, %s" % attribute
            )
        cmds.undoInfo(closeChunk=True)
        return (
            True,
            "locked un-locked geometry transformation attributes",
            nodelist,
        )
