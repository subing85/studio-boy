# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:44:55:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks set status.

import arrow
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

CORE_OBJECT = None


def execute(context, next_staus, metadata=None):
    if not CORE_OBJECT:
        message = "not found value in <TASKS_OBJECT> env variable"
        LOGGER.warning(message)
        return None
    statuses = CORE_OBJECT.findStatus()
    if next_staus not in statuses:
        LOGGER.error(
            "<%s> status not found in the status entity" % next_staus
        )
        return False
    if context.get("start_date"):
        context["start_date"] = arrow.utcnow().floor("day")
    context["status"] = statuses[next_staus]
    if metadata:
        context["metadata"] = metadata
    CORE_OBJECT.session.commit()
    LOGGER.info(
        "task <%s> change the status into %s"
        % (context["id"], next_staus)
    )
    return context


def getStatus():
    status = [
        "Not started",
        "In progress",
        "Pending Review",
        "Approved",
        "Revise",
        "Completed",
    ]
    return status


if __name__ == "__main__":
    pass
