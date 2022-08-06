# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:48:10:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks start.

import time

from pipe import resources
from pipe.core import kinds
from pipe.core import logger
from pipe.core import versions
from pipe.core import components
from pipe.core.tasks import setStatus

LOGGER = logger.getLogger(__name__)
TASKS_OBJECT = None
KIND = "submit"

KINDS = kinds.Connect()
VERSN = versions.Connect()
COMPT = components.Connect()


from pprint import pprint


def execute(task, **kwargs):
    userid = kwargs.get("userid")
    path = kwargs.get("path")
    version = kwargs.get("version")
    components = kwargs.get("components")
    comment = kwargs.get("comment")

    if not TASKS_OBJECT:
        message = "not found value in <TASKS_OBJECT> env variable"
        LOGGER.warning(message)
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
    #     task, "Completed"
    # )
    # ===============================================================================================

    dependencies = TASKS_OBJECT.hasDependencyTasksStatus(task, "Done")
    if not dependencies:
        message = "dependency tasks are not yet Completed"
        LOGGER.error(message)
        return None, None, message
    if version in VERSN.semantic:
        version_index = VERSN.semantic.index(version)
    else:
        message = 'invalid semantic verion name "%s"' % version
        LOGGER.warning(message)
        return None, None, message

    if not components:
        components = COMPT.collectFromDirectory(
            task, path=path, verbose=False
        )

    component_file = list(
        filter(lambda k: not k.get("file"), components)
    )
    if component_file:
        print("\n")
        LOGGER.error("not able to collect all components")
        for each in component_file:
            LOGGER.error('component "%s" file is None' % each["name"])
        return None, None, message
    current_user = TASKS_OBJECT.searchUserContext(userid)
    asset_version = process(
        task, current_user, version_index, components, comment
    )
    return task, asset_version, None


def process(task, user, index, components, comment):
    next_status = KINDS.findKindStatus(KIND)
    timestamp = time.time()
    header = TASKS_OBJECT.contextHeader(task)
    LOGGER.info("trigger the <%s -task> process" % KIND)
    VERSN.authorization()
    next_version_path, next_version = VERSN.nextVersionPath(
        KIND, task=task, index=index
    )
    # 1.create submit file in the project directory
    print("\n")
    LOGGER.info(
        "%s-task stage 1 - create files in submit folder" % KIND
    )
    try:
        components = VERSN.copyCat(
            next_version_path, components, timestamp
        )
        message = "success, %s-task, (create file) <%s>" % (
            KIND,
            header,
        )
        valid = True
        LOGGER.info(message)
    except Exception as error:
        message = "failed %s-task, (create file)%s" % (KIND, header)
        valid = False
        LOGGER.error(error)

    if not valid:
        LOGGER.warning("submit task process is broken %s" % message)
        return None

    metadata = {
        "kind": KIND,
        "version": next_version,
        "status": next_status,
        "status-by": user["email"],
        "status-at": resources.getDateTimes(),
        "released-by": user["email"],
        "released-at": resources.getDateTimes(),
        "dependency": None,
        "comment": comment,
    }

    # 3. create submit asset version
    print("\n")
    LOGGER.info("%s-task stage 2 - create submit version" % KIND)
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
        valid = False
        message = "failed %s-task, (created version)%s" % (
            KIND,
            header,
        )
        LOGGER.error(error)
    if not valid:
        LOGGER.warning("submit task process is broken %s" % message)
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
