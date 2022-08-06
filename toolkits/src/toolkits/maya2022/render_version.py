"""
Render Version Management 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:09:Friday-07:08:05:PM
description": render version management
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Render Version Management"
ORDER = 2
LAST_MODIFIED = "July 09, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Render Version Management Tool"
SEPARATOR = True
LOCATION = "Rendering/Render Version Management"
ENABLE = True
ICON = "version-management"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from rendering import version

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    scene = version.Render(
        parent=qwidget, step="render", iconpath=iconpath
    )
    scene.show()
