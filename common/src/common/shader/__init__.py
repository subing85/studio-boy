from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class SearchShaders(object):
    @classmethod
    def doIt(cls):
        from maya import cmds

        default_shaders = cmds.ls(defaultNodes=True, materials=True)
        shaders = cmds.ls(materials=True)
        context = []
        for shader in shaders:
            if shader in default_shaders:
                continue
            context.append(shader)
        return context


class SetDefultShader(object):
    @classmethod
    def doIt(cls, geometries):
        from maya import mel
        from maya import cmds

        cmds.undoInfo(openChunk=True)
        if not geometries:
            geometries = set(mel.eval('listTransforms "-type mesh"'))

        result = []
        try:
            cmds.sets(
                geometries, e=True, forceElement="initialShadingGroup"
            )
            valid = True
            result.append("set the default shader to the geometries")
        except Exception as error:
            valid = False
            result.append(str(error))
            LOGGER.warning(result)

        if not valid:
            return valid

        try:
            mel.eval("MLdeleteUnused;")
            valid = True
            result.append("delete the unused nodes")
        except Exception as error:
            valid = False
            result.append(str(error))
            LOGGER.warning(result)

        cmds.undoInfo(closeChunk=True)
        return valid, result
