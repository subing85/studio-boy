from common import hierarchy
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Asset(hierarchy.Asset):

    nodeType = "pipeModelNode"
    name = "Model"
    hierarchy = [
        "|Model",
        "|Model|Proxy",
        "|Model|LoRes",
        "|Model|HiRes",
    ]

    @classmethod
    def create(cls):
        from maya import cmds

        root = cls.createNode()
        proxy = cmds.group(em=1, n="Proxy")
        lores = cmds.group(em=1, n="LoRes")
        hires = cmds.group(em=1, n="HiRes")
        cmds.parent([proxy, lores, hires], root)
        cmds.connectAttr(
            "%s.lodInput0" % root, "%s.visibility" % proxy
        )
        cmds.connectAttr(
            "%s.lodInput1" % root, "%s.visibility" % lores
        )
        cmds.connectAttr(
            "%s.lodInput2" % root, "%s.visibility" % hires
        )
        return root, [proxy, lores, hires]

    @staticmethod
    def currentLod(self, node=None):
        pass

    @staticmethod
    def lodNode(self, node=None):
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
#         hierarchy = [
#             "|world",
#             "|world|control",
#             "|world|control|transform",
#             "|world|control|controls",
#             "|world|geometry",
#             "|world|geometry|hires",
#             "|world|geometry|lores",
#         ]
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
#     def create(cls):
#         from maya import cmds
#
#         if cls.hasExists():
#             return
#         world = cmds.group(em=1, n=cls.transforms[0])
#         control = cmds.group(em=1, n=cls.transforms[1])
#         controls = cmds.group(em=1, n=cls.transforms[2])
#         geometry = cmds.group(em=1, n=cls.transforms[3])
#         hires = cmds.group(em=1, n=cls.transforms[4])
#         lores = cmds.group(em=1, n=cls.transforms[5])
#         transform = cmds.circle(nr=(0, 1, 0), r=5, n=cls.transforms[6])[0]
#         reverse = cmds.shadingNode("reverse", asUtility=True, n=cls.nodes[0])
#         multiplydivide = cmds.shadingNode(
#             "multiplyDivide", asUtility=True, n=cls.nodes[1]
#         )
#
#         cmds.parent(control, geometry, world)
#         cmds.parent(transform, control)
#         cmds.parent(controls, control)
#         cmds.parent(hires, lores, geometry)
#
#         cmds.addAttr(transform, ln="lod", at="enum", en="LoRes:HiRes", k=True)
#         cmds.addAttr(
#             transform,
#             ln="geometryDisplay",
#             at="enum",
#             en="Normal:Reference",
#             k=True,
#         )
#         cmds.addAttr(
#             transform,
#             ln="controlVisibility",
#             at="enum",
#             en="Off:On",
#             k=True,
#         )
#         cmds.setAttr("%s.lod" % transform, cb=True)
#         cmds.setAttr("%s.geometryDisplay" % transform, cb=True)
#         cmds.setAttr("%s.controlVisibility" % transform, cb=True)
#         cmds.setAttr("%s.lod" % transform, 1)
#         cmds.setAttr("%s.geometryDisplay" % transform, 1)
#         cmds.setAttr("%s.controlVisibility" % transform, 1)
#         cmds.setAttr("%s.input2X" % multiplydivide, 2)
#         cmds.setAttr("%s.v" % transform, l=True, k=False, cb=False)
#
#         cmds.connectAttr(
#             "%s.controlVisibility" % transform,
#             "%s.v" % controls,
#             f=True,
#         )
#         cmds.connectAttr("%s.lod" % transform, "%s.v" % hires, f=True)
#         cmds.connectAttr("%s.lod" % transform, "%s.inputX" % reverse, f=True)
#         cmds.connectAttr("%s.outputX" % reverse, "%s.v" % lores, f=True)
#
#         cmds.setAttr("%s.overrideEnabled" % geometry, True)
#         cmds.setAttr("%s.overrideEnabled" % geometry, l=True)
#
#         cmds.connectAttr(
#             "%s.geometryDisplay" % transform,
#             "%s.input1X" % multiplydivide,
#             f=True,
#         )
#         cmds.connectAttr(
#             "%s.outputX" % multiplydivide,
#             "%s.overrideDisplayType" % geometry,
#             f=True,
#         )
#
#         cmds.parentConstraint(transform, geometry, w=True)
#         cmds.scaleConstraint(transform, geometry, o=(1, 1, 1), w=True)
#
#         LOGGER.warning("success, created asset hierarchy")
#         return True
# ===================================================================================================
