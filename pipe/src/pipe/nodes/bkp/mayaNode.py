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
