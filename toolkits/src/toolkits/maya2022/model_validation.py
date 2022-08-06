"""
Model Validation 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:22:Thursday-06:20:21:PM
description": model validation tool
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Model Validation"
ORDER = 3
LAST_MODIFIED = "July 22, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe model validation tool"
SEPARATOR = True
LOCATION = "Model/Model Validation"
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

    from modeling import validate

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    window = validate.Modeling(
        parent=qwidget,
        wsize=[500, 340],
    )
    window.show()
