from modeling import hierarchy
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Asset(hierarchy.Asset):

    nodeType = "pipeGroomNode"
    name = "Groom"

    hierarchy = hierarchy.Asset.hierarchy + ["|Groom"]

    @classmethod
    def create(cls):
        root = cls.createNode()
        return root
