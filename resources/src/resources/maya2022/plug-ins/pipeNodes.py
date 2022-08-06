import sys
import importlib

from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

from pipe.nodes.plugins import PipeShotNode
from pipe.nodes.plugins import PipeGroomNode
from pipe.nodes.plugins import PipeModelNode
from pipe.nodes.plugins import PipePuppetNode
from pipe.nodes.plugins import PipeCameraNode
from pipe.nodes.plugins import PipeLookdevNode


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(
        mobject, "Pipe-Studio maya nodes", "0.0.1"
    )

    matrix = OpenMayaMPx.MPxTransformationMatrix

    mplugin.registerTransform(
        PipeModelNode.kPluginNodeTypeName,
        PipeModelNode.nodeId,
        PipeModelNode.creator,
        PipeModelNode.initializer,
        matrix,
        PipeModelNode.kTransformMatrixID,
    )

    mplugin.registerTransform(
        PipeLookdevNode.kPluginNodeTypeName,
        PipeLookdevNode.nodeId,
        PipeLookdevNode.creator,
        PipeLookdevNode.initializer,
        matrix,
        PipeLookdevNode.kTransformMatrixID,
    )

    mplugin.registerTransform(
        PipeGroomNode.kPluginNodeTypeName,
        PipeGroomNode.nodeId,
        PipeGroomNode.creator,
        PipeGroomNode.initializer,
        matrix,
        PipeGroomNode.kTransformMatrixID,
    )

    mplugin.registerTransform(
        PipePuppetNode.kPluginNodeTypeName,
        PipePuppetNode.nodeId,
        PipePuppetNode.creator,
        PipePuppetNode.initializer,
        matrix,
        PipePuppetNode.kTransformMatrixID,
    )

    mplugin.registerTransform(
        PipeCameraNode.kPluginNodeTypeName,
        PipeCameraNode.nodeId,
        PipeCameraNode.creator,
        PipeCameraNode.initializer,
        matrix,
        PipeCameraNode.kTransformMatrixID,
    )

    mplugin.registerTransform(
        PipeShotNode.kPluginNodeTypeName,
        PipeShotNode.nodeId,
        PipeShotNode.creator,
        PipeShotNode.initializer,
        matrix,
        PipeShotNode.kTransformMatrixID,
    )
    
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterNode(PipeModelNode.nodeId)
    mplugin.deregisterNode(PipeLookdevNode.nodeId)
    mplugin.deregisterNode(PipeGroomNode.nodeId)
    mplugin.deregisterNode(PipePuppetNode.nodeId)
    mplugin.deregisterNode(PipeCameraNode.nodeId)
    mplugin.deregisterNode(PipeShotNode.nodeId)
