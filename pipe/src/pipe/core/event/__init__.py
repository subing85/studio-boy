
import pydoc
import importlib

# mport locate

from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Connect(object):

    context = dict()

    def __init__(self, item, **kwargs):
        self.item = item

        self.input = kwargs.get("input", dict())
        self.output = kwargs.get("output", dict())

    def redaItem(self, item=None):
        item = item or self.item
        LOGGER.info("class: %s" % item)
        try:
            module = pydoc.locate(item)
        except Exception as error:
            LOGGER.error("EventReadError: %s" % error)
            module = None
        return module

    def reload(self, item=None):
        item = item or self.item
        modelItem = ".".join(item.split(".")[0:-1])
        module = importlib.import_module(modelItem)
        importlib.reload(modelItem)
        return module

    @property
    def validAttributes(self):
        attributes = [
            "eventEnable",
            "eventName",
            "eventType",
            "eventAuthor",
        ]
        return attributes

    def hasValid(self, module=None):
        module = module or self.redaItem()
        if not module:
            return False
        for each in self.validAttributes:
            if hasattr(module, each):
                continue
            LOGGER.error(
                "EventAttributeError: could not found attribute <%s>"
                % each
            )
            return False
        if not hasattr(module, "execute"):
            LOGGER.error(
                "EventMethodError: could not found execute method in the source"
            )
            return False
        return True

    def initialize(self, **kwargs):
        module = self.redaItem()
        valid = self.hasValid(module=module)
        if not valid:
            LOGGER.error(
                "EventMethodError: could not process event execute method"
            )
            return
        module.input = kwargs.get("input")
        module.execute()
        self.output = module.output

    def setContext(self, key, value):
        self.context[key] = value


if __name__ == "__main__":
    item = "common.scripts.nameclash.Validate"
    item = "common.scripts.nameclash.Fix"

    con = Connect(item)
    con.initialize()
