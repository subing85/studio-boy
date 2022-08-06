import sys
import ast

from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

from pipe import utils
from pipe import resources
from pipe.core import logger

# visibility and lock
# prevent pipe enum filed name to update metadata

LOGGER = logger.getLogger(__name__)
ATTRIBUTE_CONTEXT = resources.getInputData("mayaNode")


class PipeMayaNode(OpenMayaMPx.MPxTransform):

    mobject = OpenMaya.MObject()
    metadata = OpenMaya.MObject()
    project = OpenMaya.MObject()
    assets = OpenMaya.MObject()
    sequence = OpenMaya.MObject()
    shot = OpenMaya.MObject()
    id = OpenMaya.MObject()
    name = OpenMaya.MObject()
    typed = OpenMaya.MObject()
    taskName = OpenMaya.MObject()
    taskId = OpenMaya.MObject()
    kind = OpenMaya.MObject()
    version = OpenMaya.MObject()
    startFrame = OpenMaya.MObject()
    endFrame = OpenMaya.MObject()
    framePerSecond = OpenMaya.MObject()
    assembly = OpenMaya.MObject()
    releasedAt = OpenMaya.MObject()
    releasedBy = OpenMaya.MObject()
    status = OpenMaya.MObject()
    statusAt = OpenMaya.MObject()
    statusBy = OpenMaya.MObject()
    description = OpenMaya.MObject()

    attributList = dict()

    example = {
        "project": "Ranj and Rani",
        "id": "56abf682-88ba-4ab4-83ab-fd733fcec391",
        "name": "rani",
        "typed": "character",
        "taskName": "puppet",
        "taskId": "779d13ee-21dc-468d-9ddf-6573ebbd2e4e",
        "version": "0.1.0",
        "startFrame": None,
        "endFrame": None,
        "framePerSecond": None,
        "assembly": None,
        "description": "test",
    }

    nodeId = None
    kTransformMatrixID = None
    kPluginNodeTypeName = None

    def __init__(self):
        OpenMayaMPx.MPxTransform.__init__(self)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeMayaNode())

    def _children(self):
        mobjects = [
            self.project,
            self.assets,
            self.sequence,
            self.shot,
            self.id,
            self.name,
            self.typed,
            self.taskName,
            self.taskId,
            self.kind,
            self.version,
            self.startFrame,
            self.endFrame,
            self.framePerSecond,
            self.assembly,
            self.releasedAt,
            self.releasedBy,
            self.status,
            self.statusAt,
            self.statusBy,
            self.description,
        ]
        return mobjects

    def _compute(self, plug, dataBlock):

        for a in self.children():
            print(a.isNull())

        if plug in self.children():
            print("--------------------------")

            inputHandle = dataBlock.inputValue(self.metadata)
            value = inputHandle.asString()
            outputHandle = dataBlock.outputValue(plug)
            inputvalue = ast.literal_eval(value) if value else dict()
            attribute = plug.name().split(".")[-1]
            value = (
                inputvalue[attribute]
                if inputvalue.get(attribute)
                else ""
            )
            outputHandle.setString(str(value))
            # outputHandle.setHidden(True)
            dataBlock.setClean(plug)

    @classmethod
    def setAttributeProperty(cls, attribute):
        attribute.setStorable(False)
        attribute.setWritable(True)
        attribute.setHidden(False)
        attribute.setKeyable(True)
        attribute.setInternal(True)
        attribute.setCached(True)
        attribute.setAffectsWorldSpace(True)


class PipeMayaAssetNode(OpenMayaMPx.MPxTransform):

    """pipe categories node - asset node"""

    metadata = OpenMaya.MObject()
    project = OpenMaya.MObject()
    assets = OpenMaya.MObject()
    id = OpenMaya.MObject()
    name = OpenMaya.MObject()
    typed = OpenMaya.MObject()
    taskName = OpenMaya.MObject()
    taskId = OpenMaya.MObject()
    version = OpenMaya.MObject()
    kind = OpenMaya.MObject()
    releasedAt = OpenMaya.MObject()
    releasedBy = OpenMaya.MObject()
    status = OpenMaya.MObject()
    statusAt = OpenMaya.MObject()
    statusBy = OpenMaya.MObject()
    description = OpenMaya.MObject()

    attributList = {
        "metadata": metadata,
        "project": project,
        "assets": assets,
        "id": id,
        "name": name,
        "typed": typed,
        "taskName": taskName,
        "taskId": taskId,
        "version": version,
        "kind": kind,
        "releasedAt": releasedAt,
        "releasedBy": releasedBy,
        "status": status,
        "statusAt": statusAt,
        "statusBy": statusBy,
        "description": description,
    }

    example = {
        "project": "Ranj and Rani",
        "id": "56abf682-88ba-4ab4-83ab-fd733fcec391",
        "name": "rani",
        "typed": "character",
        "taskName": "puppet",
        "taskId": "779d13ee-21dc-468d-9ddf-6573ebbd2e4e",
        "version": "0.1.0",
        "description": "test",
    }

    nodeId = OpenMaya.MTypeId(0x0000)
    kTransformMatrixID = OpenMaya.MTypeId(0x0001)
    kPluginNodeTypeName = "pipeAssetNode"

    def __init__(self):
        OpenMayaMPx.MPxTransform.__init__(self)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeMayaNode())

    def children(self):
        mobjects = [
            self.project,
            self.assets,
            # self.sequence,
            # self.shot,
            self.id,
            self.name,
            self.typed,
            self.taskName,
            self.taskId,
            self.kind,
            self.version,
            # self.startFrame,
            # self.endFrame,
            # self.framePerSecond,
            # self.assembly,
            self.releasedAt,
            self.releasedBy,
            self.status,
            self.statusAt,
            self.statusBy,
            self.description,
        ]
        return mobjects

    @classmethod
    def initializer(cls):
        typedAttribute = OpenMaya.MFnTypedAttribute()

        metadataContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="metadata", first=True
        )
        cls.metadata = typedAttribute.create(
            metadataContext["name"],
            metadataContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.metadata)

        projectContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="project", first=True
        )
        cls.project = typedAttribute.create(
            projectContext["name"],
            projectContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.project)

        assetsContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="assets", first=True
        )
        cls.assets = typedAttribute.create(
            assetsContext["name"],
            assetsContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.assets)

        idContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="id", first=True
        )
        cls.id = typedAttribute.create(
            idContext["name"],
            idContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.id)

        nameContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="name", first=True
        )
        cls.name = typedAttribute.create(
            nameContext["name"],
            nameContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.name)

        typedContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="typed", first=True
        )
        cls.typed = typedAttribute.create(
            typedContext["name"],
            typedContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.typed)

        taskNameContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="taskName", first=True
        )
        cls.taskName = typedAttribute.create(
            taskNameContext["name"],
            taskNameContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.taskName)

        taskIdContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="taskId", first=True
        )
        cls.taskId = typedAttribute.create(
            taskIdContext["name"],
            taskIdContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.taskId)

        kindContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="kind", first=True
        )
        cls.kind = typedAttribute.create(
            kindContext["name"],
            kindContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.kind)

        versionContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="version", first=True
        )
        cls.version = typedAttribute.create(
            versionContext["name"],
            versionContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.version)

        releasedAtContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="releasedAt", first=True
        )
        cls.releasedAt = typedAttribute.create(
            releasedAtContext["name"],
            releasedAtContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.releasedAt)

        releasedByContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="releasedBy", first=True
        )
        cls.releasedBy = typedAttribute.create(
            releasedByContext["name"],
            releasedByContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.releasedBy)

        statusContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="status", first=True
        )
        cls.status = typedAttribute.create(
            statusContext["name"],
            statusContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.status)

        statusAtContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="statusAt", first=True
        )
        cls.statusAt = typedAttribute.create(
            statusAtContext["name"],
            statusAtContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.statusAt)

        statusByContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="statusBy", first=True
        )
        cls.statusBy = typedAttribute.create(
            statusByContext["name"],
            statusByContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.statusBy)

        descriptionContext = utils.searchContext(
            ATTRIBUTE_CONTEXT, "name", value="description", first=True
        )
        cls.description = typedAttribute.create(
            descriptionContext["name"],
            descriptionContext["shortName"],
            OpenMaya.MFnData.kString,
        )
        cls.addAttribute(cls.description)

        cls.attributeAffects(cls.metadata, cls.project)
        cls.attributeAffects(cls.metadata, cls.assets)
        cls.attributeAffects(cls.metadata, cls.id)
        cls.attributeAffects(cls.metadata, cls.name)
        cls.attributeAffects(cls.metadata, cls.typed)
        cls.attributeAffects(cls.metadata, cls.taskName)
        cls.attributeAffects(cls.metadata, cls.taskId)
        cls.attributeAffects(cls.metadata, cls.kind)
        cls.attributeAffects(cls.metadata, cls.version)
        # cls.attributeAffects(cls.metadata, cls.releasedAt)
        cls.attributeAffects(cls.metadata, cls.releasedBy)
        cls.attributeAffects(cls.metadata, cls.status)
        cls.attributeAffects(cls.metadata, cls.statusAt)
        cls.attributeAffects(cls.metadata, cls.statusBy)
        cls.attributeAffects(cls.metadata, cls.description)

    def compute(self, plug, dataBlock):

        # ===========================================================================================
        # if plug in self.children():
        #     print ("--------------------------")
        #     for a in self.children():
        #         print (a.isNull())
        # ===========================================================================================

        inputHandle = dataBlock.inputValue(self.metadata)
        value = inputHandle.asString()
        outputHandle = dataBlock.outputValue(plug)
        inputvalue = ast.literal_eval(value) if value else dict()
        attribute = plug.name().split(".")[-1]
        value = (
            inputvalue[attribute] if inputvalue.get(attribute) else ""
        )
        outputHandle.setString(str(value))
        # outputHandle.setHidden(True)
        dataBlock.setClean(plug)


class PipeNode(object):

    typed = None

    def __init__(self, node=None):
        self.node = node
        self.nodeType = "%s.nodeType" % self.node
        self.metadata = "%s.metadata" % self.node

    def loadPlugin(self):
        from maya import cmds

        isLoaded = cmds.pluginInfo("pipeNode", q=True, loaded=True)
        if isLoaded:
            LOGGER.warning('already loaded "pipeNode" plugin')
            return
        try:
            cmds.loadPlugin("pipeNode")
        except Exception as error:
            raise ValueError(error)

    @classmethod
    def create(cls, typed=None, name=None):
        typed = typed or cls.typed
        name = name or "pipeMayaNode1"

        from maya import cmds

        PipeNode.loadPlugin(cls)
        cls.node = cmds.createNode("pipeMayaNode", name=name)
        cls.nodeType = "%s.nodeType" % cls.node
        cls.metadata = "%s.metadata" % cls.node
        filedTypes = PipeNode.nodeFiledTypes(cls)
        if typed not in filedTypes:
            cmds.delete(cls.node)
            raise Exception(
                "invalid node typed parameter <%s>" % typed
            )
        cmds.setAttr(cls.nodeType, filedTypes.index(typed))
        cmds.setAttr(cls.nodeType, lock=True)
        cls.setLocked(cls.node, locked=True)

    @classmethod
    def update(cls, context):
        from maya import cmds

        PipeNode.setLocked(cls.node, locked=False)
        cmds.setAttr(cls.metadata, str(context), type="string")
        PipeNode.setLocked(cls.node, locked=True)

    @staticmethod
    def setLocked(node, locked=True):
        from maya import cmds

        for each in PipeMayaNode.attributList:
            cmds.setAttr("%s.%s" % (node, each), lock=locked)
        cmds.lockNode(node, lock=locked)

    def nodeFiledTypes(self, node=None, nodeType=None):
        node = node or self.node
        nodeType = nodeType or self.nodeType
        from maya import OpenMaya

        mplug = PipeNode.getPlug(self.nodeType)
        enumAttribute = OpenMaya.MFnEnumAttribute(mplug.attribute())
        scriptUtil = OpenMaya.MScriptUtil()
        shortPtr = scriptUtil.asShortPtr()
        enumAttribute.getMax(shortPtr)
        max = scriptUtil.getShort(shortPtr)
        filedTypes = list()
        for index in range(max):
            filedTypes.append(enumAttribute.fieldName(index))
        return filedTypes

    @staticmethod
    def getPlug(attribute):
        from maya import OpenMaya

        mplug = OpenMaya.MPlug()
        mselection = OpenMaya.MSelectionList()
        mselection.add(attribute)
        mselection.getPlug(0, mplug)
        return mplug

    @classmethod
    def getContext(cls, node=None):
        from maya import cmds

        node = node or cls.node
        self.metadata = "%s.metadata" % node
        context = cmds.getAttr(cls.metadata)
        context = ast.literal_eval(context) if context else dict()
        return context

    @staticmethod
    def children(self):
        pass


class PipeShotNode(PipeNode):

    typed = "shot"


class PipeAssetNode(PipeNode):

    typed = "asset"
