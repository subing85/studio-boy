import sys
import ast
import json

from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

from pipe import utils
from pipe import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)
ATTRIBUTE_CONTEXT = resources.getInputData("mayaNode")


class PipeMayaNode(OpenMayaMPx.MPxTransform):

    mobject = OpenMaya.MObject()
    filepath = OpenMaya.MObject()
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
    filename = OpenMaya.MObject()
    extension = OpenMaya.MObject()
    releasedAt = OpenMaya.MObject()
    releasedBy = OpenMaya.MObject()
    status = OpenMaya.MObject()
    statusAt = OpenMaya.MObject()
    statusBy = OpenMaya.MObject()
    description = OpenMaya.MObject()

    # attributList = dict()
    attributList = {
        "filepath": filepath,
        "metadata": metadata,
        "project": project,
        "assets": assets,
        "id": id,
        "name": name,
        "typed": typed,
        "taskName": taskName,
        "taskId": taskId,
        "kind": kind,
        "version": version,
        "filename": filename,
        "extension": extension,
        "releasedAt": releasedAt,
        "releasedBy": releasedBy,
        "status": status,
        "statusAt": statusAt,
        "statusBy": statusBy,
        "description": description,
    }

    nodeId = None
    kTransformMatrixID = None
    kPluginNodeTypeName = None

    def __init__(self):
        OpenMayaMPx.MPxTransform.__init__(self)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeMayaAssetNode())

    @staticmethod
    def getAttribute(name):
        context = utils.searchContext(
            ATTRIBUTE_CONTEXT, "fn", value=name, first=True
        )
        return context

    def children(self):
        mobjects = [
            self.project,
            self.assets,
            self.id,
            self.name,
            self.typed,
            self.taskName,
            self.taskId,
            self.kind,
            self.version,
            self.filename,
            self.extension,
            self.releasedAt,
            self.releasedBy,
            self.status,
            self.statusAt,
            self.statusBy,
            self.description,
        ]
        return mobjects

    @staticmethod
    def createStringAttribute(mobject, name, **kwargs):
        context = PipeMayaNode.getAttribute(name)
        attribute = OpenMaya.MFnTypedAttribute()
        mobject = attribute.create(
            context["fn"], context["sn"], OpenMaya.MFnData.kString
        )
        PipeMayaNode.addAttribute(mobject)
        if kwargs.get("filepath"):
            attribute.setUsedAsFilename(True)
        if kwargs.get("default"):
            stringData = OpenMaya.MFnStringData()
            attribute.setDefault(stringData.create(kwargs["default"]))
        attribute.setKeyable(False)
        attribute.setStorable(False)
        attribute.setWritable(True)
        attribute.setHidden(False)
        attribute.setInternal(True)
        attribute.setCached(True)
        attribute.setAffectsWorldSpace(True)
        return mobject

    @staticmethod
    def getMetadata(filepath):

        data = dict()
        with open(filepath, "r") as file:
            data = json.load(file)

    def compute(self, plug, dataBlock):
        if plug == self.metadata:

            inputHandle = dataBlock.inputValue(self.filepath)
            value = inputHandle.asString()

            metadata = PipeMayaNode.getMetadata(value)

            outputHandle = dataBlock.outputValue(plug)
            outputHandle.setString(str(metadata))

            print("manifestttttttttttttttttttttt")
            outputHandle.setClean()
            dataBlock.setClean(plug)

        if plug in self.children():
            inputHandle = dataBlock.inputValue(self.metadata)
            value = inputHandle.asString()
            outputHandle = dataBlock.outputValue(plug)

            try:
                inputvalue = ast.literal_eval(value)
            except Exception as error:
                LOGGER.warning("invalid metadata.")
                inputvalue = dict()

            attribute = plug.name().split(".")[-1]
            value = (
                inputvalue[attribute]
                if inputvalue.get(attribute)
                else ""
            )
            outputHandle.setString(str(value))
            outputHandle.setClean()
            dataBlock.setClean(plug)
        else:
            print("not founddddddddddddddddddddddd")


class PipeMayaAssetNode(PipeMayaNode):
    mobject = OpenMaya.MObject()
    filepath = OpenMaya.MObject()
    metadata = OpenMaya.MObject()
    project = OpenMaya.MObject()
    assets = OpenMaya.MObject()
    id = OpenMaya.MObject()
    name = OpenMaya.MObject()
    typed = OpenMaya.MObject()
    taskName = OpenMaya.MObject()
    taskId = OpenMaya.MObject()
    kind = OpenMaya.MObject()
    version = OpenMaya.MObject()
    filename = OpenMaya.MObject()
    extension = OpenMaya.MObject()
    description = OpenMaya.MObject()
    releasedAt = OpenMaya.MObject()
    releasedBy = OpenMaya.MObject()
    status = OpenMaya.MObject()
    statusAt = OpenMaya.MObject()
    statusBy = OpenMaya.MObject()
    description = OpenMaya.MObject()

    attributList = {
        "filepath": filepath,
        "metadata": metadata,
        "project": project,
        "assets": assets,
        "id": id,
        "name": name,
        "typed": typed,
        "taskName": taskName,
        "taskId": taskId,
        "kind": kind,
        "version": version,
        "filename": filename,
        "extension": extension,
        "releasedAt": releasedAt,
        "releasedBy": releasedBy,
        "status": status,
        "statusAt": statusAt,
        "statusBy": statusBy,
        "description": description,
    }

    example = {
        "project": "Ranj and Rani",
        "assets": "modeling",
        "id": "56abf682-88ba-4ab4-83ab-fd733fcec391",
        "fn": "rani",
        "typed": "character",
        "taskName": "puppet",
        "taskId": "779d13ee-21dc-468d-9ddf-6573ebbd2e4e",
        "kind": "submit",
        "version": "0.1.0",
        "filename": "rani",
        "extension": "ma",
        "releasedAt": "2022:May:15:Sunday-10:12:44:PM",
        "releasedBy": "subing85@gmail.com",
        "status": "Completed",
        "statusAt": "2022:May:15:Sunday-10:12:44:PM",
        "statusBy": "subing85@gmail.com",
        "description": "test",
    }

    nodeId = OpenMaya.MTypeId(0x0001)
    kTransformMatrixID = OpenMaya.MTypeId(0x0000)
    kPluginNodeTypeName = "pipeAssetNode"

    @classmethod
    def initializer(cls):

        cls.filepath = PipeMayaNode.createStringAttribute(
            cls.filepath,
            "filepath",
            filepath=True,
            default="/manifest.json",
        )
        cls.metadata = PipeMayaNode.createStringAttribute(
            cls.metadata, "metadata", default="{}"
        )
        cls.project = PipeMayaNode.createStringAttribute(
            cls.project, "project"
        )
        cls.assets = PipeMayaNode.createStringAttribute(
            cls.project, "assets"
        )
        cls.id = PipeMayaNode.createStringAttribute(cls.id, "id")
        cls.name = PipeMayaNode.createStringAttribute(
            cls.name, "name"
        )
        cls.typed = PipeMayaNode.createStringAttribute(
            cls.typed, "typed"
        )
        cls.taskName = PipeMayaNode.createStringAttribute(
            cls.taskName, "taskName"
        )
        cls.taskId = PipeMayaNode.createStringAttribute(
            cls.taskId, "taskId"
        )
        cls.kind = PipeMayaNode.createStringAttribute(
            cls.kind, "kind"
        )
        cls.version = PipeMayaNode.createStringAttribute(
            cls.version, "version"
        )
        cls.filename = PipeMayaNode.createStringAttribute(
            cls.filename, "filename"
        )
        cls.extension = PipeMayaNode.createStringAttribute(
            cls.extension, "extension"
        )
        cls.releasedAt = PipeMayaNode.createStringAttribute(
            cls.releasedAt, "releasedAt"
        )
        cls.releasedBy = PipeMayaNode.createStringAttribute(
            cls.releasedBy, "releasedBy"
        )
        cls.status = PipeMayaNode.createStringAttribute(
            cls.status, "status"
        )
        cls.statusAt = PipeMayaNode.createStringAttribute(
            cls.statusAt, "statusAt"
        )
        cls.statusBy = PipeMayaNode.createStringAttribute(
            cls.statusBy, "statusBy"
        )
        cls.description = PipeMayaNode.createStringAttribute(
            cls.description, "description"
        )

        cls.attributeAffects(cls.filepath, cls.metadata)
        cls.attributeAffects(cls.metadata, cls.project)
        cls.attributeAffects(cls.metadata, cls.assets)
        cls.attributeAffects(cls.metadata, cls.id)
        cls.attributeAffects(cls.metadata, cls.name)
        cls.attributeAffects(cls.metadata, cls.typed)
        cls.attributeAffects(cls.metadata, cls.taskName)
        cls.attributeAffects(cls.metadata, cls.taskId)
        cls.attributeAffects(cls.metadata, cls.kind)
        cls.attributeAffects(cls.metadata, cls.version)
        cls.attributeAffects(cls.metadata, cls.filename)
        cls.attributeAffects(cls.metadata, cls.extension)
        cls.attributeAffects(cls.metadata, cls.releasedAt)
        cls.attributeAffects(cls.metadata, cls.releasedBy)
        cls.attributeAffects(cls.metadata, cls.status)
        cls.attributeAffects(cls.metadata, cls.statusAt)
        cls.attributeAffects(cls.metadata, cls.statusBy)
        cls.attributeAffects(cls.metadata, cls.description)

        print("\n++++++++++++++++++++++++++++++++++")
        for d in dir(cls):
            print(d)
        print("---------------------------------\n")


class PipeMayaShotNode(PipeMayaNode):
    mobject = OpenMaya.MObject()
    metadata = OpenMaya.MObject()
    project = OpenMaya.MObject()
    sequence = OpenMaya.MObject()
    shot = OpenMaya.MObject()
    id = OpenMaya.MObject()
    name = OpenMaya.MObject()
    typed = OpenMaya.MObject()
    taskName = OpenMaya.MObject()
    taskId = OpenMaya.MObject()
    kind = OpenMaya.MObject()
    version = OpenMaya.MObject()
    filename = OpenMaya.MObject()
    extension = OpenMaya.MObject()
    startFrame = OpenMaya.MObject()
    endFrame = OpenMaya.MObject()
    framePerSecond = OpenMaya.MObject()
    assembly = OpenMaya.MObject()
    description = OpenMaya.MObject()
    releasedAt = OpenMaya.MObject()
    releasedBy = OpenMaya.MObject()
    status = OpenMaya.MObject()
    statusAt = OpenMaya.MObject()
    statusBy = OpenMaya.MObject()
    description = OpenMaya.MObject()

    attributList = {
        "metadata": metadata,
        "project": project,
        "sequence": sequence,
        "shot": shot,
        "id": id,
        "fn": name,
        "typed": typed,
        "taskName": taskName,
        "taskId": taskId,
        "kind": kind,
        "version": version,
        "filename": filename,
        "extension": extension,
        "startFrame": startFrame,
        "endFrame": endFrame,
        "framePerSecond": framePerSecond,
        "assembly": assembly,
        "releasedAt": releasedAt,
        "releasedBy": releasedBy,
        "status": status,
        "statusAt": statusAt,
        "statusBy": statusBy,
        "description": description,
    }

    example = {
        "project": "Ranj and Rani",
        "sequence": "Seq_101",
        "shot": "Shot_1001",
        "id": "56abf682-88ba-4ab4-83ab-fd733fcec391",
        "fn": "rani",
        "typed": "character",
        "taskName": "puppet",
        "taskId": "779d13ee-21dc-468d-9ddf-6573ebbd2e4e",
        "kind": "submit",
        "version": "0.1.0",
        "filename": "rani",
        "extension": "ma",
        "startFrame": "1001",
        "endFrame": "1025",
        "framePerSecond": "25",
        "assembly": {},
        "releasedAt": "2022:May:15:Sunday-10:12:44:PM",
        "releasedBy": "subing85@gmail.com",
        "status": "Completed",
        "statusAt": "2022:May:15:Sunday-10:12:44:PM",
        "statusBy": "subing85@gmail.com",
        "description": "test",
    }

    nodeId = OpenMaya.MTypeId(0x0002)
    kTransformMatrixID = OpenMaya.MTypeId(0x0000)
    kPluginNodeTypeName = "pipeShotNode"

    @classmethod
    def initializer(cls):
        typedAttribute = OpenMaya.MFnTypedAttribute()
        # stringData = OpenMaya.MFnStringData()

        cls.filepath = PipeMayaNode.createStringAttribute(
            cls.filepath,
            "filepath",
            filepath=True,
            default="/manifest.json",
        )
        cls.metadata = PipeMayaNode.createStringAttribute(
            cls.metadata, "metadata", default="{}"
        )
        cls.project = PipeMayaNode.createStringAttribute(
            cls.project, "project"
        )
        cls.sequence = PipeMayaNode.createStringAttribute(
            cls.sequence, "sequence"
        )
        cls.shot = PipeMayaNode.createStringAttribute(
            cls.shot, "shot"
        )
        cls.id = PipeMayaNode.createStringAttribute(cls.id, "id")
        cls.name = PipeMayaNode.createStringAttribute(
            cls.name, "name"
        )
        cls.typed = PipeMayaNode.createStringAttribute(
            cls.typed, "typed"
        )
        cls.taskName = PipeMayaNode.createStringAttribute(
            cls.taskName, "taskName"
        )
        cls.taskId = PipeMayaNode.createStringAttribute(
            cls.taskId, "taskId"
        )
        cls.kind = PipeMayaNode.createStringAttribute(
            cls.kind, "kind"
        )
        cls.version = PipeMayaNode.createStringAttribute(
            cls.version, "version"
        )
        cls.filename = PipeMayaNode.createStringAttribute(
            cls.filename, "filename"
        )
        cls.extension = PipeMayaNode.createStringAttribute(
            cls.extension, "extension"
        )

        cls.startFrame = PipeMayaNode.createStringAttribute(
            cls.startFrame, "startFrame"
        )
        cls.endFrame = PipeMayaNode.createStringAttribute(
            cls.endFrame, "endFrame"
        )
        cls.framePerSecond = PipeMayaNode.createStringAttribute(
            cls.framePerSecond, "framePerSecond"
        )
        cls.assembly = PipeMayaNode.createStringAttribute(
            cls.assembly, "assembly"
        )

        cls.releasedAt = PipeMayaNode.createStringAttribute(
            cls.releasedAt, "releasedAt"
        )
        cls.releasedBy = PipeMayaNode.createStringAttribute(
            cls.releasedBy, "releasedBy"
        )
        cls.status = PipeMayaNode.createStringAttribute(
            cls.status, "status"
        )
        cls.statusAt = PipeMayaNode.createStringAttribute(
            cls.statusAt, "statusAt"
        )
        cls.statusBy = PipeMayaNode.createStringAttribute(
            cls.statusBy, "statusBy"
        )
        cls.description = PipeMayaNode.createStringAttribute(
            cls.description, "description"
        )

        cls.attributeAffects(cls.filepath, cls.metadata)

        cls.attributeAffects(cls.metadata, cls.project)
        cls.attributeAffects(cls.metadata, cls.sequence)
        cls.attributeAffects(cls.metadata, cls.shot)
        cls.attributeAffects(cls.metadata, cls.id)
        cls.attributeAffects(cls.metadata, cls.name)
        cls.attributeAffects(cls.metadata, cls.typed)
        cls.attributeAffects(cls.metadata, cls.taskName)
        cls.attributeAffects(cls.metadata, cls.taskId)
        cls.attributeAffects(cls.metadata, cls.kind)
        cls.attributeAffects(cls.metadata, cls.version)
        cls.attributeAffects(cls.metadata, cls.filename)
        cls.attributeAffects(cls.metadata, cls.extension)
        cls.attributeAffects(cls.metadata, cls.startFrame)
        cls.attributeAffects(cls.metadata, cls.endFrame)
        cls.attributeAffects(cls.metadata, cls.framePerSecond)
        cls.attributeAffects(cls.metadata, cls.assembly)
        cls.attributeAffects(cls.metadata, cls.releasedAt)
        cls.attributeAffects(cls.metadata, cls.releasedBy)
        cls.attributeAffects(cls.metadata, cls.status)
        cls.attributeAffects(cls.metadata, cls.statusAt)
        cls.attributeAffects(cls.metadata, cls.statusBy)
        cls.attributeAffects(cls.metadata, cls.description)

        # affectsOutput


class PipeNode(object):

    typed = None

    def __init__(self, node=None):
        self.node = node
        self.metadataAttribute = "%s.metadata" % self.node

    @staticmethod
    def nodeTypes():
        context = [
            {
                "nodeId": PipeMayaAssetNode.nodeId,
                "typeName": PipeMayaAssetNode.kPluginNodeTypeName,
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
    def contextExample(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.example

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

    @staticmethod
    def openMayaMPx(node=None):
        node = node or PipeNode.node
        typed = PipeNode.nodeType(node)
        for each in [PipeMayaShotNode, PipeMayaAssetNode]:
            if each.kPluginNodeTypeName != typed:
                continue
            return each
        return None

    @staticmethod
    def attributeList(node=None):
        node = node or PipeNode.node
        obj = PipeNode.openMayaMPx(node=node)
        return obj.attributList

    @classmethod
    def create(cls, typed=None, name=None):
        typed = typed or cls.typed
        name = name or "PipeMayaAssetNode1"
        from maya import cmds

        cls.loadPlugin()
        cls.node = cmds.createNode(typed, name=name)
        cls.metadataAttribute = "%s.metadata" % cls.node
        cls.setLocked(cls.node, lock=True, metadata=False)

    @classmethod
    def update(cls, context, node=None):
        node = node or cls.node
        cls.metadataAttribute = "%s.metadata" % node
        from maya import cmds

        cls.setLocked(cls.node, lock=False, metadata=True)
        cmds.setAttr(
            cls.metadataAttribute, str(context), type="string"
        )
        cmds.setAttr(cls.metadataAttribute, lock=True)
        cls.setLocked(cls.node, lock=True, metadata=True)

    @staticmethod
    def setLocked(node, lock=True, metadata=False):
        from maya import cmds

        cmds.lockNode(node, lock=False)
        for each in PipeNode.attributeList():
            if not metadata and each == "metadata":
                continue
            attribute = "%s.%s" % (node, each)
            if not cmds.objExists(attribute):
                continue
            cmds.setAttr(attribute, lock=lock)
        cmds.lockNode(node, lock=lock)

    @classmethod
    def refresh(cls, node=None):
        node = node or cls.node
        cls.metadataAttribute = "%s.metadata" % node
        from maya import cmds

        cls.setLocked(cls.node, lock=False)
        context = cmds.getAttr(cls.metadataAttribute)
        cmds.setAttr(cls.metadataAttribute, lock=False)
        temp = cls.contextExample()
        cmds.setAttr(cls.metadataAttribute, str(temp), type="string")
        cmds.setAttr(
            cls.metadataAttribute, str(context), type="string"
        )
        cls.setLocked(cls.node, lock=True)

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
