# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:33:41:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core version download.

import time
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

VERSN_OBJECT = None


def execute(**kwargs):
    versions = kwargs.get("versions", None)

    if not VERSN_OBJECT:
        message = "not found value in <VERSN_OBJECT> env variable"
        LOGGER.warning(message)
        return None, None
    contexts = []
    if versions:
        for each in versions:
            context = {
                "version": each,
                "path": None,
                "kind": None,
                "timestamp": kwargs.get("timestamp", time.time()),
                "progressbar": kwargs.get("progressbar"),
            }
            contexts.append(context)
    else:
        # only for publish, take submit version and deploy to publish version
        # if the value of kwargs path None, deploy the components based on
        # the AssetVersion kind type ('submit' or 'publish')
        if not kwargs.get("version"):
            LOGGER.warning('argument "version" should be declare')
            return
        if not kwargs.get("kind"):
            LOGGER.warning('argument "kind" should be declare')
            return
        context = {
            "version": kwargs["version"],
            "path": kwargs.get("path", None),
            "kind": kwargs["kind"],
            "timestamp": kwargs.get("timestamp", time.time()),
            "progressbar": kwargs.get("progressbar"),
        }
        contexts.append(context)

    print("contexts", contexts)
    components = deployVersionComponents(contexts)
    return components


def deployVersionComponents(contexts):
    components = []
    for each in contexts:
        if each.get("path"):
            version_path = each["path"]
        else:
            version_path, current_version = VERSN_OBJECT.versionPath(
                each["version"], kind=each["kind"]
            )

        version_components = VERSN_OBJECT.downloadVersion(
            each["version"],
            version_path,
            timestamp=each["timestamp"],
            progressbar=each.get("progressbar"),
        )
        if not version_components:
            continue
        version_component = {
            "AssetVersion": each["version"],
            "components": version_components,
        }
        components.append(version_component)
        valid, message = (
            True,
            "success, deploy the version components in publish",
        )
        LOGGER.info(message)
    return components


if __name__ == "__main__":

    from pipe.core import versions

    import os

    os.environ["PROJECT-ID"] = "57cfc315-c96d-4031-89f6-110ad66c0cbd"
    os.environ["PROJECT-PATH"] = "Z:/projects/RAR"

    con = versions.Connect()
    con.authorization()

    version = con.update(
        "AssetVersion", "85c8109f-98d1-4367-9748-011e1a1bacef"
    )

    print(version)

    VERSN_OBJECT = con

    execute(version=version, kind="submit")
