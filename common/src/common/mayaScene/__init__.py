import os
import stat
import time
import json
import shutil
import subprocess

from pipe import utils
from pipe.core import logger
from pipe.nodes import PipeNode
from common.hierarchy import Shot
from common.pipefile import Create

LOGGER = logger.getLogger(__name__)


class GetAllHistory(object):
    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        geometries = mel.eval('listTransforms "-type mesh"')
        nurbscurve = mel.eval('listTransforms "-type nurbsCurve"')
        nodes = set(geometries + nurbscurve)
        context = {}
        for node in nodes:
            histories = cmds.listHistory(node, pdo=True, gl=True)
            if not histories:
                continue
            histories = [each for each in histories]
            context.setdefault(node, histories)
        return context


class GetNonDeformHistory(object):
    @classmethod
    def doIt(cls):
        from maya import mel
        from maya import cmds

        geometries = mel.eval('listTransforms "-type mesh"')
        nurbscurve = mel.eval('listTransforms "-type nurbsCurve"')
        defomer_nodes = cmds.listNodeTypes("deformer")
        nodes = set(geometries + nurbscurve)
        context = {}
        for node in nodes:
            histories = cmds.listHistory(node, pdo=1, gl=1)
            if not histories:
                continue
            non_defomers = []
            for history in histories:
                node_type = cmds.nodeType(history)
                if node_type in defomer_nodes:
                    continue
                non_defomers.append(history.encode())
            if not non_defomers:
                continue
            context.setdefault(node, non_defomers)
        return context


class DeleteAllHistory(object):
    @classmethod
    def doIt(cls):
        from maya import cmds

        cmds.undoInfo(openChunk=True)
        nodes = GetAll.doIt()
        if not nodes:
            LOGGER.info("could not find history")
            return
        context = {}
        for node in nodes:
            for deform in node[1]:
                if not cmds.objExists(deform):
                    continue
                cmds.delete(deform)
                context.setdefault("deleted", []).append(deform)
            cmds.bakePartialHistory(node, preCache=True)
            context.setdefault("deleted history from", []).append(node)
        cmds.undoInfo(closeChunk=True)
        return context


class DeleteAllNonDeformHistory(object):
    @classmethod
    def doIt(cls):

        from maya import cmds

        cmds.undoInfo(openChunk=True)
        nodes = GetNonDeformHistory.doIt()
        if not nodes:
            LOGGER.info("could not find non deform history")
            return
        context = {}
        for node in nodes:
            cmds.bakePartialHistory(node, prePostDeformers=True)
            context.setdefault("deleted history from", []).append(node)
        cmds.undoInfo(closeChunk=True)
        return context


class Scene(object):

    sourceFileNodes = {
        "file": "fileTextureName",
        "psdFileTex": "fileTextureName",
        "aiImage": "filename",
    }

    @classmethod
    def exportScene(cls, filepath, **kwargs):
        from maya import OpenMaya

        format = kwargs.get("format", "mayaAscii")
        readOnly = kwargs.get("readOnly", False)
        preserve_rferences = kwargs.get("preserve_rferences", False)

        if os.path.isfile(filepath):
            cls.removeFilepath(filepath)

        OpenMaya.MFileIO.exportAll(filepath, format, preserve_rferences)
        if not readOnly:
            return filepath
        os.chmod(filepath, stat.S_IREAD)
        return filepath

    @classmethod
    def exportShader(cls, filepath, **kwargs):
        from maya import OpenMaya

        format = kwargs.get("format", "mayaAscii")
        readOnly = kwargs.get("readOnly", False)
        preserve_rferences = kwargs.get("preserve_rferences", False)
        relativedirname = kwargs.get("relativedirname", None)
        relativepath = kwargs.get("relativepath", False)

        networks = cls.shaderNetworks(
            relativedirname=relativedirname, relativepath=True
        )
        cls.shaderNetworksMetadata(networks)

        shadingEngines = list(map(lambda k: k["shadingEngine"], networks))
        lookdevNode = cls.shaderLink(shadingEngines)

        if not shadingEngines:
            LOGGER.warning("not found shadingEngine in your scene")

        if lookdevNode:
            shadingEngines.append(lookdevNode)

        mselection_list = OpenMaya.MSelectionList()

        for node in shadingEngines:
            mselection_list.add(node)
        OpenMaya.MGlobal.setActiveSelectionList(mselection_list)

        if os.path.isfile(filepath):
            cls.removeFilepath(filepath)

        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        OpenMaya.MFileIO.exportSelected(filepath, format, False)
        OpenMaya.MGlobal.clearSelectionList()

        if not readOnly:
            return filepath

        os.chmod(filepath, stat.S_IREAD)
        return filepath

    @classmethod
    def exportShaderSD(cls, filepath, relativedirname, **kwargs):
        readOnly = kwargs.get("readOnly", False)

        if os.path.isfile(filepath):
            cls.removeFilepath(filepath)

        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        context = cls.shaderNetworks(relativedirname=relativedirname, relativepath=True)

        filepath = cls.write(cls, filepath, context, readOnly=readOnly)
        # ===========================================================================================
        # with open(filepath, "w") as file:
        #     file.write(json.dumps(networks, indent=4))
        # if not readOnly:
        #     return filepath
        # os.chmod(filepath, stat.S_IREAD)
        # ===========================================================================================
        return filepath

    @classmethod
    def shaderNetworks(cls, relativedirname=None, relativepath=False):
        context = cls.getShaderNetworks(
            cls,
            relativedirname=relativedirname,
            relativepath=relativepath,
        )
        return context

    @classmethod
    def shaderNetworksMetadata(cls, metadata):
        context = cls.setShaderNetworksMetadata(cls, metadata)
        return context

    @classmethod
    def shaderLink(cls, shadingEngines):
        lookdevNode = cls.setShaderLink(cls, shadingEngines)
        return lookdevNode

    @classmethod
    def remapping(cls, mayafile, dirname, **kwargs):

        create = kwargs.get("create", False)
        relativedirname = kwargs.get("relativedirname", None)

        sourcefiles = cls.searchSourceFile(relativepath=False)

        if relativedirname:
            dirname = utils.setPathResolver(dirname, folders=[relativedirname])

            if os.path.isdir(dirname) and create:
                utils.detetePath(dirname)

        if not os.path.isdir(dirname) and create:
            os.makedirs(dirname)

        sourcefiles = [each["path"] for each in sourcefiles]
        context = []
        for each in sourcefiles:
            if create:
                try:
                    shutil.copy2(each, dirname)
                except Exception as error:
                    LOGGER.error(error)
            filename = os.path.basename(each)
            if relativedirname:
                targetpath = "%s/%s" % (relativedirname, filename)
            else:
                targetpath = utils.setPathResolver(dirname, folders=[filename])
            context.append([each, targetpath])

        process = subprocess.Popen(
            [
                "pipe",
                "MtRemapping",
                "-s",
                mayafile,
                "-f",
                str(context),
            ],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.wait()
        stdout = process.stdout.readlines()
        stderr = process.stderr.readlines()
        communicate = process.communicate()

        for each in stdout:
            print(each.decode("utf-8").replace("\r\n", ""))

        for each in stderr:
            print(each.decode("utf-8").replace("\r\n", ""))

        return process

    def getShaderNetworks(self, **kwargs):
        relativedirname = kwargs.get("relativedirname", None)
        relativepath = kwargs.get("relativepath", False)

        from maya import cmds

        shadingEngines = self.shadingEngines()
        context = []
        for each in shadingEngines:
            geometries = cmds.sets(each, q=True)
            history = self.shadingEngineHistory(each)
            shader = cmds.listConnections("%s.surfaceShader" % each, s=True, d=False)

            sourcefile = self.findSourceFile(
                history,
                relativedirname=relativedirname,
                relativepath=relativepath,
            )

            network = {
                "shadingEngine": each,
                "history": history,
                "geometry": geometries,
                "shader": shader,
                "sourcefiles": sourcefile,
            }
            context.append(network)
        return context
    
    def setShaderNetworksMetadata(self, metadata):
        from maya import cmds

        for each in metadata:
            shadingEngine = each["shadingEngine"]
            attribute = "%s.metadata" % shadingEngine
            if not cmds.objExists(attribute):
                cmds.addAttr(shadingEngine, ln="metadata", dt="string")
            cmds.setAttr(attribute, lock=False)
            PipeNode.disconnectSourcePlugs(attribute)
            cmds.setAttr(attribute, str(each), type="string")
            cmds.setAttr(attribute, lock=True)

    def setShaderLink(self, shadingEngines):
        from maya import cmds
        from common.hierarchy import Asset

        lookdevNode = Asset.getLookdevNodes(referenced=False, first=True)
        if not lookdevNode:
            raise Exception ("could not find lookdevNode from the scene")
        for shadingEngine in shadingEngines:
            attribute = "%s.metadata" % shadingEngine
            if not cmds.objExists(attribute):
                cmds.addAttr(shadingEngine, ln="metadata", dt="string")
            cmds.setAttr(attribute, lock=False)
            PipeNode.disconnectSourcePlugs(attribute) 
            cmds.connectAttr("%s.message" % lookdevNode, attribute, f=True)
            cmds.setAttr(attribute, lock=True)
        return lookdevNode

    @classmethod
    def shadingEngines(cls):
        from maya import cmds

        shdingengines = cls.getShadingEngine()
        nodes = []
        for each in shdingengines:
            geometries = cmds.sets(each, q=True)
            if not geometries:
                continue
            nodes.append(each)
        return nodes

    @classmethod
    def getShadingEngine(self):
        from maya import cmds

        defaultnodes = cmds.ls(defaultNodes=True)
        shadingEngines = cmds.ls(type="shadingEngine")
        nodes = []
        for each in shadingEngines:
            if each in defaultnodes:
                continue
            nodes.append(each)
        return nodes

    @classmethod
    def shadingEngineHistory(cls, shadingEngine):
        from maya import cmds

        history = cmds.listHistory(shadingEngine, pdo=True, gl=True)
        if shadingEngine in history:
            history.remove(shadingEngine)
        return history

    @classmethod
    def shadingEnginesHistory(cls):
        from maya import cmds

        history = cmds.listHistory(shadingEngine, pdo=True, gl=True)
        if shadingEngine in history:
            history.remove(shadingEngine)
        return history

    @classmethod
    def findSourceFile(cls, nodes, **kwargs):
        relativedirname = kwargs.get("relativedirname", None)
        relativepath = kwargs.get("relativepath", False)

        from maya import cmds

        sourcenodes = []
        for node in nodes:
            typed = cmds.nodeType(node)
            if typed not in cls.sourceFileNodes:
                continue
            attribute = "%s.%s" % (node, cls.sourceFileNodes[typed])
            if not cmds.objExists(attribute):
                continue
            source_file = cmds.getAttr(attribute)

            if relativedirname:
                source_file = cls.relativedirname(source_file, relativedirname)

            if relativepath and not relativedirname:
                source_file = cls.relatviePath(source_file)

            context = {
                "node": node,
                "path": source_file,
                "attribute": cls.sourceFileNodes[typed],
            }
            sourcenodes.append(context)
        return sourcenodes

    @classmethod
    def searchSourceFile(cls, relativepath=False):
        shadingEngines = cls.shadingEngines()
        nodes = list()
        for each in shadingEngines:
            history = cls.shadingEngineHistory(each)
            nodes.extend(history)
        sourcefile = cls.findSourceFile(nodes, relativepath=relativepath)
        return sourcefile

    @classmethod
    def relatviePath(cls, filepath):
        from maya import cmds

        dirname = os.path.dirname(cmds.file(q=1, sn=1))
        path = filepath.rsplit(dirname, 1)[-1]
        return path

    @classmethod
    def relativedirname(self, filepath, dirname):
        path = "%s/%s" % (dirname, os.path.basename(filepath))
        return path

    @classmethod
    def removeFilepath(cls, filepath):
        try:
            os.chmod(filepath, stat.S_IWRITE)
        except Exception as error:
            LOGGER.error(error)
        try:
            os.remove(filepath)
        except Exception as error:
            LOGGER.error(error)

    @classmethod
    def exportPuppetPose(cls, filepath, **kwargs):
        nodetype = kwargs.get("nodetype")
        pattern = kwargs.get("pattern")
        control = kwargs.get("control")
        readOnly = kwargs.get("readOnly", False)

        nodes = cls.getNodes(cls, **kwargs)
        context = cls.defaultPose(cls, nodes)

        filepath = cls.write(cls, filepath, context, readOnly=readOnly)
        return filepath

    def getNodes(self, **kwargs):
        mode = kwargs.get("mode")
        nodetype = kwargs.get("nodetype")
        pattern = kwargs.get("pattern")

        from maya import mel
        from maya import cmds

        nodes = list()
        if kwargs.get("mode") == "nodetype":
            nodes = mel.eval('listTransforms "-type %s";' % nodetype)
        if kwargs.get("mode") == "pattern":
            nodes = cmds.ls(pattern)

        return nodes

    def defaultPose(self, nodes):
        from maya import cmds

        controls = {}
        for node in nodes:
            attributes = cmds.listAttr(node, k=True, u=True, sn=True)
            if not attributes:
                continue
            values = {}
            for attribute in attributes:
                value = cmds.getAttr("%s.%s" % (node, attribute))
                values[attribute] = value
            controls[node] = values
        return controls

    def write(self, filepath, context, readOnly=False):
        with open(filepath, "w") as file:
            file.write(json.dumps(context, indent=4))
        if not readOnly:
            return filepath
        os.chmod(filepath, stat.S_IREAD)
        return filepath
    
    @classmethod
    def importFiles(cls, context, parent=None, typed="reference"):
        
        from maya import cmds
        
        
        for each in context:
            if not os.path.isfile(each["filepath"]):
                LOGGER.warning("could not find the source file, %s" % each["filepath"])
                continue
            parameters = {"namespace": each["name"]}
            if typed=="reference":
                parameters.update({"reference":True, "returnNewNodes":True})
            
            print ("\n")
            from pprint import pprint
            pprint (parameters)

            cls.importFile(each["filepath"], parent=parent, **parameters)
            
    @classmethod
    def updateFiles(cls, context, rootNode=None):
        from maya import cmds
        
        from pprint import pprint
        #print ("\nupdateFiles")
        #pprint (context)
        for each in context:
            
            if not each.node:
                continue
            
            if not each.isCheckState():
                # LOGGER.warning("%s, is un-checked", each.name)
                continue
                

            if not each.filepath:
                continue

            
            if not os.path.isfile(each.filepath):
                LOGGER.warning("could not find filepath %s" % each.filepath)
                continue

            currentFilepath = each.node.referencePath()
            referenceNode = each.node.referenceNode()

            if currentFilepath != each.filepath:
                nodes = cmds.file(each.filepath, loadReference=referenceNode, rnn=True)
                LOGGER.info("replace %s to %s" % (currentFilepath, each.filepath))
            else:
                nodes = each.node.referenceNodes()

            if rootNode:
                PipeNode.linkToParent(rootNode, nodes)


    @staticmethod
    def newScene():
        from maya import cmds
        cmds.file(new=True, force=True)
    
    @staticmethod
    def saveScene(filepath, **kwargs):
        timestamp = kwargs.get("timestamp", time.time())
        force = kwargs.get("force",  False)
        from maya import OpenMaya
        Create.directory(filepath, timestamp=timestamp, force=False)
        Create.removeFilepath(filepath)
        OpenMaya.MFileIO.saveAs(filepath, "mayaAscii", True)
        return True


    @classmethod
    def importFile(cls, filepath, parent=None, **kwargs):
        from maya import cmds
        # nodes = cmds.file (filepath, reference=True, namespace=namespace, returnNewNodes=True)
        nodes = cmds.file (filepath, **kwargs)
        
        if parent:
            PipeNode.linkToParent(parent, nodes)
            
        return nodes
            




