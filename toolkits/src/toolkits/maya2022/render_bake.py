"""
Render Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:11:Sunday-11:51:32:PM
description": render bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Render Bake"
ORDER = 3
LAST_MODIFIED = "July 11, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Render Tool for extract the publish components such as maya scene, cache and casting-sheet"
SEPARATOR = True
LOCATION = "Rendering/Render Bake"
ENABLE = True
ICON = "render-bake"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from rendering import bake

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    layout = bake.Render(
        parent=qwidget, step="render", iconpath=iconpath
    )
    layout.show()
