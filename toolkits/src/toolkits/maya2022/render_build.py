"""
Animation Build 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:07:Wednesday-10:15:01:PM
description": render shot build
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Render Build"
ORDER = 1
LAST_MODIFIED = "July 07, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Render shot Build Tool"
SEPARATOR = True
LOCATION = "Rendering/Render Build"
ENABLE = True
ICON = "render-build"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from rendering import build

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    scene = build.Render(
        parent=qwidget, step="render", iconpath=iconpath
    )
    scene.show()
