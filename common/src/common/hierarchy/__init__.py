from pipe.core import logger
from pipe.nodes import GetNode
from pipe.nodes import PipeNode

LOGGER = logger.getLogger(__name__)


class Asset(object):

    nodeType = None
    name = None
    hierarchy = None

    @classmethod
    def hasExists(cls):
        nodes = Asset.get(referenced=True, nodeType=cls.nodeType)
        exists = True if nodes else False
        return exists

    @classmethod
    def createNode(cls, nodeType=None, name=None):
        print ("nodeType", nodeType)
        nodeType = nodeType or cls.nodeType
        name = name or cls.name
        if not nodeType:
            raise Exception("invalid node type <%s>" % cls.nodeType)
        PipeNode.create(typed=nodeType, name=name)
        return PipeNode.node

    @staticmethod
    def get(referenced=False, nodeType=None):
        from maya import cmds

        nodeType = nodeType or Asset.nodeType
        nodes = cmds.ls(type=nodeType)
        if referenced:
            return nodes
        for node in nodes:
            if not cmds.referenceQuery(node, isNodeReferenced=True):
                continue
            nodes.remove(node)
        return nodes
    
    @staticmethod
    def getNodeByType(nodeType, referenced=False, first=False):
        nodes = Asset.get(nodeType=nodeType, referenced=referenced)
        result = nodes[0] if nodes and first else nodes
        return result

    @staticmethod
    def delete(nodes):
        from maya import cmds

        for each in nodes:
            if cmds.nodeType(each) != Asset.nodeType:
                LOGGER.warning(
                    "invalid %s %s" % (each, Asset.nodeType)
                )
                continue
            if cmds.referenceQuery(each, isNodeReferenced=True):
                continue
            PipeNode.delete(each)

    @staticmethod
    def getNode():
        nodes = Asset.get(referenced=True)
        return nodes[0]

    @classmethod
    def validate(cls):
        from maya import cmds

        invalid_nodes = {}
        for each in cls.hierarchy:
            if cmds.objExists(each):
                continue
            invalid_nodes.setdefault("missing", []).append(each)
        top_level_nodes = cmds.ls(assemblies=True)
        unwant_nodes = []
        validNodes = cmds.ls(cls.hierarchy) + cls.defaultNodes()
        for node in top_level_nodes:
            print(node, cls.defaultNodes())
            if node in validNodes:
                continue
            invalid_nodes.setdefault("unwanted", []).append(node)
        return invalid_nodes

    @staticmethod
    def defaultNodes():
        from maya import cmds

        nodes = cmds.ls(defaultNodes=True)
        nodes.extend(["persp", "top", "front", "side"])
        return nodes

    @staticmethod
    def getLookdevNodes(referenced=False, first=False):
        result = Asset.getNodeByType(
            "pipeLookdevNode", referenced=referenced, first=first
        )
        return result


class Shot(Asset):
    sceneTypes = {"layout": 0, "animation": 1, "render": 2}

    sceneTypeAttribute = None

    @classmethod
    def createNode(cls, sceneType=None, name=None):
        from maya import cmds
        if sceneType not in cls.sceneTypes:
            raise Exception("invalid scene node type")
        PipeNode.create(typed="pipeShotNode", name=name)
        cls.sceneTypeAttribute = "%s.sceneType" % PipeNode.node
        cmds.setAttr(cls.sceneTypeAttribute, cls.sceneTypes[sceneType])
        cmds.setAttr(cls.sceneTypeAttribute, lock=True)
        return PipeNode.node
    
    @classmethod
    def nodeUpdate(cls, node, sceneType):
        from maya import cmds
        cls.sceneTypeAttribute = "%s.sceneType" % node
        if sceneType not in cls.sceneTypes:
            raise Exception("invalid scene node type.")
        if not cmds.objExists(cls.sceneTypeAttribute):
            raise Exception("invalid scene node type attribute.")
        cmds.setAttr(cls.sceneTypeAttribute, lock=False)
        cmds.setAttr(cls.sceneTypeAttribute, cls.sceneTypes[sceneType])
        cmds.setAttr(cls.sceneTypeAttribute, lock=True)

    @classmethod
    def getRootNode(cls):
        rootNode = PipeNode.searchFirstNode()
        return rootNode

    @classmethod
    def getCurrentTaskId(cls):
        parentNode = cls.getRootNode()
        if not parentNode:
            LOGGER.warning("could not find root node")
            return
        sceneNode = GetNode(parentNode)
        taskId = sceneNode.taskId()
        return taskId
    
    @classmethod
    def getChidren(cls):
        sceneNode = GetNode(cls.getRootNode())
        context = []
        if sceneNode.isNull():
            LOGGER.warning("could not find root node")
            return context
        for child in sceneNode.children():
            childContext = sceneNode.getChildContext(child)
            if not childContext:
                continue
            context.append(childContext)
        return context
    
    @classmethod
    def getParent(cls):
        parentNode = GetNode(cls.getRootNode())
        if parentNode.isNull():
            LOGGER.warning("could not find parent node")
            return None
        return parentNode

    @classmethod
    def setNode(cls, node):
        pipeNode = GetNode(node)
        return pipeNode