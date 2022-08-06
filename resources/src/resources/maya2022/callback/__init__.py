from maya import OpenMaya
from pipe.core import logger
from resources.maya2022.callback import save

LOGGER = logger.getLogger(__name__)


def beforeNew(*args):
    return


def afterNew(*args):
    return


def beforeOpen(*args):
    return


def afterOpen(*args):
    return


def beforeSave(*args):
    LOGGER.info("callback, before save")
    save.After.doIt()
    LOGGER.info("callback, succeed.")
    return

def afterSave(*args):
    LOGGER.info("callback, afetre Save")
    save.After.doIt()
    LOGGER.info("callback, succeed.")
    return


def beforeImport(*args):
    return


def afterImport(*args):
    return


def beforeReference(*args):
    return


def afterReference(*args):
    return


def doIt():
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeNew, beforeNew)
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, afterNew)

    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeOpen, beforeOpen)
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, afterOpen)

    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeSave, beforeSave)
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterSave, afterSave)

    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeImport, beforeImport)
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterImport, afterImport)

    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeReference, beforeReference)
    OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterReference, afterReference)
