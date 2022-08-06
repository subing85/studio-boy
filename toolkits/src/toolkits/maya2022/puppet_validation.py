"""
Puppet Validation 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:23:Friday-06:12:53:PM
description": puppet validation tool
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Puppet Validation"
ORDER = 3
LAST_MODIFIED = "July 23, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe puppet validation tool"
SEPARATOR = True
LOCATION = "Puppet/Puppet Validation"
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

    from puppet import validate

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    iconpath = os.path.join(resources.getIconPath(), "%s.png" % ICON)
    window = validate.Puppet(
        parent=qwidget,
        step="puppet",
        wsize=[500, 340],
        iconpath=iconpath,
    )
    window.show()
