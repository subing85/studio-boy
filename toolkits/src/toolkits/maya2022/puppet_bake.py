"""
Puppet Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:May:18:Tuesday-05:55:27:PM
description": puppet bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Puppet Bake"
ORDER = 4
LAST_MODIFIED = "June 24, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Puppet bake Tool for extract the publish components such as look-image, turnaround-mov, maya scene, etc"
SEPARATOR = True
LOCATION = "Puppet/Puppet Bake"
ENABLE = True
ICON = "puppet-bake"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from puppet import bake

    import importlib

    importlib.reload(bake)

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    window = bake.Puppet(
        parent=qwidget,
        wsize=[400, 310],
    )
    window.show()
