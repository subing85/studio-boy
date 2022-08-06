import os
from toolkits import core
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def doIt():
    from maya import mel
    from maya import cmds
        
    # set the project
    project_path = os.getenv("PROJECT-PATH")

    if project_path:
        if not os.path.isdir(project_path):
            try:
                os.makedirs(project_path)
            except Exception as error:
                LOGGER.error(error)
        cmds.workspace(project_path, openWorkspace=True)
    else:
        LOGGER.warning("could not find PROJECT-PATH")

    workspace = cmds.workspace(q=True, fn=True)
    print("\n")
    LOGGER.info("Current workspace: %s" % workspace)

    mel.eval('setNamedPanelLayout "Single Perspective View";')

    # set the unit
    cmds.upAxis(ax="y")
    cmds.currentUnit(linear="centimeter")
    cmds.currentUnit(time="ntsc")
    cmds.currentUnit(angle="degree")
    LOGGER.info("Set Maya units")

    cmds.playbackOptions(e=True, min=1)
    cmds.playbackOptions(e=True, ast=1)
    cmds.playbackOptions(e=True, max=90)
    cmds.playbackOptions(e=True, aet=90)
    cmds.currentTime(1)
    LOGGER.info("Set Maya playback frames")

    cmds.optionVar(fv=("defaultCameraNearClipValue", 1))
    cmds.optionVar(fv=("defaultCameraFarClipValue", 1000000))
    LOGGER.info("Set Camera Near and Far Clip")

    cmds.playbackOptions(v="all")
    cmds.playbackOptions(loop="continuous")
    cmds.playbackOptions(ps=0)

    LOGGER.info("Set playback to real time")

    cmds.undoInfo(state=True)
    cmds.undoInfo(infinity=True)

    LOGGER.info("Set maya undo to infinity")

    plugins = [
        "AbcExport",
        "AbcImport",
        "OpenEXRLoader",
        "animImportExport",
        "atomImportExport",
        # 'gpuCache',
        "xgenToolkit",
        "pipeNodes",
    ]
    for plugin in plugins:
        try:
            cmds.loadPlugin(plugin)
            LOGGER.info("success, plug-in loaded %s" % plugin)
        except Exception as error:
            LOGGER.warning(str(error))

    print("\n")

    mayamenu = core.MayaMenu()
    mayamenu.create()

    LOGGER.info("success, Studio-Pipe ToolKit Setup")
    LOGGER.info("success, setup Studio-Pipe maya default settings")

