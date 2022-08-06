"""
Lookdev Validation 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:23:Friday-04:11:51:PM
description": lookdev validation tool
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Lookdev Validation"
ORDER = 2
LAST_MODIFIED = "July 23, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe lookdev validation tool"
SEPARATOR = True
LOCATION = "Lookdev/Lookdev Validation"
ENABLE = True
ICON = "validate"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from lookdev import validate

    import importlib

    importlib.reload(validate)

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    window = validate.Lookdev(
        parent=qwidget,
        wsize=[500, 340],
        iconpath=iconpath,
    )
    window.show()
