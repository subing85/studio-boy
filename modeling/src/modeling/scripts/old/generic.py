import os
import stat

from maya import cmds
from maya import OpenMaya

from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def export_scene(
    filepath,
    format="mayaAscii",
    overridepaths=None,
    preserve_rferences=False,
):
    if os.path.isfile(filepath):
        os.chmod(filepath, stat.S_IWRITE)
        os.remove(filepath)
    OpenMaya.MFileIO.exportAll(filepath, format, preserve_rferences)
    if not overridepaths:
        return filepath
    os.chmod(filepath, stat.S_IREAD)
    return filepath


def puppet_hierarchy():
    nodes = [
        "world",
        "control",
        "controls",
        "geometry",
        "hires",
        "lores",
        "transform" "lod_rvs",
        "display_mdn",
    ]
    for each in nodes:
        if not cmds.objExists(each):
            continue
        LOGGER.warning(
            'already exists node called, "%s" rename the node and try!...'
            % each
        )
        return
    world = cmds.group(em=1, n="world")
    control = cmds.group(em=1, n="control")
    controls = cmds.group(em=1, n="controls")
    geometry = cmds.group(em=1, n="geometry")
    hires = cmds.group(em=1, n="hires")
    lores = cmds.group(em=1, n="lores")
    transform = cmds.circle(nr=(0, 1, 0), r=5, n="transform")[0]
    reverse = cmds.shadingNode("reverse", asUtility=True, n="lod_rvs")
    multiplydivide = cmds.shadingNode(
        "multiplyDivide", asUtility=True, n="display_mdn"
    )

    cmds.parent(control, geometry, world)
    cmds.parent(transform, control)
    cmds.parent(controls, control)
    cmds.parent(hires, lores, geometry)

    cmds.addAttr(
        transform, ln="lod", at="enum", en="LoRes:HiRes", k=True
    )
    cmds.addAttr(
        transform,
        ln="geometryDisplay",
        at="enum",
        en="Normal:Reference",
        k=True,
    )
    cmds.addAttr(
        transform,
        ln="controlVisibility",
        at="enum",
        en="Off:On",
        k=True,
    )
    cmds.setAttr("%s.lod" % transform, cb=True)
    cmds.setAttr("%s.geometryDisplay" % transform, cb=True)
    cmds.setAttr("%s.controlVisibility" % transform, cb=True)
    cmds.setAttr("%s.lod" % transform, 1)
    cmds.setAttr("%s.geometryDisplay" % transform, 1)
    cmds.setAttr("%s.controlVisibility" % transform, 1)
    cmds.setAttr("%s.input2X" % multiplydivide, 2)
    cmds.setAttr("%s.v" % transform, l=True, k=False, cb=False)

    cmds.connectAttr(
        "%s.controlVisibility" % transform, "%s.v" % controls, f=True
    )
    cmds.connectAttr("%s.lod" % transform, "%s.v" % hires, f=True)
    cmds.connectAttr(
        "%s.lod" % transform, "%s.inputX" % reverse, f=True
    )
    cmds.connectAttr("%s.outputX" % reverse, "%s.v" % lores, f=True)

    cmds.setAttr("%s.overrideEnabled" % geometry, True)
    cmds.setAttr("%s.overrideEnabled" % geometry, l=True)

    cmds.connectAttr(
        "%s.geometryDisplay" % transform,
        "%s.input1X" % multiplydivide,
        f=True,
    )
    cmds.connectAttr(
        "%s.outputX" % multiplydivide,
        "%s.overrideDisplayType" % geometry,
        f=True,
    )

    cmds.parentConstraint(transform, geometry, w=True)
    cmds.scaleConstraint(transform, geometry, o=(1, 1, 1), w=True)

    LOGGER.warning("success, created asset hierarchy")
    return True
