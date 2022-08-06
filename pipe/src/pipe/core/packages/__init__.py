# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:01:04:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core git packages.

import os
import git
import json
import gitlab

from pipe import utils
from pipe import resources
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Connect(object):
    def __init__(self, **kwargs):
        """https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#project-tags"""
        self.auth_json = kwargs.get("auth_json")

    def authorization(self):
        account = resources.getInputData("repository")
        self.session = gitlab.Gitlab(
            account["url"],
            private_token=account["token"],
            api_version=4,
        )
        self.session.auth()

    def _authorization(self, json_path):
        if not json_path:
            LOGGER.warning("invalid json_path")
            return
        if not os.path.isfile(json_path):
            LOGGER.warning("not found %s" % json_path)
            return
        content = resources.getData(json_path)
        if not content.get("enable"):
            return None
        if not content.get("data"):
            return None
        account = content["data"]
        self.session = gitlab.Gitlab(
            account["url"],
            private_token=account["token"],
            api_version=4,
        )
        self.session.auth()

    @property
    def groupPath(self):
        return "studio-pipe"

    @property
    def groupName(self):
        return "Studio-Pipe"

    @property
    def configPath(self):
        path = utils.setPathResolver(
            self.pipePath, folders=["config.json"]
        )
        return path

    @property
    def pipePath(self):
        return os.getenv("PIPELINE-PATH")

    def getProjectPath(self, name, tag=None):
        if tag:
            path = utils.setPathResolver(
                self.pipePath, folders=[name, tag]
            )
        else:
            path = utils.setPathResolver(
                self.pipePath, folders=[name]
            )
        return path

    def hasProject(self, name, tag=None):
        project_path = self.getProjectPath(name, tag=tag)
        if os.path.isdir(project_path):
            return True
        return False

    def configContext(self, all=False):
        data = resources.getData(self.configPath)
        if not data.get("enable"):
            return None
        if all:
            return data
        return data.get("data")

    def getGroup(self, group_path=None):
        group_path = group_path or self.groupPath
        groups = self.session.groups.list(search=group_path)
        if not groups:
            LOGGER.info(
                "not found group <%s> in the studio-pipe gitlab"
                % group_path
            )
            return None
        group = groups[0]
        return group

    def getProjects(self):
        projects = self.session.projects.list(visibility="private")
        projects = sorted(
            projects, key=lambda k: (k.created_at), reverse=True
        )
        valid_projects = []
        for project in projects:
            group_path = project.namespace.get("path")
            if group_path != self.groupPath:
                continue
            valid_projects.append(project)
        return valid_projects

    def getTags(self, project):
        tags = project.tags.list()
        tags = sorted(
            tags,
            key=lambda k: (k.commit.get("created_at")),
            reverse=True,
        )
        return tags

    def findProject(self, name, group=None):
        group = group or self.groupPath
        try:
            project = self.session.projects.get(
                "%s/%s" % (group, name)
            )
        except Exception:
            project = None
        return project

    def cloneProject(self, project_name, group_path=None, tag=None):
        group_path = group_path or self.groupPath
        project = self.findProject(project_name, group=group_path)
        project_path = self.getProjectPath(project_name, tag)
        if os.path.isdir(project_path):
            utils.detetepath(project_path)
        if not os.path.isdir(project_path):
            os.makedirs(project_path)
        git.Git(project_path).clone(project.http_url_to_repo)
        local_path = utils.setPathResolver(
            project_path, folders=[project.name]
        )
        if tag:
            repo = git.Git(local_path)
            repo.checkout(tag)
        print("\n")
        LOGGER.info("project: %s" % project.name)
        LOGGER.info("tag: %s" % tag)
        LOGGER.info("path: %s" % local_path)

    def updateConfig(self, projects):
        context = self.configContext(all=True)
        for project, tag in projects.items():
            contents = list(
                filter(
                    lambda k: k["name"] == project, context["data"]
                )
            )
            if not contents:
                LOGGER.warning("not found <%s> in the config data")
                continue
            content = contents[0]
            index = context["data"].index(content)
            context["data"][index]["name"] = project
            context["data"][index]["version"] = tag
        context["lastModified"] = resources.getDateTimes()
        with open(self.configPath, "w") as file:
            json.dump(context, file, indent=4)
        LOGGER.info("updated config %s" % self.configPath)
        return True


if __name__ == "__main__":
    pass
