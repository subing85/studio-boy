from pipe.nodes import PipeNode

from pipe.nodes import PipeModelNode
from pipe.nodes import PipeLookdevNode
from pipe.nodes import PipeGroomNode
from pipe.nodes import PipePuppetNode
from pipe.nodes import PipeMayaShotNode
from pipe.nodes import PipeMayaAssetNode

from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class PipeNode(object):

    typed = None
    filepathAttribute = None
    metadataAttribute = None
    parentAttribute = None
    childrenAttribute = None

    def __init__(self, node=None):
        self.node = node
        PipeNode.setGlobalAttributes(self.node)

    @staticmethod
    def nodeTypes():
        context = [
            {
                "nodeId": PipeMayaAssetNode.nodeId,
                "typeName": PipeMayaAssetNode.kPluginNodeTypeName,
            },
            {
                "nodeId": PipeModelNode.nodeId,
                "typeName": PipeModelNode.kPluginNodeTypeName,
            },
            {
                "nodeId": PipeLookdevNode.nodeId,
                "typeName": PipeLookdevNode.kPluginNodeTypeName,
            },
            {
                "nodeId": PipeGroomNode.nodeId,
                "typeName": PipeGroomNode.kPluginNodeTypeName,
            },
            {
                "nodeId": PipePuppetNode.nodeId,
                "typeName": PipePuppetNode.kPluginNodeTypeName,
            },
            {
                "nodeId": PipeMayaShotNode.nodeId,
                "typeName": PipeMayaShotNode.kPluginNodeTypeName,
            },
        ]
        return context

    @staticmethod
    def nodeType(node):
        from maya import cmds

        return cmds.nodeType(node)

    @staticmethod
    def openMayaMPx(node=None):
        node = node or PipeNode.node
        typed = PipeNode.nodeType(node)

        openMayaMPxs = [
            PipeMayaAssetNode,
            PipeModelNode,
            PipeLookdevNode,
            PipeGroomNode,
            PipePuppetNode,
            PipeMayaShotNode,
        ]

        for each in openMayaMPxs:
            if each.kPluginNodeTypeName != typed:
                continue
            return each
        return None

    @staticmethod
    def contextExample(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.example

    @staticmethod
    def outAttributes(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.outAttributes

    @staticmethod
    def attributeType(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.attributeType

    @staticmethod
    def attributeList(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        attributes = []
        for each in obj.attributeList():
            attributes.append(each["fn"])
        return attributes

    @staticmethod
    def allAttributeList(node=None):
        attributeList = [
            "filepath",
            "metadata",
        ] + PipeNode.attributeList(node=node)
        return attributeList

    @staticmethod
    def nodeId(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.nodeId

    @staticmethod
    def kTransformMatrixID(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.kTransformMatrixID

    @staticmethod
    def kPluginNodeTypeName(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.kPluginNodeTypeName

    @staticmethod
    def loadPlugin():
        from maya import cmds

        isLoaded = cmds.pluginInfo("pipeNodes", q=True, loaded=True)
        if isLoaded:
            LOGGER.warning('already loaded "pipeNode" plugin')
            return
        try:
            cmds.loadPlugin("pipeNodes")
        except Exception as error:
            raise ValueError(error)

    @classmethod
    def setGlobalAttributes(cls, node):
        cls.filepathAttribute = "%s.filepath" % node
        cls.metadataAttribute = "%s.metadata" % node
        cls.parentAttribute = "%s.parent" % node
        cls.childrenAttribute = "%s.children" % node

    @classmethod
    def create(cls, name, typed=None):
        typed = typed or cls.typed

        if not typed:
            LOGGER.warning("invalid node type")
            return

        from maya import cmds

        cls.loadPlugin()

        cls.node = cmds.createNode(typed, name=name)
        cls.setGlobalAttributes(cls.node)
        cls.update(node=cls.node)
        cls.setLocked(cls.node, lock=True)

    @classmethod
    def update(cls, node=None):
        node = node or cls.node
        from maya import cmds

        if not cls.filepathAttribute:
            cls.setGlobalAttributes(node)
        cls.setLocked(node, lock=False)
        cmds.setAttr(cls.filepathAttribute, "", type="string")
        cmds.setAttr(
            cls.filepathAttribute, str("manifest.json"), type="string"
        )
        cls.setLocked(node, lock=True)

    @staticmethod
    def setLocked(node, lock=True):
        from maya import cmds

        cmds.lockNode(node, lock=False)
        for each in PipeNode.allAttributeList(node=node):
            attribute = "%s.%s" % (node, each)
            # print (attribute)
            if not cmds.objExists(attribute):
                continue
            cmds.setAttr(attribute, lock=lock)
        cmds.lockNode(node, lock=lock)

    @classmethod
    def refresh(cls, node=None):
        cls.update(node=node)

    @classmethod
    def refreshMetadata(cls, node=None):
        node = node or cls.node
        cls.metadataAttribute = "%s.metadata" % node
        from maya import cmds

        if not cls.metadataAttribute:
            cls.setGlobalAttributes(node)

        cls.setLocked(node, lock=False)
        context = cmds.getAttr(cls.metadataAttribute)
        temp = PipeNode.contextExample(node)
        cmds.setAttr(cls.metadataAttribute, str(temp), type="string")
        cmds.setAttr(
            cls.metadataAttribute, str(context), type="string"
        )
        cls.setLocked(node, lock=True)

    @classmethod
    def getContext(cls, node=None, verbose=False):
        from maya import cmds

        node = node or cls.node
        cls.metadataAttribute = "%s.metadata" % node
        context = cmds.getAttr(cls.metadataAttribute)
        context = ast.literal_eval(context) if context else dict()
        if verbose:
            print(json.dumps(context, indent=4))
        return context

    @staticmethod
    def getLocation(node=None):
        node = node or PipeMayaAssetNode.node
        from maya import cmds
