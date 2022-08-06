import os
import ast
import json

from maya import OpenMaya
from maya import OpenMayaMPx

from pipe import utils
from pipe import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

ATTRIBUTE_CONTEXT = resources.getInputData("mayaNode")


class PipeMayaNode(OpenMayaMPx.MPxTransform):

    mobject = OpenMaya.MObject()

    filepath = OpenMaya.MObject()
    metadata = OpenMaya.MObject()
    parent = OpenMaya.MObject()
    children = OpenMaya.MObject()

    lod = OpenMaya.MObject()
    lodInput = OpenMaya.MObject()
    input = OpenMaya.MObject()

    lodValues = {0: (1, 0, 0), 1: (0, 1, 0), 2: (0, 0, 1)}

    outAttributes = list()
    attributeType = None

    def __init__(self):
        OpenMayaMPx.MPxTransform.__init__(self)

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeMayaNode())

    @staticmethod
    def getAttributeContext(type):
        context = utils.searchContext(
            ATTRIBUTE_CONTEXT, "label", value=type, first=True
        )
        context = list(
            filter(lambda k: k.get("enable"), context["attributes"])
        )
        return context

    @staticmethod
    def attributeList():
        context = PipeMayaNode.getAttributeContext(
            PipeMayaNode.attributeType
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

    @staticmethod
    def createStringAttribute(fullName, shortName, **kwargs):
        attribute = OpenMaya.MFnTypedAttribute()
        mobject = OpenMaya.MObject()
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
        attribute.setStorable(True)
        attribute.setWritable(True)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createMessageAttribute(fullName, shortName):
        attribute = OpenMaya.MFnMessageAttribute()
        mobject = OpenMaya.MObject()
        mobject = attribute.create(fullName, shortName)
        PipeMayaNode.addAttribute(mobject)
        attribute.setKeyable(False)
        attribute.setStorable(True)
        attribute.setWritable(True)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createEnumAttribute(
        fullName, shortName, fields, channelBox=False
    ):
        attribute = OpenMaya.MFnEnumAttribute()
        mobject = OpenMaya.MObject()
        mobject = attribute.create(fullName, shortName)

        for index, field in enumerate(fields):
            attribute.addField(field, index)

        PipeMayaNode.addAttribute(mobject)

        switch = True if channelBox else False

        attribute.setChannelBox(switch)
        attribute.setKeyable(switch)
        attribute.setStorable(True)
        attribute.setWritable(True)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def create3IntAttribute(fullName, shortName):
        attribute = OpenMaya.MFnNumericAttribute()
        mobject = OpenMaya.MObject()
        mobject = attribute.create(
            fullName, shortName, OpenMaya.MFnNumericData.k3Int
        )
        PipeMayaNode.addAttribute(mobject)
        attribute.setKeyable(False)
        attribute.setStorable(True)
        attribute.setWritable(False)
        attribute.setReadable(True)
        attribute.setHidden(False)
        return mobject

    @staticmethod
    def createFilepathAttribute():
        filepath = PipeMayaNode.createStringAttribute(
            "filepath", "fp", filepath=True, default="/test.json"
        )
        return filepath

    @staticmethod
    def createMetadataAttribute():
        metadata = PipeMayaNode.createStringAttribute(
            "metadata", "md", default="{}"
        )
        return metadata

    @staticmethod
    def createParentAttribute():
        parent = PipeMayaNode.createMessageAttribute("parent", "pt")
        return parent

    @staticmethod
    def createChildenAttribute():
        children = PipeMayaNode.createMessageAttribute(
            "children", "cn"
        )
        return children

    @staticmethod
    def createLodAttribute():
        fields = ["Proxy", "LoRes", "HiRes"]
        lod = PipeMayaNode.createEnumAttribute(
            "LOD", "ld", fields, channelBox=True
        )
        lodInput = PipeMayaNode.create3IntAttribute("lodInput", "li")
        return lod, lodInput
    
    @staticmethod
    def createSceneTypeAttribute():
        fields = ["Layout", "Animation", "Render"]
        sceneType = PipeMayaNode.createEnumAttribute(
            "sceneType", "st", fields, channelBox=True
        )
        return sceneType

    def compute(self, plug, dataBlock):

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

        if plug.isChild() and plug.parent() == self.lodInput:
            inputHandle = dataBlock.inputValue(self.lod)
            value = inputHandle.asInt()
            outputHandle = dataBlock.outputValue(plug.parent())
            x, y, z = self.lodValues[value]
            outputHandle.set3Int(x, y, z)
            outputHandle.setClean()
            dataBlock.setClean(plug)


class PipeModelNode(PipeMayaNode):

    nodeId = OpenMaya.MTypeId(0x0001)
    kTransformMatrixID = OpenMaya.MTypeId(0x1000)
    kPluginNodeTypeName = "pipeModelNode"
    kPipeType = "Model"
    
    lodAttribute = True

    mobject = OpenMaya.MObject()
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

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeModelNode())

    @classmethod
    def initializer(cls):
        cls.filepath = cls.createFilepathAttribute()
        cls.metadata = cls.createMetadataAttribute()
        cls.parent = cls.createParentAttribute()

        if cls.lodAttribute:
            cls.lod, cls.lodInput = cls.createLodAttribute()

        for each in cls.attributeList():
            outAttribute = OpenMaya.MObject()
            outAttribute = cls.createStringAttribute(
                each["fn"], each["sn"]
            )
            cls.outAttributes.append(outAttribute)
            cls.attributeAffects(cls.metadata, outAttribute)
            cls.attributeAffects(cls.filepath, outAttribute)

        cls.attributeAffects(cls.filepath, cls.metadata)

        if cls.lodAttribute:
            cls.attributeAffects(cls.lod, cls.lodInput)


class PipeLookdevNode(PipeModelNode):

    nodeId = OpenMaya.MTypeId(0x0002)
    kTransformMatrixID = OpenMaya.MTypeId(0x2000)
    kPluginNodeTypeName = "pipeLookdevNode"
    kPipeType = "Lookdev"

    mobject = OpenMaya.MObject()
    attributeType = "asset"
    lodAttribute = False

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeLookdevNode())


class PipeGroomNode(PipeLookdevNode):

    nodeId = OpenMaya.MTypeId(0x0003)
    kTransformMatrixID = OpenMaya.MTypeId(0x3000)
    kPluginNodeTypeName = "pipeGroomNode"
    kPipeType = "Groom"

    mobject = OpenMaya.MObject()
    attributeType = "asset"
    lodAttribute = False

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeGroomNode())


class PipePuppetNode(PipeModelNode):

    nodeId = OpenMaya.MTypeId(0x0004)
    kTransformMatrixID = OpenMaya.MTypeId(0x4000)
    kPluginNodeTypeName = "pipePuppetNode"
    kPipeType = "Puppet"

    mobject = OpenMaya.MObject()
    attributeType = "asset"
    lodAttribute = False

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeGroomNode())
    

class PipeCameraNode(PipeModelNode):

    nodeId = OpenMaya.MTypeId(0x0005)
    kTransformMatrixID = OpenMaya.MTypeId(0x5000)
    kPluginNodeTypeName = "pipeCameraNode"
    kPipeType = "Camera"

    mobject = OpenMaya.MObject()
    attributeType = "asset"
    lodAttribute = False

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeGroomNode())
    

class PipeShotNode(PipeMayaNode):

    nodeId = OpenMaya.MTypeId(0x0006)
    kTransformMatrixID = OpenMaya.MTypeId(0x6000)
    kPluginNodeTypeName = "pipeShotNode"
    kPipeType = "Shot"

    mobject = OpenMaya.MObject()
    attributeType = "shot"

    @classmethod
    def creator(cls):
        return OpenMayaMPx.asMPxPtr(PipeGroomNode())
    
    @classmethod
    def initializer(cls):
        cls.filepath = cls.createFilepathAttribute()
        cls.metadata = cls.createMetadataAttribute()
        cls.children = cls.createChildenAttribute()

        cls.sceneType = cls.createSceneTypeAttribute()

        for each in cls.attributeList():
            outAttribute = OpenMaya.MObject()
            outAttribute = cls.createStringAttribute(
                each["fn"], each["sn"]
            )
            cls.outAttributes.append(outAttribute)
            cls.attributeAffects(cls.metadata, outAttribute)
            cls.attributeAffects(cls.filepath, outAttribute)

        cls.attributeAffects(cls.filepath, cls.metadata)

