"""
Layout Build 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:May:18:Tuesday-05:55:27:PM
description": layout build
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Layout Build"
ORDER = 1
LAST_MODIFIED = "June 15, 2022"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Layout Tool for scene build and version management."
SEPARATOR = True
LOCATION = "Layout/Layout Build"
ENABLE = True
ICON = "layout-build"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)



def execute():
    LOGGER.info(COMMENTS)
    
    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from layout import build

    import importlib
    importlib.reload(build)
    
    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    layout = build.Layout(
        parent=qwidget, iconpath=iconpath
    )
    layout.show()
