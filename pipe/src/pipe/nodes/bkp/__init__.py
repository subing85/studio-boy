import os
import sys
import ast
import json

from maya import OpenMaya
from maya import OpenMayaUI
from maya import OpenMayaMPx
from maya import OpenMayaRender


from pipe import utils
from pipe import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)
ATTRIBUTE_CONTEXT = resources.getInputData("mayaNode")

from pprint import pprint


class PipeMayaNode(OpenMayaMPx.MPxTransform):

    mobject = OpenMaya.MObject()

    filepath = OpenMaya.MObject()
    metadata = OpenMaya.MObject()
    parent = OpenMaya.MObject()
    children = OpenMaya.MObject()
    lod = OpenMaya.MObject()
    lodOut = OpenMaya.MObject()
    input = OpenMaya.MObject()
    output = OpenMaya.MObject()

    outAttributes = list()
    attributeType = None
    nodeId = None
    kTransformMatrixID = None
    kPluginNodeTypeName = None

    def __init__(self):
        OpenMayaMPx.MPxTransform.__init__(self)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeMayaAssetNode())

    @classmethod
    def attributeList(cls):
        context = PipeMayaAssetNode.getAttributeContext(
            cls.attributeType
        )
        return context

    @staticmethod
    def getAttributeContext(type):
        context = utils.searchContext(
            ATTRIBUTE_CONTEXT, "label", value=type, first=True
        )
        print()
        context = list(
            filter(lambda k: k.get("enable"), context["attributes"])
        )
        return context

    @staticmethod
    def getMetadata(filepath):
        filepath = utils.setPathResolver(filepath)
        metadata = dict()
        if not filepath or not os.path.isfile(filepath):
            return metadata
        with open(filepath, "r") as file:
            try:
                content = json.load(file)
            except Exception as error:
                LOGGER.warning(error)
                content = dict()
            if not content:
                return metadata
            for each in PipeMayaNode.attributeList():
                filedlist = each["field"].split(".")
                filedValue = utils.getFieldValue(content, filedlist)
                metadata[each["fn"]] = filedValue
            return metadata

    def compute(self, plug, dataBlock):

        print(plug.name())

        print(self.metadata.isNull())

        if plug == self.metadata:
            inputHandle = dataBlock.inputValue(self.filepath)
            value = inputHandle.asString()
            metadata = PipeMayaNode.getMetadata(value)
            outputHandle = dataBlock.outputValue(plug)
            outputHandle.setString(str(metadata))
            outputHandle.setClean()
            dataBlock.setClean(plug)

        if plug in self.outAttributes:
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

    @staticmethod
    def createStringAttribute(mobject, fullName, shortName, **kwargs):
        attribute = OpenMaya.MFnTypedAttribute()
        mobject = attribute.create(
            fullName, shortName, OpenMaya.MFnData.kString
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
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createMessageAttribute(mobject, fullName, shortName):
        attribute = OpenMaya.MFnMessageAttribute()
        mobject = attribute.create(fullName, shortName)
        PipeMayaNode.addAttribute(mobject)
        attribute.setKeyable(False)
        attribute.setStorable(False)
        attribute.setWritable(True)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createEnumAttribute(
        mobject, fullName, shortName, fields, channelBox=False
    ):
        attribute = OpenMaya.MFnEnumAttribute()
        mobject = attribute.create(fullName, shortName)
        for index, field in enumerate(fields):
            attribute.addField(field, index)
        PipeMayaNode.addAttribute(mobject)
        switch = True if channelBox else False
        hidden = False if channelBox else True
        attribute.setChannelBox(switch)
        attribute.setKeyable(switch)
        attribute.setStorable(switch)
        attribute.setWritable(True)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def create3FloatAttribute(
        mobject, fullName, shortName, channelBox=False
    ):
        attribute = OpenMaya.MFnNumericAttribute()
        mobject = attribute.create(
            fullName, shortName, OpenMaya.MFnNumericData.k3Float
        )
        PipeMayaNode.addAttribute(mobject)
        attribute.setKeyable(False)
        attribute.setStorable(False)
        attribute.setWritable(False)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createNumericAttribute(
        mobject, fullName, shortName, default=0.0
    ):
        # ===========================================================================================
        # attribute = OpenMaya.MFnNumericAttribute()
        # mobject = attribute.create(fullName, shortName, OpenMaya.MFnNumericData.kFloat, default)
        # PipeMayaNode.addAttribute(mobject)
        # attribute.setKeyable(False)
        # attribute.setStorable(False)
        # attribute.setWritable(True)
        # attribute.setReadable(True)
        # attribute.setHidden(False)
        # return mobject
        # ===========================================================================================
        pass

    @staticmethod
    def createFilepathAttribute(mobject):
        mobject = PipeMayaNode.createStringAttribute(
            mobject,
            "filepath",
            "fp",
            filepath=True,
            default="/test.json",
        )
        return mobject

    @staticmethod
    def createFilepathAttribute1():
        PipeMayaNode.filepath = PipeMayaNode.createStringAttribute(
            PipeMayaNode.filepath,
            "filepath1",
            "fp1",
            filepath=True,
            default="/test.json",
        )
        return PipeMayaNode.filepath

    @staticmethod
    def createMetadataAttribute(mobject):
        mobject = PipeMayaNode.createStringAttribute(
            mobject, "metadata", "md", default="{}"
        )
        return mobject

    @staticmethod
    def createParentAttribute():
        PipeMayaNode.parent = PipeMayaNode.createMessageAttribute(
            PipeMayaNode.parent, "parent", "pt"
        )
        return PipeMayaNode.parent

    @staticmethod
    def createChildenAttribute():
        PipeMayaNode.children = PipeMayaNode.createMessageAttribute(
            PipeMayaNode.children, "children", "cn"
        )
        return PipeMayaNode.children

    @staticmethod
    def createLodAttribute():
        fields = ["Proxy", "LoRes", "HiRes"]
        PipeMayaNode.lod = PipeMayaNode.createEnumAttribute(
            PipeMayaNode.lod, "LOD", "ld", fields, channelBox=True
        )

        # ===========================================================================================
        # PipeMayaNode.lodOut = PipeMayaNode.create3FloatAttribute(
        #      PipeMayaNode.lodOut, "lodOut", "lodOut", channelBox=False
        #     )
        # ===========================================================================================
        return PipeMayaNode.lod
        # , PipeMayaNode.lodOut

    @staticmethod
    def createInputAttribute():
        PipeMayaNode.input = PipeMayaNode.createStringAttribute(
            PipeMayaNode.input, "inputA", "in", default="hello"
        )
        return PipeMayaNode.input

    @staticmethod
    def createOutAttribute():
        PipeMayaNode.output = PipeMayaNode.createStringAttribute(
            PipeMayaNode.output, "outputA", "ot", default="subin"
        )
        return PipeMayaNode.output


class PipeMayaAssetNode(OpenMaya.MPxTransform):
    nodeId = OpenMaya.MTypeId(0x0001)
    kTransformMatrixID = OpenMaya.MTypeId(0x1000)
    kPluginNodeTypeName = "pipeAssetNode"

    input = OpenMaya.MObject()
    output = OpenMaya.MObject()

    def __init__(self):
        # super(TestNode, self).__init__()
        OpenMayaMPx.MPxNode.__init__(self)

    def compute(self, plug, data):
        if plug == self.output:

            # get inputs
            a_value = data.inputValue(self.input).asString()

            hOutputHandle = data.outputValue(self.output)
            hOutputHandle.setString(str(a_value))
            hOutputHandle.setClean()
            data.setClean(plug)

    @classmethod
    def creator(cls):
        return PipeMayaAssetNode()
        # return OpenMayaMPx.asMPxPtr(TestNode())

    @classmethod
    def initialize(cls):

        attribute = OpenMaya.MFnTypedAttribute()
        cls.input = attribute.create(
            "inputs", "in", OpenMaya.MFnData.kString
        )
        cls.addAttribute(cls.input)

        attribute = OpenMaya.MFnTypedAttribute()
        cls.output = attribute.create(
            "outputs", "ot", OpenMaya.MFnData.kString
        )
        cls.addAttribute(cls.output)

        cls.attributeAffects(cls.input, cls.output)


class _PipeMayaAssetNode(PipeMayaNode):
    # lass PipeMayaAssetNode(OpenMayaMPx.MPxTransform):

    attributeType = "asset"

    example = {
        "project": "Ranj and Rani",
        "category": "assets",
        "entityName": "raja",
        "entityId": "11666086-4430-46a6-8aef-2c0fc41fc06e",
        "taskName": "Puppet",
        "taskId": "94d984bd-7f6c-4816-a3c7-c12804a190a5",
        "assetName": "assets|raja|Puppet",
        "assetId": "39636d96-8997-4996-9751-096c969cb7b6",
        "kind": "submit",
        "version": "0.0.1",
        "versionId": "11e689f0-edbf-4602-b5cc-9a8d0bccca52",
        "filename": None,
        "extension": None,
        "releasedAt": "2022:May:15:Sunday-02:10:56:PM",
        "releasedBy": "tony.williams@example.com",
        "status": "Approved",
        "statusAt": "2022:May:15:Sunday-10:11:55:PM",
        "statusBy": "subing85@gmail.com",
        "assignments": ["tony.williams"],
        "dependency": None,
        "comment": "",
    }

    filepath = OpenMaya.MObject()
    metadata = OpenMaya.MObject()

    nodeId = OpenMaya.MTypeId(0x0001)
    kTransformMatrixID = OpenMaya.MTypeId(0x1000)
    kPluginNodeTypeName = "pipeAssetNode"

    def __init__(self):
        super(PipeMayaAssetNode, self).__init__()

    @classmethod
    def initializer(cls):

        cls.filepath = PipeMayaNode.createStringAttribute(
            cls.filepath,
            "filepath",
            "fp",
            filepath=True,
            default="/test.json",
        )

        cls.metadata = PipeMayaNode.createStringAttribute(
            cls.metadata, "metadata", "md", default="{}"
        )

        # cls.filepath = PipeMayaAssetNode.createFilepathAttribute(cls.filepath)
        # cls.metadata = PipeMayaAssetNode.createMetadataAttribute(cls.metadata)
        # cls.parent = PipeMayaAssetNode.createParentAttribute()

        cls.lod = PipeMayaAssetNode.createLodAttribute()
        cls.input = PipeMayaAssetNode.createInputAttribute()
        cls.output = PipeMayaAssetNode.createOutAttribute()
        cls.attributeAffects(cls.input, cls.output)

        context = cls.attributeList()
        for each in context:
            outAttribute = OpenMaya.MObject()
            outAttribute = PipeMayaNode.createStringAttribute(
                outAttribute, each["fn"], each["sn"]
            )
            cls.outAttributes.append(outAttribute)
            cls.attributeAffects(cls.metadata, outAttribute)
            cls.attributeAffects(cls.filepath, outAttribute)

        cls.attributeAffects(cls.filepath, cls.metadata)


class PipeModelNode(PipeMayaAssetNode):
    attributeType = "asset"
    nodeId = OpenMaya.MTypeId(0x0002)
    kTransformMatrixID = OpenMaya.MTypeId(0x2000)
    kPluginNodeTypeName = "pipeModelNode"

    @classmethod
    def initializer(cls):
        # super(PipeModelNode).initializer()
        PipeMayaAssetNode.initializer()

        # PipeMayaAssetNode.lod, PipeMayaAssetNode.lodOut = PipeMayaAssetNode.createLodAttribute()

        # print (PipeMayaAssetNode.lod, PipeMayaAssetNode.lodOut)

        # cls.attributeAffects(PipeMayaAssetNode.lod, PipeMayaAssetNode.lodOut)


class PipeLookdevNode(PipeMayaAssetNode):
    attributeType = "asset"
    nodeId = OpenMaya.MTypeId(0x0003)
    kTransformMatrixID = OpenMaya.MTypeId(0x3000)
    kPluginNodeTypeName = "pipeLookdevNode"

    @classmethod
    def initializer(cls):
        PipeMayaAssetNode.initializer()


class PipeGroomNode(PipeMayaAssetNode):
    attributeType = "asset"
    nodeId = OpenMaya.MTypeId(0x0004)
    kTransformMatrixID = OpenMaya.MTypeId(0x4000)
    kPluginNodeTypeName = "pipeGroomNode"

    @classmethod
    def initializer(cls):
        PipeMayaAssetNode.initializer()


class PipePuppetNode(PipeMayaAssetNode):
    attributeType = "asset"
    nodeId = OpenMaya.MTypeId(0x0005)
    kTransformMatrixID = OpenMaya.MTypeId(0x5000)
    kPluginNodeTypeName = "pipePuppetNode"

    @classmethod
    def initializer(cls):
        PipeMayaAssetNode.initializer()


class PipeMayaShotNode(PipeMayaNode):
    attributeType = "shot"
    nodeId = OpenMaya.MTypeId(0x0006)
    kTransformMatrixID = OpenMaya.MTypeId(0x6000)
    kPluginNodeTypeName = "pipeShotNode"


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
        return obj.attributeList()

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
