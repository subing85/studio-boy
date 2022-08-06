"""
Asset Hierarchy 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 2021:July:06:Tuesday-03:56:27:PM
description": create asset hierarchy
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Create Hierarchy"
ORDER = 2
LAST_MODIFIED = "July 06, 2021"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe Create basic asset hierarchy"
SEPARATOR = True
LOCATION = "Model/Create Hierarchy"
ENABLE = True
ICON = "asset-hierarchy"

import os
from pipe.core import logger
from toolkits import resources

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    from modeling.hierarchy import Asset

    node, lods = Asset.create()

    LOGGER.info("root %s" % node)
    LOGGER.info("lods %s" % lods)
