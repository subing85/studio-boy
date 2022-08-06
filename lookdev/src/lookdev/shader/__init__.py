import os
import json

from pipe import utils
from apis import studio
from common.pipefile import Create


from common import shader
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class SearchShaders(shader.SearchShaders):
    pass


class SetDefultShader(shader.SetDefultShader):
    pass


class SearchLookdevShader(object):
    @classmethod
    def getShapeNodes(cls, geometries=None):
        from maya import mel
        from maya import cmds

        geometries = geometries or mel.eval(
            'listTransforms "-type mesh"'
        )
        shapes = []
        for geometry in geometries:
            shape = cmds.listRelatives(geometry, type="shape")
            shapes.append(shape[0])
        return shapes

    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        default_shaders = cmds.ls(defaultNodes=True, materials=True)
        shapes = cls.getShapeNodes()
        context = {}
        for shape in shapes:
            shding_engines = cmds.listConnections(
                shape, type="shadingEngine"
            )
            if not shding_engines:
                context.setdefault(
                    "not assign any shaders", []
                ).append(shape)
                continue
            dependency_nodes = cmds.listConnections(shding_engines)
            shaders = list(
                set(cmds.ls(dependency_nodes, materials=True))
            )
            for shader in shaders:
                if shader not in default_shaders:
                    continue
                key = "assign default shader <%s>" % shader
                context.setdefault(key, []).append(shape)
        return context


class SearchBrokenShaders(object):
    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        default_nodes = cmds.ls(defaultNodes=True)
        shaders = cmds.ls(materials=True)
        context = {}
        for shader in shaders:
            if shader in default_nodes:
                continue
            dependency_nodes = cmds.listConnections(shader)
            shading_engines = list(
                set(cmds.ls(dependency_nodes, type="shadingEngine"))
            )
            if not shading_engines:
                context.setdefault("broken shader", []).append(shader)
                continue
            for shading_engine in shading_engines:
                if shading_engine in default_nodes:
                    continue
                geometries = cmds.sets(shading_engine, q=True)
                if geometries:
                    continue
                context.setdefault("unassigned shader", []).append(
                    shader
                )
        return context


class ClearAssignments(object):
    @classmethod
    def doIt(cls, geometries):
        from maya import cmds

        context = dict()
        for each in geometries:
            node = each
            if "." in each:
                node = cmds.listRelatives(each, p=1)[0]
            shdingnodes = cmds.listConnections(
                node, type="shadingEngine"
            )
            if not shdingnodes:
                continue
            for shdingnode in shdingnodes:
                if shdingnode in context:
                    if node in context.get(shdingnode):
                        continue
                context.setdefault(shdingnode, []).append(node)
        for k, v in context.items():
            cmds.sets(v, rm=k)


class CreatePuppetShader(object):
    def __init__(self, version=None):
        self.version = version

    def getShaderSD(self, version, dirname=None):

        print("version", version)
        components = list(
            filter(
                lambda k: k["name"] == "shader"
                and k["file_type"] == ".json",
                version["components"],
            )
        )
        if not components:
            LOGGER.warning(
                "could not find any shader components from <%s>"
                % version
            )
            return

        component = components[0]

        if not dirname:
            name = "%s-%s-" % (
                version["task"]["parent"]["name"],
                version["task"]["name"],
            )
            dirname = Create.tempDirectory(name)
        vern = studio.Versions()
        filepath = vern.toDownload(component, dirname)

        with open(filepath, "r") as file:
            context = json.load(file)
            return context
        return context

    def getSourceFiles(self, context):
        source_files = []
        if not context.get("sourcefiles"):
            return source_files

        for x in context["sourcefiles"]:
            if not x.get("path"):
                continue
            if x["path"] in source_files:
                continue
            source_files.append(x["path"])
        return source_files

    @classmethod
    def doIt(
        cls, task=None, version=None, dirname=None, context=None
    ):
        version = version or cls.version

        if not dirname:
            name = "%s-%s-" % (
                version["task"]["parent"]["name"],
                version["task"]["name"],
            )
            dirname = Create.tempDirectory(name)

        sdcontext = cls.getShaderSD(cls, version, dirname=dirname)

        vers = studio.Versions()
        comp = studio.Components()
        meda = studio.Media()

        versionpath, name = vers.getVersionPath(version)
        kindpath = vers.kindPath(context["kind"], task=task)

        # targetdirname = utils.setPathResolver(kindpath, folders=[context["relative-path"]])
        targetdirname = utils.setPathResolver(kindpath)

        components = version["components"]

        for each in sdcontext:
            sourceimages = cls.getSourceFiles(cls, each)
            if not sourceimages:
                continue
            sourceimage = sourceimages[0]
            filename, format = os.path.splitext(
                os.path.basename(sourceimage)
            )
            source_components = comp.getComponents(
                components,
                name="sourceimages",
                format=format,
                filename=filename,
            )
            if not source_components:
                continue
            source_component = source_components[0]
            filepath = vers.toDownload(
                source_component, targetdirname, readOnly=False
            )

            outputPath = meda.saveResizeImage(filepath, **context)
            LOGGER.info(
                "resize into the %s x %s"
                % (context["width"], context["height"])
            )
            filename = utils.getFileName(outputPath)
            cls.loResShaderNewtwork(
                cls,
                outputPath,
                name=filename,
                assignments=each.get("geometry"),
            )

    def loResShaderNewtwork(
        self, filepath, name=None, assignments=None
    ):
        from maya import cmds

        name = name or utils.getFileName(filepath)

        blinn = cmds.shadingNode(
            "blinn", asShader=True, n="%s_shad" % name
        )

        cmds.setAttr("%s.eccentricity" % blinn, 0.47)
        cmds.setAttr("%s.specularRollOff" % blinn, 0.253)
        cmds.setAttr(
            "%s.specularColor" % blinn,
            0.247,
            0.247,
            0.247,
            type="double3",
        )

        shadingengine = cmds.sets(
            r=True, nss=True, n="%s_shdn" % blinn
        )
        cmds.connectAttr(
            "%s.outColor" % blinn, "%s.surfaceShader" % shadingengine
        )

        if assignments:
            # ClearAssignments.doIt(assignments)
            cmds.sets(assignments, e=True, forceElement=shadingengine)

        nodes = [blinn, shadingengine]
        if not filepath:
            return nodes

        file = cmds.shadingNode(
            "file", asUtility=True, n="%s_file" % name
        )
        placetexture = cmds.shadingNode(
            "place2dTexture",
            isColorManaged=True,
            asTexture=True,
            n="%s_2dtx" % name,
        )
        cmds.setAttr(
            "%s.fileTextureName" % file, filepath, type="string"
        )
        cmds.connectAttr("%s.outColor" % file, "%s.color" % blinn)
        cmds.connectAttr(
            "%s.outUV" % placetexture, "%s.uvCoord" % file
        )
        cmds.connectAttr(
            "%s.outUvFilterSize" % placetexture,
            "%s.uvFilterSize" % file,
        )
        cmds.connectAttr(
            "%s.coverage" % placetexture, "%s.coverage" % file
        )
        cmds.connectAttr(
            "%s.translateFrame" % placetexture,
            "%s.translateFrame" % file,
        )
        cmds.connectAttr(
            "%s.rotateFrame" % placetexture, "%s.rotateFrame" % file
        )
        cmds.connectAttr(
            "%s.mirrorU" % placetexture, "%s.mirrorU" % file
        )
        cmds.connectAttr(
            "%s.mirrorV" % placetexture, "%s.mirrorV" % file
        )
        cmds.connectAttr(
            "%s.stagger" % placetexture, "%s.stagger" % file
        )
        cmds.connectAttr("%s.wrapU" % placetexture, "%s.wrapU" % file)
        cmds.connectAttr("%s.wrapV" % placetexture, "%s.wrapV" % file)
        cmds.connectAttr(
            "%s.repeatUV" % placetexture, "%s.repeatUV" % file
        )
        cmds.connectAttr(
            "%s.offset" % placetexture, "%s.offset" % file
        )
        cmds.connectAttr(
            "%s.rotateUV" % placetexture, "%s.rotateUV" % file
        )
        cmds.connectAttr(
            "%s.noiseUV" % placetexture, "%s.noiseUV" % file
        )
        cmds.connectAttr(
            "%s.vertexUvOne" % placetexture, "%s.vertexUvOne" % file
        )
        cmds.connectAttr(
            "%s.vertexUvTwo" % placetexture, "%s.vertexUvTwo" % file
        )
        cmds.connectAttr(
            "%s.vertexUvThree" % placetexture,
            "%s.vertexUvThree" % file,
        )
        cmds.connectAttr(
            "%s.vertexCameraOne" % placetexture,
            "%s.vertexCameraOne" % file,
        )
        nodes.extend([file, placetexture])
        return nodes
