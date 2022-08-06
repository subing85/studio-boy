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
