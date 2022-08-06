from pipe import utils
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class History(object):
    context = list()
    live = list()
    widgetitem = None
    entity = False
    mode = None
    pin = False
    category = None
    sequence = None

    def __init__(self):
        History.__init__(self)

    @classmethod
    def setWidget(cls, widgetitem):
        cls.widgetitem = widgetitem

    @classmethod
    def setEntity(cls, entity):
        cls.entity = entity
        cls.mode = "update" if entity else "create"

    @classmethod
    def setPin(cls, pin):
        cls.pin = pin

    @classmethod
    def setLive(cls, item):
        cls.live = item

    @classmethod
    def setCategory(cls, category):
        cls.category = category

    @classmethod
    def setSequence(cls, sequence):
        cls.sequence = sequence

    @classmethod
    def add(cls, item):
        item.extend(
            [
                {"category": cls.category},
                {"widgetitem": cls.widgetitem},
                {"entity": cls.entity},
                {"pin": cls.pin},
                {"mode": cls.mode},
            ]
        )
        if cls.sequence:
            item.append({"sequence": cls.sequence})
        cls.context.append(item)

    @classmethod
    def getContext(cls, widgetitem=None):
        widgetitem = widgetitem or cls.widgetitem
        context = list()
        for each in cls.context:
            contexts = utils.searchContext(
                each, "widgetitem", value=widgetitem
            )
            if contexts:
                context = each.copy()
                break
        return context

    @classmethod
    def clear(cls):
        cls.context = list()

    @classmethod
    def update(cls, key, value, live=None):
        live = live or cls.live
        if live not in cls.context:
            LOGGER.warning("not found context in the history context")
            return
        index = cls.context.index(live)
        for each in cls.context[index]:
            if key not in each:
                continue
            each[key] = value

    @classmethod
    def get(cls, all=True):
        context = cls.context if all else [cls.live]
        return context

    @classmethod
    def remove(cls, item=None):
        item = item or cls.live
        if item not in cls.context:
            LOGGER.warning("not found context in the history context")
            return
        cls.context.remove(item)

    @classmethod
    def validate(cls, all=True, create=True, entity=True):
        history_context = cls.get(all=all)
        if not history_context:
            message = "not found step item to create!..."
            return False, message, None
        for each in history_context:
            entity_context = utils.specialSearchContext(
                each, "entity", value=None, default=False
            )
            if not entity_context:
                message = (
                    "invalid history context, not find entity key!..."
                )
                return False, message
            if create:
                if entity:
                    if entity_context["entity"] is True:
                        message = "already created, try with newly added item!..."
                        return False, message
                pin_context = utils.specialSearchContext(
                    each, "pin", value=None, default=False
                )
                if not pin_context:
                    message = "invalid history context, not find pin key!..."
                    return False, message
                if not pin_context.get("pin"):
                    message = "save the step item use Pin Button and try!..."
                    return False, message
            else:
                if entity_context["entity"] is False:
                    message = "current item is newly added item, try with already created item!..."
                    return False, message
        return True, None

    @classmethod
    def toContext(cls, history):
        context = dict()
        value_contexts = utils.searchContext(
            history, "name", value=None
        )
        for each in value_contexts:
            if not each.get("value"):
                continue
            if each.get("meatadata"):
                data = {"key": each["meatadata"]}
                if each.get("strDict"):
                    endfield = each["field"].split(".")[-1]
                    data.update({"value": {endfield: each["value"]}})
                else:
                    data.update({"value": each["value"]})
                context.setdefault(each["name"], data)
            else:
                context.setdefault(each["name"], each["value"])
        category_context = utils.specialSearchContext(
            history, "category", value=None, default=None
        )
        entity_context = utils.specialSearchContext(
            history, "entity", value=None, default=False
        )
        tag_context = utils.specialSearchContext(
            history, "tag", value=None, default=False
        )
        widgetitem_context = utils.specialSearchContext(
            history, "widgetitem", value=None, default=None
        )
        sequence_context = utils.specialSearchContext(
            history, "sequence", value=None, default=None
        )
        context.update(category_context)
        context.update(entity_context)
        context.update(tag_context)
        context.update(widgetitem_context)
        context.update(sequence_context)
        step_context = {
            "step": widgetitem_context["widgetitem"].entity
        }
        context.update(step_context)
        return context


if __name__ == "__main__":
    pass
