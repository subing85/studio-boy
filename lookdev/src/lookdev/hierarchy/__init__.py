from modeling import hierarchy
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Asset(hierarchy.Asset):

    nodeType = "pipeLookdevNode"
    name = "Lookdev"

    hierarchy = hierarchy.Asset.hierarchy + ["|Lookdev"]

    @classmethod
    def create(cls):
        root = cls.createNode()
        return root
