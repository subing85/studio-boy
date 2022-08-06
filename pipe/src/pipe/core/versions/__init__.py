# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:11:25:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core versions.

import os
import stat
import copy
import time
import shutil
import requests
import distutils

from pipe import utils
from pipe.core import kinds
from pipe.core import logger
from pipe.core import ftrack
from pipe.core import components
from pipe.core.tasks import manifest
from pipe.core.versions import download

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Connect(ftrack.Connect):
    entity = "AssetVersion"

    def __init__(self, entity=entity, **kwargs):
        super(Connect, self).__init__(entity, **kwargs)

        self.task = kwargs.get("task") or dict()
        self.start_version = "0.0.1"
        self.comp = components.Connect()

    @property
    def semantic(self):
        versions = ["major", "minor", "patch"]
        return versions

    def currentStep(self, taskid):
        context = self.session.get("Task", taskid)
        return context

    def currentVersion(self, id):
        context = self.find(id)
        return context

    def projectPathEnv(self):
        self.inpt.config = "project"
        env = self.inpt.findEnvValue("path")
        return env

    @property
    def projectid(self):
        self.inpt.config = "project"
        env_key = self.inpt.findEnvValue("id")
        return os.getenv(env_key)

    def projectPath(self):
        env = self.projectPathEnv()
        path = utils.setPathResolver(os.getenv(env))
        return path

    def categoryPath(self, task=None):
        task = task or self.task
        path = utils.setPathResolver(
            self.projectPath(), folders=[task["link"][1]["name"]]
        )
        return path

    def entityPath(self, task=None):
        task = task or self.task
        link_name = [each["name"] for each in task["link"][2:-1]]
        path = utils.setPathResolver(
            self.categoryPath(task=task), folders=link_name
        )
        return path

    def taskPath(self, task=None):
        task = task or self.task
        path = utils.setPathResolver(
            self.entityPath(task=task), folders=[task["type"]["name"]]
        )
        return path

    def kindPath(self, kind, task=None):
        knds = kinds.Connect()
        display_name = knds.findKindName(kind)
        if not display_name:
            LOGGER.warning('invalid kind name called "%s"' % kind)
            return
        task = task or self.task
        path = utils.setPathResolver(
            self.taskPath(task=task), folders=[display_name]
        )
        return path

    def latestVersionPath(self, kind, task=None):
        task = task or self.task
        latest_version = self.latestVersion(kind, task=task)
        if not latest_version:
            return
        index_list = latest_version.split(".")
        if len(index_list) != 3:
            LOGGER.warning("invalid version formatting")
            return
        kind_path = self.kindPath(kind, task=task)
        if not kind_path:
            return
        path = utils.setPathResolver(
            kind_path, folders=[latest_version]
        )
        return path, latest_version

    def metadata(self):
        self.inpt.config = "metadata"
        contexts = self.inpt.get()
        return contexts

    def submitMetadata(self, task, **kwargs):
        contexts = self.metadata()
        metadata = {}
        for key, value in kwargs.items():
            contents = list(
                filter(lambda k: k["name"] == key, contexts)
            )
            if not contents:
                continue
            metadata[key] = value
        return metadata

    def findLatestVersionMetadata(self, context):
        metadata = context.get("metadata")
        return metadata

    def findValueFromMetadata(self, context, key):
        if not context:
            return None
        metadata = context.get("metadata")
        if not metadata:
            return None
        if not metadata.get(key):
            return None
        return metadata[key]

    def findKindFromAssetVersion(self, context):
        value = self.findValueFromMetadata(context, "kind")
        return value

    def findVersionFromAssetVersion(self, context):
        value = self.findValueFromMetadata(context, "version")
        return value

    def versionPath(self, asset_version, kind=None):
        kind = kind or self.findKindFromAssetVersion(asset_version)
        header = self.contextHeader(asset_version)
        LOGGER.info("version header, %s" % header)
        if not kind:
            LOGGER.warning(
                "invalid version metadata in %s" % asset_version["id"]
            )
            return
        kind_path = self.kindPath(kind, task=asset_version["task"])
        if not kind_path:
            return
        current_version = self.findVersionFromAssetVersion(
            asset_version
        )
        path = utils.setPathResolver(
            kind_path, folders=[current_version]
        )
        return path, current_version

    def nextVersionPath(self, kind, task=None, index=2):
        task = task or self.task
        kind_path = self.kindPath(kind, task=task)
        if not kind_path:
            return
        next_version = self.nextVersion(kind, task=task, index=index)
        path = utils.setPathResolver(
            kind_path, folders=[next_version]
        )
        return path, next_version

    def getLocalPath(self, context):
        dirname = self.projectPath()
        link_name = [each["name"] for each in context["link"][1:]]
        path = utils.setPathResolver(dirname, folders=link_name)
        return path

    def getKindPath(self, parent, kind):
        parent_path = self.getLocalPath(parent)
        path = utils.setPathResolver(parent_path, folders=[kind])
        return path

    def latestVersion(self, kind, task=None):
        task = task or self.task
        current_version = self.findLatestVersion(kind, task=task)
        if not current_version:
            return
        latest_version = current_version["metadata"].get("version")
        return latest_version

    def nextVersion(self, kind, task=None, index=2):
        task = task or self.task
        latest_version = self.findLatestVersion(kind, task=task)
        if not latest_version:
            return self.start_version
        current_version = latest_version["metadata"].get("version")
        next_version = self.getNextVersion(current_version, index)
        return next_version

    def findLatestVersion(self, kind, task=None):
        task = task or self.task
        versions = self.searchKindVersions(
            kind=kind, taskid=task["id"]
        )
        if not versions:
            LOGGER.warning(
                "not found any versions in <%s>, <%s>"
                % (kind, task.get("id"))
            )
            return None
        return versions[0]

    def getLatestValidVerion(self, kind, status, task=None):
        task = task or self.task
        latest_version = self.findLatestVersion(kind, task=task)
        current_status = task["status"]["name"]
        if current_status != status:
            LOGGER.warning(
                "version, not yet %s the task <%s>"
                % (status, task["id"])
            )
            return
        metadata_stage = self.findValueFromMetadata(
            latest_version, "status"
        )
        if metadata_stage != status:
            LOGGER.warning(
                "metadata, not yet %s the task <%s>"
                % (status, task["id"])
            )
            return
        return latest_version

    def searchKindVersion(self, kind, task=None, versions=None):
        task = task or self.task
        if not versions:
            current_version = self.findLatestVersion(kind, task=task)
            return current_version
        taskid = task["id"] if not isinstance(task, str) else task
        filter = "AssetVersion where %s and %s and %s" % (
            "task.id = %s" % taskid,
            'metadata any (key="kind" and value="%s")' % kind,
            'metadata any (key="version" and value="%s")' % versions,
        )
        asset_versions = self.search(filter=filter)
        if not asset_versions:
            return None
        return asset_versions.first()

    def searchKindVersions(self, **kwargs):
        projectid = kwargs.get("projectid", False)
        categoryid = kwargs.get("categoryid", None)
        stepid = kwargs.get("stepid", None)
        taskid = kwargs.get("taskid", None)
        kind = kwargs.get("kind", None)
        versions = kwargs.get("versions", None)

        filters = ["AssetVersion where"]
        if projectid:
            filters.append('task.project.id="%s"' % self.projectid)
        if categoryid:
            filters.append('task.parent.parent.id="%s"' % categoryid)
        if stepid:
            filters.append('asset.context_id="%s"' % stepid)
        if taskid:
            filters.append("%s" % ('task.id="%s"' % taskid))
        if kind:
            filters.append(
                'metadata any (key="kind" and value="%s")' % kind
            )
        if versions:
            filters.append(
                'metadata any (key="version" and value="%s")'
                % versions
            )
        if len(filters) > 2:
            filter = "%s %s %s" % (
                " ".join(filters[0:2]),
                "and",
                " and ".join(filters[2:]),
            )
        else:
            filter = " ".join(filters[0:2])
        asset_versions = self.search(filter=filter)
        if not asset_versions:
            LOGGER.warning("not find any versions")
            return None
        sorted_versions = sorted(
            asset_versions,
            key=lambda x: distutils.version.StrictVersion(
                x["metadata"]["version"]
            ),
            reverse=True,
        )
        return sorted_versions

    def getNextVersion(self, latest_version, index):
        """
        index 0, 1, 2 = MAJOR0, MINOR, PATCH
        """
        major, minor, patch = latest_version.split(".")
        if index == 0:
            versions = "%s.%s.%s" % (int(major) + 1, 0, 0)
        if index == 1:
            versions = "%s.%s.%s" % (major, int(minor) + 1, 0)
        if index == 2:
            versions = "%s.%s.%s" % (major, minor, int(patch) + 1)
        return versions

    def copyCat(self, targetpath, components, time_stamp=None):
        time_stamp = time_stamp or time.time()
        if os.path.isdir(targetpath):
            try:
                print("\n")
                utils.detetePath(targetpath)
                print("\n")
            except Exception as error:
                LOGGER.error(str(error))
        if not os.path.isdir(targetpath):
            os.makedirs(targetpath)
        os.utime(targetpath, (time_stamp, time_stamp))
        result = []
        for component in components:
            content = copy.deepcopy(component)
            fullpath = self.copyFile(
                targetpath, component, time_stamp
            )
            content["file"] = fullpath
            result.append(content)
        os.chmod(targetpath, stat.S_IREAD)
        return result

    def copyFile(self, targetpath, component, time_stamp):

        if component.get("entity-name"):
            filename = "%s%s" % (
                component["entity-name"],
                component["format"],
            )

        elif component.get("type") == "dirname":
            filename = "%s/%s%s" % (
                component["name"],
                component["filename"],
                component["format"],
            )

        # ===========================================================================================
        # elif component.get("relativePath"):
        #     filename = "%s/%s%s" % (
        #         component["relativePath"], component["filename"], component["format"])
        # ===========================================================================================

        else:
            filename = "%s%s" % (
                component["name"],
                component["format"],
            )

        fullpath = os.path.join(targetpath, filename)
        fullpath = utils.setPathResolver(fullpath)
        if os.path.isfile(fullpath):
            os.chmod(fullpath, stat.S_IWRITE)
            os.remove(fullpath)

        if not os.path.isdir(os.path.dirname(fullpath)):
            os.makedirs(os.path.dirname(fullpath))
            os.utime(targetpath, (time_stamp, time_stamp))

        os.chmod(component["file"], stat.S_IWRITE)

        shutil.copy2(component["file"], fullpath)
        os.utime(fullpath, (time_stamp, time_stamp))
        os.chmod(component["file"], stat.S_IREAD)
        os.chmod(fullpath, stat.S_IREAD)
        LOGGER.info("create file: %s" % fullpath)
        return fullpath

    def collect(self, version, **kwargs):
        index = kwargs.get("index", 2)
        verbose = kwargs.get("verbose", False)
        timestamp = kwargs.get("timestamp", time.time())
        version_path, current_version = self.nextVersionPath(
            "publish", version["task"], index=index
        )
        components = self.downloadVersion(
            version,
            version_path,
            timestamp=timestamp,
            progressbar=None,
        )
        return components

    def downloadComponent(self, component, output_path, **kwargs):
        readOnly = kwargs.get("readOnly", True)
        timestamp = kwargs.get("timestamp", time.time())
        server_location = kwargs.get(
            "server_location", self.serverLocation()
        )
        url = server_location.get_url(component)
        request = requests.get(url, allow_redirects=True)

        if not os.path.isdir(os.path.dirname(output_path)):
            directory = os.path.dirname(output_path)
            os.makedirs(directory)

            if readOnly:
                os.utime(directory, (timestamp, timestamp))
                os.chmod(directory, stat.S_IREAD)

        if os.path.isfile(output_path):
            utils.deleteFile(output_path)

        try:
            open(output_path, "wb").write(request.content)
            valid, message = True, None
        except Exception as error:
            valid, message = False, str(error)

        if valid and readOnly:
            os.utime(output_path, (timestamp, timestamp))
            os.chmod(output_path, stat.S_IREAD)
        return valid, message

    def toDownloadComponent(self, component, dirname, **kwargs):
        basename = self.getBasenameFrommComponent(component)
        filepath = utils.setPathResolver(dirname, suffix=basename)
        message = "downloading to, %s" % (filepath)
        LOGGER.info(message)
        valid, message = self.downloadComponent(
            component, filepath, **kwargs
        )
        return filepath

    def downloadVersion(self, version, directory, **kwargs):
        timestamp = kwargs.get("timestamp", time.time())
        progressbar = kwargs.get("progressbar", None)
        server_location = self.serverLocation()
        if not os.path.isdir(directory):
            os.makedirs(directory)
            os.utime(directory, (timestamp, timestamp))
            os.chmod(directory, stat.S_IREAD)
        else:
            print("\n")
            utils.detetePath(directory)
        if progressbar:
            progressbar.show()
            progressbar.setMaximum(len(version["components"]))
        print("\n")
        LOGGER.info(
            "total components, %s" % len(version["components"])
        )
        LOGGER.info("local path %s" % directory)
        components = []
        for index, each in enumerate(version["components"]):
            filepath = self.getFilePathFromComponent(each, directory)

            if not filepath:
                LOGGER.warning(
                    "unregister component, %s" % each["id"]
                )
                continue

            filepath = os.path.expandvars(filepath)
            message = "%s. downloading to, %s" % (index + 1, filepath)
            LOGGER.info(message)
            if progressbar:
                progressbar.setValue(index + 1)
                progressbar.setFormat("%s - %s" % (message, "%p%"))
            valid, result = self.downloadComponent(
                each,
                filepath,
                timestamp=timestamp,
                server_location=server_location,
            )
            if not valid:
                LOGGER.warning(
                    "%s. downloading error %s"
                    % (index + 1, str(result))
                )
                continue
            component = copy.deepcopy(dict(each["metadata"]))
            component["file"] = filepath
            component["format"] = each["file_type"]
            components.append(component)
        if progressbar:
            progressbar.setValue(100)
            progressbar.setFormat("completed - %s" % ("%p%"))
            progressbar.close()
        return components

    def getFilePathFromComponent(self, component, directory):
        filepath = None
        basename = self.getBasenameFrommComponent(component)
        if not basename:
            return filepath
        filepath = utils.setPathResolver(directory, suffix=basename)
        return filepath

    def getBasenameFrommComponent(self, component):
        basename = None
        metadata = self.getComponentMetadata(component)
        if not metadata:
            return basename
        if not metadata.get("valid"):
            return basename

        if metadata.get("type") == "path":
            basename = "%s%s" % (
                metadata["filename"],
                component["file_type"],
            )

        if metadata.get("type") == "dirname":
            # if metadata.get("type"):
            basename = "%s/%s%s" % (
                metadata["name"],
                metadata["filename"],
                component["file_type"],
            )
        return basename

    def taskLinkName(self, task):
        links = [each["name"] for each in task["link"][1:]]
        link_name = "|".join(links)
        return link_name

    def taskLinkedAssets(self, task, link_name=None):
        link_name = link_name or self.taskLinkName(task)
        filter = "Asset where %s and %s" % (
            'name = "%s"' % link_name,
            'parent.id = "%s"' % task["parent"]["id"],
        )
        assets = self.search(filter=filter)
        return assets

    def findUploadAssetType(self, task):
        typed = self.comp.setpAssetTypeInput(task)
        filter = "AssetType where %s" % ("name = %s" % typed)
        context = self.search(filter).first()
        return context

    def createNewVersion(self, *args, **kwargs):
        task = args[0]
        user = args[1]
        components = args[2]
        next_status = args[3]
        version_path = args[4]
        comment = kwargs.get("comment")
        dependency = kwargs.get("dependency")
        metadata = kwargs.get("metadata")
        timestamp = kwargs.get("timestamp", time.time())

        link_name = self.taskLinkName(task)
        assets = self.taskLinkedAssets(task, link_name)
        if assets:
            asset = assets.first()
            LOGGER.info(
                "updating the asset version on already exists asset entity, %s"
                % asset["id"]
            )
        else:
            asset_type = self.findUploadAssetType(task)
            asset_context = {
                "name": link_name,
                "parent": task["parent"],
                "type": asset_type,
                "user": user,
            }
            asset = self.session.create("Asset", asset_context)
            self.session.commit()
            LOGGER.info("create new asset entity, %s" % asset["id"])
        status_list = self.currentTaskStatus(task)
        contexts = {
            "comment": comment,
            "is_latestVersion": False,
            "is_published": True,
        }
        if status_list.get(next_status):
            contexts["status"] = status_list[next_status]
        contexts["asset"] = asset
        contexts["task"] = task
        contexts["user"] = user
        contexts["metadata"] = metadata
        if dependency:
            # it is for publish, to store which submit version is used
            contexts["metadata"]["dependency"] = {
                "id": dependency["id"],
                "version": dependency["metadata"].get("version"),
                "status": dependency["metadata"].get("status"),
                "status-by": dependency["metadata"].get("status-by"),
                "status-at": dependency["metadata"].get(
                    "status-data"
                ),
            }
        asset_version = self.session.create("AssetVersion", contexts)
        LOGGER.info(
            "create asset version entity, %s" % asset_version["id"]
        )
        server_location = self.serverLocation()
        print("\n")
        LOGGER.info(
            "%s-task - create manifest" % metadata.get("kind")
        )
        task_manifest = manifest.create(
            asset_version,
            version_path,
            comment=comment,
            metadata=metadata,
            timestamp=timestamp,
        )
        components.append(task_manifest)
        print("\n")
        for each in components:
            metadata = copy.deepcopy(each)
            metadata.pop("file")
            data = {"name": each["name"], "metadata": metadata}
            component = asset_version.create_component(
                path=each["file"], data=data, location=server_location
            )
            LOGGER.info("uploaded component, %s" % each["file"])
            if each["name"] == "look" and each["code"] == "image":
                asset_version["thumbnail"] = component
                LOGGER.info(
                    "convert component to thumbnail, %s"
                    % each["file"]
                )
            if each["code"] == "mov":
                asset_version.encode_media(component)
                LOGGER.info(
                    "convert component to playable mov, %s"
                    % each["file"]
                )
        self.session.commit()
        return asset_version

    def getComponentMetadata(self, component):
        if not component.get("metadata"):
            return None
        if not component["metadata"].get("name"):
            return None
        return component["metadata"]

    def getVersionName(self, context):
        if not context:
            return None
        if not context["metadata"].get("version"):
            return None
        return context["metadata"]["version"]

    def startDownloadVersions(self, **kwargs):
        categoryid = kwargs.get("categoryid", None)
        stepid = kwargs.get("stepid", None)
        taskid = kwargs.get("taskid", None)
        kind = kwargs.get("kind", None)
        versions = kwargs.get("versions", None)
        progressbar = kwargs.get("progressbar", None)

        asset_versions = self.searchKindVersions(
            projectid=self.projectid,
            categoryid=categoryid,
            stepid=stepid,
            taskid=taskid,
            kind=kind,
            versions=versions,
        )
        if not asset_versions:
            return
        download.VERSN_OBJECT = self
        components = download.execute(
            versions=asset_versions,
            timestamp=time.time(),
            progressbar=progressbar,
        )
        return components

    def searchDependencyVersions(
        self, task, taskname, kind="publish"
    ):
        dependencies = self.findDependencyTasks(task, tasks=taskname)
        dependency_taks = dependencies.first()
        if not dependency_taks:
            return list()
        versions = self.searchKindVersions(
            taskid=dependency_taks["id"], kind=kind
        )
        return versions


if __name__ == "__main__":
    os.environ["PROJECT-ID"] = "ad54bf94-ba83-41d3-899d-9ed3dc1ab699"
    os.environ["PROJECT-PATH"] = "Z:/projects/RAR"
    os.environ["PIPE-VERSION"] = "0.0.1"

    con = Connect()
    con.authorization()

    from pprint import pprint

    p = con.searchKindVersions(
        taskid = "45fa6eb4-23df-4ddd-a67d-de2f981e6d35",
        kind="publish",
        versions = "0.1.0"
        )
    print (p)
