"""
Model Bake 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:May:18:Tuesday-05:55:27:PM
description": model bake
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Model Bake"
ORDER = 4
LAST_MODIFIED = "May 18, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Model bake Tool for extract the publish components such as look-image, turnaround-mov and uv-json"
SEPARATOR = True
LOCATION = "Model/Model Bake"
ENABLE = True
ICON = "model-bake"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    import shiboken2
    from maya import OpenMayaUI
    from PySide2 import QtWidgets

    from modeling import bake

    import importlib

    importlib.reload(bake)

    swig = int(OpenMayaUI.MQtUtil.mainWindow())
    qwidget = shiboken2.wrapInstance(swig, QtWidgets.QWidget)

    window = bake.Modeling(
        parent=qwidget,
        wsize=[400, 235],
    )
    window.show()
