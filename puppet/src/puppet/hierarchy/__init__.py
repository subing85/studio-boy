from common import hierarchy
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

import importlib

importlib.reload(hierarchy)


class Asset(hierarchy.Asset):

    nodeType = "pipePuppetNode"
    name = "Puppet"

    hierarchy = [
        "|Puppet",
        "|Puppet|control",
        "|Puppet|control|transform",
        "|Puppet|control|controls",
        "|Puppet|Model|Proxy",
        "|Puppet|Model|LoRes",
        "|Puppet|Model|HiRes",
    ]

    @classmethod
    def create(cls):
        from maya import cmds

        if cls.hasExists():
            LOGGER.warning("already exists puppet hierarchy in the scene.")
            return

        modelNodes = Asset.getModelNodes()
        if not modelNodes:
            raise Exception("could not find model hierarchy.")
        if len(modelNodes) > 2:
            raise Exception("more the one model hierarchy found in the scene.")

        modelNode = modelNodes[0]

        root = cls.createNode()
        control = cmds.group(em=1, n="control")
        controls = cmds.group(em=1, n="controls")
        transform = cmds.circle(nr=(0, 1, 0), r=5, n="transform")[0]

        cmds.parent(control, root)
        cmds.parent(transform, control)
        cmds.parent(controls, control)

        cmds.addAttr(
            transform,
            ln="LOD",
            at="enum",
            en="Proxy:LoRes:HiRes",
            k=True,
        )
        cmds.addAttr(
            transform,
            ln="geometryDisplay",
            at="enum",
            en="Normal:Template:Reference",
            k=True,
        )
        cmds.addAttr(
            transform,
            ln="controlVisibility",
            at="enum",
            en="Off:On",
            k=True,
        )

        if modelNodes:
            cmds.parent(modelNodes, root)
            cmds.parentConstraint(transform, modelNode, w=True)
            cmds.scaleConstraint(transform, modelNode, o=(1, 1, 1), w=True)
            cmds.connectAttr("%s.LOD" % transform, "%s.LOD" % modelNode, f=True)
            cmds.connectAttr(
                "%s.geometryDisplay" % transform,
                "%s.overrideDisplayType" % modelNode,
                f=True,
            )
            cmds.setAttr("%s.overrideEnabled" % modelNode, 1)

        cmds.connectAttr(
            "%s.controlVisibility" % transform,
            "%s.visibility" % controls,
            f=True,
        )

        cmds.setAttr("%s.LOD" % transform, cb=True)
        cmds.setAttr("%s.geometryDisplay" % transform, cb=True)
        cmds.setAttr("%s.controlVisibility" % transform, cb=True)
        cmds.setAttr("%s.LOD" % transform, 0)
        cmds.setAttr("%s.geometryDisplay" % transform, 2)
        cmds.setAttr("%s.controlVisibility" % transform, 1)
        cmds.setAttr("%s.visibility" % transform, l=True, k=False, cb=False)

        cmds.select(cl=True)

        LOGGER.warning("success, created puppet hierarchy")
        return True

    @classmethod
    def createCamera(cls):
        from maya import cmds

        if cls.hasExists():
            LOGGER.warning("already exists puppet hierarchy in the scene.")
            return

        cameraNodes = Asset.getModelNodes()

        if not cameraNodes:
            cameraNodes = [cls.createNode(nodeType="pipeCameraNode", name="Camera")]

        if cameraNodes and len(cameraNodes) > 2:
            raise Exception("more the one model hierarchy found in the scene.")

        cameraNode = cameraNodes[0]

        root = cls.createNode()
        control = cmds.group(em=1, n="control")
        controls = cmds.group(em=1, n="controls")
        transform = Asset.createSweepCircle(name="transform")
        cmds.parent(control, root)
        cmds.parent(transform, control)
        cmds.parent(controls, control)

        cmds.parent(cameraNode, root)
        cmds.parentConstraint(transform, cameraNode, w=True)
        
        cmds.setAttr("%s.visibility" % transform, l=True, k=False, cb=False)
        cmds.setAttr("%s.scaleX" % transform, l=True, k=False, cb=False)
        cmds.setAttr("%s.scaleY" % transform, l=True, k=False, cb=False)
        cmds.setAttr("%s.scaleZ" % transform, l=True, k=False, cb=False)
        
        cmds.select(cl=True)

        LOGGER.warning("success, created camera hierarchy")
        return True


    @staticmethod
    def createSweepCircle(name):
        from maya import cmds
        sweepCircle = cmds.circle(nr=(0, 1, 0), r=5, sweep=225, n=name)[0]
        cmds.setAttr("%s.rotateY" % sweepCircle, 68)
        cmds.makeIdentity(sweepCircle, apply=True, t=True, r=True, s=True, n=2)
        cmds.bakePartialHistory(sweepCircle, prePostDeformers=True)
        return sweepCircle

    @staticmethod
    def getModelNodes():
        modelNodes = Asset.get(nodeType="pipeModelNode")
        return modelNodes

    @staticmethod
    def getCameraNodes():
        modelNodes = Asset.get(nodeType="pipeCameraNode")
        return modelNodes

    @staticmethod
    def currentLod(node=None):
        pass

    @staticmethod
    def lodNode(node=None):
        pass


# ===================================================================================================
# class _Asset(object):
#
#     transforms = [
#         "world",
#         "control",
#         "controls",
#         "geometry",
#         "hires",
#         "lores",
#         "transform",
#     ]
#     nodes = ["lod_rvs", "display_mdn"]
#     default = ["persp", "top", "front", "side", "|%s" % transforms[0]]
#
#     @classmethod
#     def hasExists(cls):
#         from maya import cmds
#
#         nodes = cls.transforms + cls.nodes
#         for each in nodes:
#             if not cmds.objExists(each):
#                 continue
#             LOGGER.warning("already exists node called, <%s>" % each)
#             return True
#         return False
#
#     @classmethod
#     def validate(cls):
#         from maya import cmds
#

#         invalid_nodes = {}
#         for each in hierarchy:
#             if cmds.objExists(each):
#                 continue
#             invalid_nodes.setdefault("missing", []).append(each)
#         top_level_nodes = cmds.ls(assemblies=True)
#         unwant_nodes = []
#         for node in top_level_nodes:
#             if node in cls.default:
#                 continue
#             invalid_nodes.setdefault("unwanted", []).append(node)
#         return invalid_nodes
#
#     @classmethod
#     def createModel(cls):
#         from pipe.nodes import PipeNode
#
#         PipeNode.create(typed="pipeModelNode", name="model1")
#
#
#
#
#     @classmethod
#     def createLookdev(cls):
#         pass
#
#     @classmethod
#     def createGroom(cls):
#         pass
#
#     @classmethod
#     def createPuppet(cls):
#         pass
#
#     @classmethod
