"""
Lookdev Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:01:Tuesday-05:55:27:PM
description": lookdev bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Lookdev Bake"
ORDER = 3
LAST_MODIFIED = "July 01, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Lookdev bake Tool for extract the publish components such as look-image, turnaround-mov, shader and maya scene"
SEPARATOR = True
LOCATION = "Lookdev/Lookdev Bake"
ENABLE = True
ICON = "lookdev-bake"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from lookdev import bake

    import importlib

    importlib.reload(bake)

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    window = bake.Lookdev(
        parent=qwidget,
        wsize=[400, 265],
    )
    window.show()
