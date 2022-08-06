import os
import stat
import json
import shutil
import tempfile

from common import resources
from pipe.core import logger
from common.pipefile import Create

LOGGER = logger.getLogger(__name__)


class TimeUnit(object):
    @classmethod
    def scene(cls):
        units = {
            "game": 15,
            "film": 24,
            "pal": 25,
            "ntsc": 30,
            "show": 48,
            "palf": 50,
        }
        from maya import cmds

        fps = units.get(cmds.currentUnit(q=1, time=1), "25")
        return fps


class ImageFormat(object):
    @classmethod
    def formatManager(cls):
        from maya.app.general import createImageFormats

        formatmanager = createImageFormats.ImageFormats()
        return formatmanager

    @classmethod
    def getDescription(cls, format):
        formatmanager = cls.formatManager()
        imagedescriptor = formatmanager.findKey(format)
        if not imagedescriptor:
            return
        return imagedescriptor.description

    @classmethod
    def availableFormats(cls):
        formatManager = cls.formatManager()
        for format in formatManager.formats:
            print(format.extension, format.description)


class Playblast(object):
    @classmethod
    def CurrentFrame(cls):
        from maya import cmds

        return int(cmds.currentTime(q=True))

    @classmethod
    def FrameByFrame(cls, **kwargs):
        from maya import cmds

        format = kwargs.get("format", "image")
        widthHeight = kwargs.get("widthHeight", [1024, 1024])
        clearCache = kwargs.get("clearCache", False)
        viewer = kwargs.get("viewer", False)
        showOrnaments = kwargs.get("showOrnaments", False)
        fp = kwargs.get("showOrnaments", TimeUnit.scene())
        percent = kwargs.get("percent", 100)
        compression = kwargs.get("compression", "tif")
        extension = kwargs.get("extension", "tif")

        quality = kwargs.get("quality", 100)
        padding = kwargs.get("padding", 5)

        filepath = kwargs.get("filepath")
        if not filepath:
            filepath = Create.tempFile()

        fstart = kwargs.get("fstart", int(cmds.currentTime(q=True)))
        fend = kwargs.get("fend", int(cmds.currentTime(q=True)))

        camera = cmds.lookThru(q=True)
        cmds.setAttr("%s.overscan" % camera, 1)
        cmds.select(cl=True)

        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        outputs = []
        for frame in range(fstart, fend + 1, 1):
            index = str(frame).zfill(padding)
            completeFilename = "%s-%s.%s" % (
                filepath,
                index,
                extension,
            )
            context = {
                "format": format,
                "completeFilename": completeFilename,
                "frame": [frame],
                "clearCache": clearCache,
                "viewer": viewer,
                "showOrnaments": showOrnaments,
                "fp": fp,
                "percent": percent,
                "compression": compression,
                "quality": quality,
                "widthHeight": widthHeight,
            }
            # cmds.currentTime(frame)
            image = cmds.playblast(**context)
            outputs.append(image)
        return outputs

    @classmethod
    def FramesByRange(cls, **kwargs):
        from maya import cmds

        format = kwargs.get("format") or "tif"
        fstart = kwargs.get("fstart") or int(cmds.currentTime(q=True))
        fend = kwargs.get("fend") or int(cmds.currentTime(q=True))
        tempdir = tempfile.mktemp("Playblast", tempfile.gettempdir())
        filepath = kwargs.get("filepath") or tempdir
        resolution = kwargs.get("resolution") or [1024, 1024]
        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        camera = cmds.lookThru(q=True)
        cmds.setAttr("%s.overscan" % camera, 1)
        cmds.select(cl=True)

        context = {
            "format": "image",
            "filename": filepath,
            "frame": range(fstart, fend + 1),
            "framePadding": 4,
            "clearCache": False,
            "viewer": False,
            "showOrnaments": False,
            "percent": 100,
            "compression": format,
            "quality": 100,
            "widthHeight": resolution,
        }
        image = cmds.playblast(**context)
        return image


class LiveRender(object):
    @classmethod
    def FrameByFrame(cls, **kwargs):
        from maya import cmds
        from maya import mel

        widthHeight = kwargs.get("widthHeight", [1024, 1024])
        percent = kwargs.get("percent", 100)
        extension = kwargs.get("extension", "tga")
        compression = kwargs.get("compression")

        quality = kwargs.get("quality", 100)
        padding = kwargs.get("padding", 5)

        filepath = kwargs.get("filepath")
        if not filepath:
            filepath = Create.tempFile()

        fstart = kwargs.get("fstart", int(cmds.currentTime(q=True)))
        fend = kwargs.get("fend", int(cmds.currentTime(q=True)))

        camera = cmds.lookThru(q=True)
        cmds.setAttr("%s.overscan" % camera, 1)
        cmds.select(cl=True)

        cmds.setAttr("defaultRenderGlobals.extensionPadding", padding)
        cmds.setAttr("defaultResolution.width", widthHeight[0])
        cmds.setAttr("defaultResolution.height", widthHeight[1])

        if not compression:
            compression = ImageFormat.getDescription(extension)

        formatManager = ImageFormat.formatManager()
        formatManager.pushRenderGlobalsForDesc(compression)

        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        outputs = []
        for frame in range(fstart, fend + 1, 1):
            cmds.currentTime(frame)
            mel.eval("renderWindowRenderCamera render renderView %s;" % camera)
            index = str(frame).zfill(padding)
            completeFilename = "%s-%s.%s" % (
                filepath,
                index,
                extension,
            )
            cmds.renderWindowEditor("renderView", e=True, writeImage=completeFilename)
            formatManager.popRenderGlobals()
            outputs.append(completeFilename)
        return outputs


class RenderCamera(object):

    lookThruCamera = None
    cameraNodes = list()

    @classmethod
    def create(cls, fstart, fend, kstart=0, kend=360):
        from maya import cmds

        current_camera = cmds.lookThru(q=True)
        mov_camera = cmds.camera()
        constraint = cmds.parentConstraint(
            current_camera, mov_camera[0], mo=False, w=True
        )
        cmds.delete(constraint)
        cmds.lookThru(mov_camera[1])
        camera_group = cmds.group(em=True)
        cmds.parent(mov_camera[0], camera_group)
        cmds.setAttr("%s.overscan" % mov_camera[1], 1)
        anim_curve = cmds.createNode("animCurveTA")
        cmds.connectAttr("%s.output" % anim_curve, "%s.rotateY" % camera_group)
        cmds.keyTangent(anim_curve, e=True, wt=False)
        cmds.setAttr("%s.preInfinity" % anim_curve, 0)
        cmds.setAttr("%s.postInfinity" % anim_curve, 0)
        cmds.setKeyframe(anim_curve, time=fstart, value=kstart)
        cmds.setKeyframe(anim_curve, time=fend, value=-kend)
        cmds.keyTangent(
            anim_curve,
            e=1,
            t=(fstart, fend),
            itt=("linear"),
            ott=("linear"),
        )
        cls.lookThruCamera = current_camera
        cls.cameraNodes = [camera_group, mov_camera[0], anim_curve]

    @classmethod
    def delete(cls):
        from maya import cmds

        if cls.lookThruCamera:
            cmds.lookThru(cls.lookThruCamera)
        for node in cls.cameraNodes:
            if not cmds.objExists(node):
                continue
            cmds.delete(node)
