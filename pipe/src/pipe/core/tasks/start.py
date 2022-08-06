# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:45:33:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks start.

import time

from pipe import resources
from pipe.core import logger
from pipe.core.tasks import setStatus

LOGGER = logger.getLogger(__name__)
TASKS_OBJECT = None


def execute(task, user, timestamp=None):
    timestamp = timestamp or time.time()
    if not TASKS_OBJECT:
        message = "not found value in <TASKS_OBJECT> env variable"
        LOGGER.warning(message)
        return None, message
    setStatus.CORE_OBJECT = TASKS_OBJECT
    metadata = {
        "start-by": user["email"],
        "start-at": resources.getTimeToDatetime(timestamp),
    }
    task = setStatus.execute(task, "In progress", metadata=metadata)
    return task, None


if __name__ == "__main__":
    pass
