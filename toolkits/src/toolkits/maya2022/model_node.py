"""
Model Asset Node 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 022:June:08:Wednesday-11:08:31:PM
description": model asset node
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Model Asset Node"
ORDER = 1
LAST_MODIFIED = "June 08, 2022"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe, create asset model node"
SEPARATOR = True
LOCATION = "Model/Model Node"
ENABLE = True
ICON = "model-node"

import os
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    from modeling.hierarchy import Asset

    node = Asset.createNode()
