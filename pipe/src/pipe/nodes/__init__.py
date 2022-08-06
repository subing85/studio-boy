import ast
import json

from pprint import pprint

from pipe.core import logger

from pipe.nodes.plugins import PipeShotNode
from pipe.nodes.plugins import PipeModelNode
from pipe.nodes.plugins import PipeGroomNode
from pipe.nodes.plugins import PipePuppetNode
from pipe.nodes.plugins import PipeCameraNode
from pipe.nodes.plugins import PipeLookdevNode

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
    def openMayaMPxs():
        mayaMPxs = [
            PipeShotNode,
            PipePuppetNode,
            PipeModelNode,
            PipeCameraNode,
            PipeLookdevNode,
            PipeGroomNode,
        ]
        return mayaMPxs

    @staticmethod
    def nodeTypes(verbose=False):
        contextList = []
        for each in PipeNode.openMayaMPxs():
            context = {
                "nodeId": each.nodeId,
                "typeName": each.kPluginNodeTypeName,
            }
            contextList.append(context)
        if verbose:
            pprint(contextList)
        return contextList

    @staticmethod
    def nodeType(node):
        from maya import cmds

        return cmds.nodeType(node)

    @staticmethod
    def openMayaMPx(node=None):
        node = node or PipeNode.node
        typed = PipeNode.nodeType(node)
        for each in PipeNode.openMayaMPxs():
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
        if not obj:
            raise Exception("invalid pipe node object, check the node type")
        attributes = [each["fn"] for each in obj.attributeList()]
        return attributes

    @staticmethod
    def allAttributeList(node=None):
        attributeList = [
            "filepath",
            "metadata",
            "parent",
            "children",
            "LOD",
            "lodInput",
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
        cls.lodAttribute = "%s.LOD" % node
        cls.lodInputAttribute = "%s.lodInput" % node
        cls.sceneTypeAttribute = "%s.sceneType" % node

    @classmethod
    def create(cls, name=None, typed=None):
        name = name or "pipeNode"
        typed = typed or cls.typed

        if not typed:
            LOGGER.warning("invalid node type")
            return

        from maya import cmds

        cls.loadPlugin()

        cls.node = cmds.createNode(typed, name=name)
        cls.setGlobalAttributes(cls.node)
        cls.update(node=cls.node, lock=False)
        # cls.setLocked(cls.node, lock=True)
        return cls.node

    @classmethod
    def update(cls, node=None, lock=False):
        node = node or cls.node
        from maya import cmds

        cls.setGlobalAttributes(node)
        if not cmds.referenceQuery(node, isNodeReferenced=True):
            cls.setLocked(node, lock=False)
        manifestPath = cmds.getAttr(cls.filepathAttribute)
        if not manifestPath.endswith("manifest.json"):
            manifestPath = "manifest.json"
        cmds.setAttr(cls.filepathAttribute, "", type="string")
        cmds.setAttr(cls.filepathAttribute, manifestPath, type="string")
        if lock and not cmds.referenceQuery(node, isNodeReferenced=True):
            cls.setLocked(node, lock=True)

    @staticmethod
    def setLocked(node, lock=True):
        from maya import cmds

        cmds.lockNode(node, lock=False)
        for each in PipeNode.allAttributeList(node=node):
            attribute = "%s.%s" % (node, each)
            if not cmds.objExists(attribute):
                continue
            cmds.setAttr(attribute, lock=lock)
        cmds.lockNode(node, lock=lock)

    @staticmethod
    def delete(node):
        from maya import cmds

        try:
            PipeNode.setLocked(node, lock=False)
            cmds.delete(node)
        except Exception as error:
            LOGGER.error(error)

    @classmethod
    def refresh(cls, node=None, lock=False):
        cls.update(node=node, lock=lock)

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
        cmds.setAttr(cls.metadataAttribute, str(context), type="string")
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
    def getDagPath(node):
        from maya import OpenMaya

        mselection = OpenMaya.MSelectionList()
        mselection.add(node)
        mdag_path = OpenMaya.MDagPath()
        mselection.getDagPath(0, mdag_path)
        return mdag_path

    @staticmethod
    def getMObject(node):
        from maya import OpenMaya

        mselection = OpenMaya.MSelectionList()
        mselection.add(node)
        mobject = OpenMaya.MObject()
        mselection.getDependNode(0, mobject)
        return mobject

    @staticmethod
    def getPlug(node, attribute):
        from maya import OpenMaya

        mplug = OpenMaya.MPlug()
        mselection = OpenMaya.MSelectionList()
        mselection.add("%s.%s" % (node, attribute))
        mselection.getPlug(0, mplug)
        return mplug

    @staticmethod
    def getEnumAttributeValues(node, attribute):
        from maya import OpenMaya

        mplug = PipeNode.getPlug(node, attribute)
        enumAttribute = OpenMaya.MFnEnumAttribute(mplug.attribute())
        scriptUtil = OpenMaya.MScriptUtil()
        shortPtr = scriptUtil.asShortPtr()
        enumAttribute.getMax(shortPtr)
        max = scriptUtil.getShort(shortPtr)
        filedTypes = list()
        for index in range(max + 1):
            filedTypes.append(enumAttribute.fieldName(index))
        return filedTypes

    @staticmethod
    def getLocation(node=None):
        node = node or PipeMayaAssetNode.node
        from maya import cmds

    @staticmethod
    def serachNode(nodes=None):
        from maya import cmds

        nodes = nodes or cmds.ls(all=True)
        context = {}
        for each in PipeNode.openMayaMPxs():
            nodeList = cmds.ls(nodes, type=each.kPluginNodeTypeName)
            context[each.kPluginNodeTypeName] = nodeList
        return context

    @staticmethod
    def parentDependencyOrder():
        context = list()
        for each in PipeNode.openMayaMPxs():
            context.append(each.kPluginNodeTypeName)
        return context

    @staticmethod
    def disconnectSourcePlugs(attribute):
        from maya import cmds

        plugs = cmds.listConnections(attribute, plugs=True, source=True)
        if not plugs:
            return
        for plug in plugs:
            cmds.disconnectAttr(plug, attribute)

    @staticmethod
    def getRootNodes(nodes):
        from maya import cmds

        #===========================================================================================
        # rootNodes = set()
        # for each in cmds.ls(nodes, long=True, type="transform"):
        #     rootNodes.add(each.split("|")[1])
        #===========================================================================================

        rootNodes = []
        for each in cmds.ls(nodes, type="transform"):
            parents = cmds.listRelatives(each, parent=True)
            if not parents:
                rootNodes.append(each)
                continue
            if parents[0] not in nodes:
                rootNodes.append(each)

        return rootNodes
    
    @staticmethod
    def unParentNodes(nodes):
        nodes = []
        for each in cmds.ls(nodes, type="transform"):
            if cmds.listRelatives(each, parent=True):
                continue
            nodes.append(each)
        return nodes

    @staticmethod
    def searchFirstNode(nodes=[]):
        from maya import cmds

        nodes = nodes or cmds.ls()
        for each in PipeNode.parentDependencyOrder():
            children = cmds.ls(nodes, type=each)
            if not children:
                continue
            return children[0]
        return None

    @staticmethod
    def linkToParent(parent, nodes):
        from maya import cmds

        firstNode = PipeNode.searchFirstNode(nodes=nodes)
        
        if not firstNode:
            LOGGER.warning("could not find children pipe nodes")

        parentAttribute = "%s.children" % parent
        childAttribute = "%s.parent" % firstNode


        PipeNode.disconnectSourcePlugs(childAttribute)
        cmds.connectAttr(parentAttribute, childAttribute, f=True)

        childRootNodes = PipeNode.getRootNodes(nodes)
        # childRootNodes = PipeNode.unParentNodes(nodes)
        
        for each in childRootNodes:
            parents = cmds.listRelatives(each, parent=True)
            if parents and parent in parents:
                continue
            cmds.parent(firstNode, parent)



    @staticmethod
    def getSceneType(node):
        from maya import cmds
        from maya import OpenMaya

        index = cmds.getAttr("%s.sceneType" % node)
        mplug = PipeNode.getPlug(node, "sceneType")
        enumAttribute = OpenMaya.MFnEnumAttribute(mplug.attribute())
        fieldName = enumAttribute.fieldName(index)
        return fieldName

    @staticmethod
    def getAttibuteValue(attribute):
        from maya import cmds

        if not cmds.objExists(attribute):
            LOGGER.warning("could not find the attribute, %s" % attribute)
            return None
        return cmds.getAttr(attribute)

    @staticmethod
    def getChildren(node):
        from maya import cmds

        children = cmds.listConnections("%s.children" % node, destination=True)
        return children

    @staticmethod
    def getParent(node):
        from maya import cmds
        parents = cmds.listConnections("%s.parent" % self.node, source=True)
        return parents[0] if parents else None
    
    @staticmethod
    def getReferenceNode(node):
        from maya import cmds
        if not cmds.referenceQuery(node, isNodeReferenced=True):
            LOGGER.warning("node <%s> is not referenced in the scene")
            return
        referenceNode = cmds.referenceQuery(node, rfn=True)
        return referenceNode
    
    @staticmethod
    def getAllReferenceNode(node):
        from maya import cmds
        if not cmds.referenceQuery(node, isNodeReferenced=True):
            LOGGER.warning("node <%s> is not referenced in the scene")
            return list()
        allNodes = cmds.referenceQuery(node, nodes=True)   
        return allNodes
    
    @staticmethod
    def getReferencePath(node):
        from maya import cmds
        if not cmds.referenceQuery(node, isNodeReferenced=True):
            LOGGER.warning("node <%s> is not referenced in the scene")
            return None
        filepath = cmds.referenceQuery (node,  filename=True, withoutCopyNumber=True)
        return filepath


class GetNode(object):
    def __init__(self, node):
        self.node = node
        
    @property
    def name(self):
        return self.node

    def isNull(self):
        return False if self.node else True
    
    def isValid(self):
        return True if self.node else False
        
    @property
    def nodeType(self):
        return PipeNode.nodeType(self.node)

    def openMayaMPx(self):
        mayaMPx = PipeNode.openMayaMPx(node=self.node)
        return mayaMPx

    def pipeNodeType(self):
        mayaMPx = self.openMayaMPx()
        if mayaMPx.kPipeType != "shot":
            return mayaMPx
        fieldName = PipeNode.getSceneType(self.node)
        return fieldName

    def getAttributeValue(self, attribute):
        attributeValue = PipeNode.getAttibuteValue("%s.%s" % (self.node, attribute))
        return attributeValue

    def taskId(self):
        id = self.getAttributeValue("taskId")
        return id

    def children(self):
        children = PipeNode.getChildren(self.node)
        return children

    def getChildContext(self, child):
        entityId = self.getAttributeValue("entityId")
        if not entityId:
            return dict()
        entityName = PipeNode.getAttibuteValue("%s.entityName" % child)
        context = {
            "id": entityId,
            "name": entityName,
            "color": [0, 255, 0],
            "node": GetNode(child),
        }
        return context

    def getParent(self):
        parent = PipeNode.getParent(self.node)
        return parent

    def getMetadata(self):
        metadata = PipeNode.getAttributeValue("metadata")
        return metadata

    def getProject(self):
        poject = PipeNode.getAttributeValue("poject")
        return poject

    def getCategory(self):
        category = PipeNode.getAttributeValue("category")
        return category

    def getEntityName(self):
        entityName = PipeNode.getAttributeValue("entityName")
        return entityName

    def getTaskName(self):
        taskName = self.getAttributeValue("taskName")
        return taskName

    def getKind(self):
        kind = self.getAttributeValue("kind")
        return kind

    def getVersion(self):
        version = self.getAttributeValue("version")
        return version

    def getStatus(self):
        status = self.getAttributeValue("status")
        return status

    def referenceNode(self):
        return PipeNode.getReferenceNode(self.node)
    
    def referenceNodes(self):
        print ("\nself.node", self.node)
        return PipeNode.getAllReferenceNode(self.node)

    def referencePath(self):
        return PipeNode.getReferencePath(self.node)
        
            
