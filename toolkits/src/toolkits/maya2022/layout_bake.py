"""
Layout Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:May:18:Tuesday-05:55:27:PM
description": layout bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Layout Bake"
ORDER = 2
LAST_MODIFIED = "June 24, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Layout Tool for extract the publish components such as preview-mov, maya scene, animation, cache and casting-sheet"
SEPARATOR = True
LOCATION = "Layout/Layout Bake"
ENABLE = True
ICON = "layout-bake"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from animation import bake

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    layout = bake.Animation(
        parent=qwidget, iconpath=iconpath
    )
    layout.show()
