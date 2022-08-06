"""
Animation Build 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:May:18:Tuesday-05:55:27:PM
description": animation build
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Animation Build"
ORDER = 2
LAST_MODIFIED = "July 05, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Animation shot Build Tool"
SEPARATOR = True
LOCATION = "Animation/Animation Build"
ENABLE = True
ICON = "animation-build"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from animation import build

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    scene = build.Scene(
        parent=qwidget, step="animation", iconpath=iconpath
    )
    scene.show()
