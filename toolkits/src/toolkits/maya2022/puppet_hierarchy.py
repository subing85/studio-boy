"""
Puppet Asset Node 0.0.1 
mail id: subing85@gmail.com
author": Subin. Gopi (subing85@gmail.com)
#copyright": (c) 2021, Studio-Pipe Los Angeles, CA and Wuhan, China All rights reserved.
lastModified": 022:June:08:Wednesday-11:08:31:PM
description": create puppet hierarchy
warning": #WARNING! All changes made in this file will be lost!
"""

NAME = "Create Hierarchy"
ORDER = 1
LAST_MODIFIED = "June 09, 2022"
OWNER = "Subin Gopi"
COMMENTS = "Studio-Pipe, create Puppet hierarchy"
SEPARATOR = True
LOCATION = "Puppet/Create Hierarchy"
ENABLE = True
ICON = "puppet-hierarchy"

import os
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


def execute():
    LOGGER.info(COMMENTS)

    from puppet.hierarchy import Asset

    node = Asset.create()
    LOGGER.info("root %s" % node)
