"""
Layout Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:07:Wednesday-05:30:35:PM
description": layout bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Animation Bake"
ORDER = 4
LAST_MODIFIED = "July 07, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Animation Tool for extract the publish components such as preview-mov, maya scene, cache and casting-sheet"
SEPARATOR = True
LOCATION = "Animation/Animation Bake"
ENABLE = True
ICON = "animation-bake"

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
        parent=qwidget, step="animation", iconpath=iconpath
    )
    layout.show()
