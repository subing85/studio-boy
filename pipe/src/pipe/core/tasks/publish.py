# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:44:20:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks publish.

import time

from pipe import resources
from pipe.core import kinds
from pipe.core import logger
from pipe.core import versions
from pipe.core.tasks import setStatus
from pipe.core.versions import download


LOGGER = logger.getLogger(__name__)
TASKS_OBJECT = None
KIND = "publish"

KINDS = kinds.Connect()
VERSN = versions.Connect()


def execute(task, **kwargs):
    userid = kwargs.get("userid")
    version = kwargs.get("version")
    comment = kwargs.get("comment")

    if not TASKS_OBJECT:
        message = "not found value in <TASKS_OBJECT> env variable"
        LOGGER.warning(message)
        return None, None, message
    super_user = TASKS_OBJECT.hasSuperUser(userid)
    current_user = TASKS_OBJECT.usercontext
    if not super_user and KIND == "publish":
        message = (
            "permission denied current user <%s>"
            % current_user["email"]
        )
        LOGGER.error(message)
        return None, None, message
    current_status = TASKS_OBJECT.currentStatus(task)
    dependency_status = KINDS.findKindDependencyStatus(KIND)
    if current_status["name"] not in dependency_status:
        message = "not able to release %s task, because current task status is <%s>" % (
            KIND,
            current_status["name"],
        )
        LOGGER.warning(message)
        return None, None, message
    # ===============================================================================================
    # dependencies = TASKS_OBJECT.hasDependencyTasksStatus(
    #     task, "Approved"
    # )
    # ===============================================================================================

    dependencies = TASKS_OBJECT.hasDependencyTasksStatus(task, "Done")

    if not dependencies:
        message = "dependency tasks are not yet Approved"
        LOGGER.error(message)
        return None, None, message
    if version in VERSN.semantic:
        version_index = VERSN.semantic.index(version)
    else:
        message = 'invalid semantic verion name "%s"' % version
        LOGGER.warning(message)
        return None, None, message
    asset_version = process(
        task, current_user, version_index, comment
    )
    return task, asset_version, None


def process(task, user, index, comment):
    next_status = KINDS.findKindStatus(KIND)
    timestamp = time.time()
    header = TASKS_OBJECT.contextHeader(task)
    LOGGER.info("trigger the <%s -task> process" % KIND)
    VERSN.authorization()

    # find latest approved submit version
    print("\n")
    LOGGER.info(
        "%s-task stage 1 - find latest approved submit version" % KIND
    )
    latest_submit_version = VERSN.getLatestValidVerion(
        "submit", "Approved", task=task
    )
    if not latest_submit_version:
        LOGGER.warning(
            "not able to find latest approved submit version "
        )
        return None
    version_header = TASKS_OBJECT.contextHeader(latest_submit_version)
    LOGGER.info(
        "latest approved version ID, <%s>"
        % latest_submit_version["id"]
    )
    LOGGER.info(
        "latest approved task version header  <%s>" % version_header
    )

    # 1.Download file from submit version and deploy to local project
    print("\n")
    LOGGER.info(
        "%s-task stage 2 - Download and deploy file from latest approved submit version"
        % KIND
    )
    next_version_path, next_version = VERSN.nextVersionPath(
        KIND, task=task, index=index
    )
    download.VERSN_OBJECT = VERSN

    try:
        reloyed_contexts = download.execute(
            version=latest_submit_version,
            path=next_version_path,
            kind=KIND,
            timestamp=timestamp,
        )
        message = "success, %s-task, (deploy file) <%s>" % (
            KIND,
            header,
        )
        valid = True
        LOGGER.info(message)
    except Exception as error:
        message = "failed %s-task, (deploy file)%s" % (KIND, header)
        valid = False
        LOGGER.error("%s, %s" % (message, error))
        return None

    components = reloyed_contexts[0].get("components")
    if not valid:
        LOGGER.warning("publish task process is broken %s" % message)
        return None
    metadata = {
        "kind": KIND,
        "version": next_version,
        "status": next_status,
        "status-by": user["email"],
        "status-at": resources.getDateTimes(),
        "released-by": user["email"],
        "released-at": resources.getDateTimes(),
        "comment": comment,
    }
    metadata["dependency"] = {
        "id": latest_submit_version["id"],
        "version": latest_submit_version["metadata"].get("version"),
        "status": latest_submit_version["metadata"].get("status"),
        "status-by": latest_submit_version["metadata"].get(
            "status-by"
        ),
        "status-at": latest_submit_version["metadata"].get(
            "status-data"
        ),
    }

    # 3. create submit asset version
    print("\n")
    LOGGER.info("%s-task stage 2 - create publish version" % KIND)
    arguments = [
        task,
        user,
        components,
        next_status,
        next_version_path,
    ]
    try:
        asset_version = VERSN.createNewVersion(
            *arguments,
            comment=comment,
            metadata=metadata,
            timestamp=timestamp
        )
        message = "success, %s-task, (created version) <%s>" % (
            KIND,
            header,
        )
        valid = True
        LOGGER.info(message)
    except Exception as error:
        valid = (False,)
        message = "failed %s-task, (created version)%s" % (
            KIND,
            header,
        )
        LOGGER.error(error)
    if not valid:
        LOGGER.warning("publish task process is broken %s" % message)
        return None

    # 4. update task status
    print("\n")
    LOGGER.info("%s-task stage 3 - update task status" % KIND)
    setStatus.CORE_OBJECT = TASKS_OBJECT
    status_result = setStatus.execute(task, next_status)

    # update asset version status
    LOGGER.info("%s-task (Task), %s" % (KIND, header))
    LOGGER.info("%s-task (Task) ID, %s" % (KIND, task["id"]))
    LOGGER.info(
        "%s AssetVersion ID, %s" % (KIND, asset_version["id"])
    )
    LOGGER.info("%s Asset ID, %s" % (KIND, asset_version["asset_id"]))
    LOGGER.info("%s-task new version, %s" % (KIND, next_version))
    LOGGER.info("%s local task path, %s" % (KIND, next_version_path))
    LOGGER.info("completed the <%s-task> process" % KIND)
    return asset_version


if __name__ == "__main__":
    pass
