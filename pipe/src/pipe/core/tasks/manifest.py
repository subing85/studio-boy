# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-03:40:53:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core tasks manifest.

import os
import stat
import time
import json

from pipe.core import logger

LOGGER = logger.getLogger(__name__)
MANIFEST_NAME = "manifest"


def create(entity, path, **kwargs):
    comment = kwargs.get("comment", None)
    metadata = kwargs.get("metadata", None)
    timestamp = kwargs.get("timestamp", time.time())

    if entity.entity_type == "Version":
        version = entity
        task = entity.get("task")
    
    if entity.entity_type == "Task":
        version = dict()
        task = entity

    #===============================================================================================
    # start_date = None
    # if task.get("start_date"):
    #     start_date = task["start_date"].format(
    #         "YYYY-MM-DD HH:mm:ss"
    #     )
    #===============================================================================================

    data = {
        "Task": dict(),
        "AssetVersion": dict(),
        "metadata": metadata,
        "Dependency": None
        }
    
    if task:
        assignments = [each["resource"]["username"] for each in task["assignments"]]
        data["Task"] = {
            "project": task["link"][0],
            "category": task["link"][1]["name"],
            "entity": task["link"][-2],
            "name": task["type"]["name"],
            "id": task["id"],
            "description": task["description"],
            "assignments": assignments
        }
    
    if version:
        data["AssetVersion"] = {
            "id": version["id"],
            "asset-name": version["asset"]["name"],
            "asset-id": version["asset"]["id"],
            "asset-type-name": version["asset"]["type"]["name"],
            "asset-type-id": version["asset"]["type"]["id"],
            "comment": comment,
        }

    filepath = "%s/%s.json" % (path, MANIFEST_NAME)
    if not os.path.isdir(path):
        os.makedirs(path)
        os.utime(path, (timestamp, timestamp))
    filepath = "%s/%s.json" % (path, MANIFEST_NAME)
    if os.path.isfile(filepath):
        os.chmod(filepath, stat.S_IWRITE)
    with open(filepath, "w") as fwrite:
        fwrite.write(json.dumps(data, indent=4))
        os.utime(filepath, (timestamp, timestamp))
        os.chmod(filepath, stat.S_IREAD)
        result = {
            "code": "json",
            "display-name": "Manifest",
            "file": filepath,
            "format": ".json",
            "name": "manifest",
            "type": "path",
            "valid": True,
            "filename": "manifest",
        }
        return result
    return None


def update(version, path, **kwargs):
    metadata = kwargs.get("metadata", None)
    timestamp = kwargs.get("timestamp", time.time())
    filepath = os.path.join(path, "%s.json" % MANIFEST_NAME)

    if not os.path.isfile(filepath):
        print("\n")
        LOGGER.error("not able to find current version manifest")
        return
    os.chmod(filepath, stat.S_IWRITE)
    data = dict()
    with open(filepath, "r") as fread:
        data = json.load(fread)
        data["metadata"].update(metadata)

    data["AssetVersion"] = {
        "id": version["id"],
        "asset-name": version["asset"]["name"],
        "asset-id": version["asset"]["id"],
        "asset-type-name": version["asset"]["type"]["name"],
        "asset-type-id": version["asset"]["type"]["id"],
        "comment": version["comment"],
    }
    with open(filepath, "w") as fwrite:
        fwrite.write(json.dumps(data, indent=4))
        os.utime(filepath, (timestamp, timestamp))
        os.chmod(filepath, stat.S_IREAD)


if __name__ == "__main__":
    pass
