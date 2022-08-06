# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:35:49:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks approved.

import time

from pipe import resources
from pipe.core import logger
from pipe.core.tasks import manifest
from pipe.core.tasks import setStatus

LOGGER = logger.getLogger(__name__)
TASKS_OBJECT = None
VERSN_OBJECT = None


def execute(task, version, user, timestamp=None):
    timestamp = timestamp or time.time()
    if not TASKS_OBJECT:
        message = "not found value in <TASKS_OBJECT> env variable"
        LOGGER.warning(message)
        return None, None
    if not VERSN_OBJECT:
        message = "not found value in <VERSN_OBJECT> env variable"
        LOGGER.warning(message)
        return None, None
    current_status = TASKS_OBJECT.currentStatus(task)
    if current_status["name"] != "Pending Review":
        message = (
            "not able to decline submission task, because current task status is <%s>"
            % (current_status["name"])
        )
        LOGGER.warning(message)
        return None, None
    VERSN_OBJECT.authorization()
    asset_version = VERSN_OBJECT.searchKindVersion(
        "submit", task=task, versions=version
    )
    metadata = asset_version.get("metadata")
    metadata["status"] = "Approved"
    metadata["status-by"] = user["email"]
    metadata["status-at"] = resources.getTimeToDatetime(timestamp)
    setStatus.CORE_OBJECT = TASKS_OBJECT
    task = setStatus.execute(task, "Approved")
    setStatus.CORE_OBJECT = VERSN_OBJECT
    asset_version = setStatus.execute(asset_version, "Approved")
    version_path, current_version = VERSN_OBJECT.versionPath(
        asset_version, kind="submit"
    )
    manifest.update(
        asset_version,
        version_path,
        metadata=metadata,
        timestamp=timestamp,
    )
    return task, asset_version, None


if __name__ == "__main__":
    pass
