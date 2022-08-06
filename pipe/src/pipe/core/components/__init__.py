# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:48:35:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core submit and publish components.

import os
import glob
import copy
import json

from pipe import utils
from pipe.core import inputs
from pipe.core import logger

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Connect(inputs.Connect):
    typed = "components"

    def __init__(self, typed=typed, **kwargs):
        super(Connect, self).__init__(typed, **kwargs)

    def taskComponents(self, task_name):
        contexts = list(
            filter(lambda k: k["name"] == task_name, self.get())
        )
        if not contexts:
            LOGGER.warning(
                'not found "%s" components in the configure'
                % task_name
            )
            return
        return contexts[0]

    def findComponents(self, components, **kwargs):
        name = kwargs.get("name")
        format = kwargs.get("format")
        filename = kwargs.get("filename")

        source_components = list(
            filter(
                lambda k: k["name"] == name
                and k["file_type"] == format
                and k["metadata"].get("filename") == filename,
                components,
            )
        )
        if not source_components:
            return list()
        return source_components

    def findSpecificComponent(self, components, name, first=False):
        components = list(
            filter(lambda k: k["name"] == name, components)
        )
        if not components:
            LOGGER.warning("could not found any components")
            return
        if first:
            return components[0]
        return components

    def findComponentFileName(self, components, name, first=False):
        components = self.findSpecificComponent(
            components, name, first=first
        )
        if not components:
            return
        if not isinstance(components, list):
            components = [components]

        filenames = []
        for component in components:
            filename = "%s%s" % (
                component["metadata"]["filename"],
                component["metadata"]["format"],
            )
            filenames.append(filename)

        if first:
            return filenames[0]
        return filenames

    def kinds(self):
        inpt = inputs.Connect("kind")
        return inpt.get()

    def searchKindContext(self, name):
        kinds = self.kinds()
        contexts = list(filter(lambda k: k["name"] == name, kinds))
        if not contexts:
            return None
        return contexts[0]

    def findKindName(self, name):
        context = self.searchKindContext("local")
        kind = context.get("display-name")
        return kind

    def componentPath(self, task, kind=None):
        if not kind:
            kind = self.findKindName("local")
        link_name = [each["name"] for each in task["link"][1:]]
        folders = link_name + [kind]
        path = utils.setPathResolver(
            os.getenv("PROJECT-PATH"), folders=folders
        )
        return path

    def setpAssetTypeInput(self, task):
        input = self.taskInputs(task)
        if not input:
            return
        return input.get("AssetType")

    def taskInputs(self, task):
        name = task["type"]["name"]
        inputs = list(filter(lambda k: k["name"] == name, self.get()))
        if not inputs:
            LOGGER.warning('not found task "%s" in the config' % name)
            return
        return inputs[0]

    def findExtentionFile(self, files, formats):
        for each in files:
            for format in formats:
                if not each.endswith(format):
                    continue
                path = utils.setPathResolver(each)
                extension = format
                return path, extension
        return None, None

    def findFolderFiles(self, dirname, formats, input_context):
        contexts = []
        if not os.path.isdir(dirname):
            return contexts
        basename = os.path.basename(dirname)
        for each in os.listdir(dirname):
            path = utils.setPathResolver(dirname, folders=[each])
            extension = None
            for format in formats:
                if not path.endswith(format):
                    continue
                extension = format
            if not extension:
                continue
            relativePath = utils.setPathResolver(
                basename, folders=[each]
            )
            context = input_context.copy()
            filename, format = utils.findFileNameAndFormat(path)
            context["file"] = path
            context["format"] = extension
            context["filename"] = filename
            context["relativePath"] = relativePath
            context["valid"] = True
            contexts.append(context)
        return contexts

    def collectFromDirectory(self, task, path=None, verbose=False):
        config_context = self.taskInputs(task)
        if not config_context:
            return
        component_path = path or self.componentPath(task)
        contexts = []
        for component in config_context.get("components"):
            values = copy.deepcopy(component)
            values.pop("formats")
            values["valid"] = False
            component_name = component["name"]

            if component.get("entity-name"):
                values["entity-name"] = task["parent"]["name"]
                component_name = task["parent"]["name"]

            if component["type"] == "dirname":
                folder_dirname = utils.setPathResolver(
                    component_path, folders=[component_name]
                )
                input_context = copy.deepcopy(values)
                folder_context = self.findFolderFiles(
                    folder_dirname,
                    component["formats"],
                    input_context,
                )

                contexts.extend(folder_context)
            else:
                files = glob.glob(
                    "%s/%s.*" % (component_path, component_name)
                )
                current_file, format = self.findExtentionFile(
                    files, component["formats"]
                )
                filename, format = utils.findFileNameAndFormat(
                    current_file
                )

                values["file"] = current_file
                values["filename"] = filename
                values["format"] = format

                if values["file"]:
                    values["valid"] = True
                contexts.append(values.copy())
        if verbose:
            print(json.dumps(contexts, indent=4))
        return contexts

    def collectFromWidget(self, task, treewidget, verbose=False):
        config_context = self.taskInputs(task)
        if not config_context:
            return
        components = config_context.get("components")
        contexts = []
        widget_item = treewidget.invisibleRootItem()
        for index in range(widget_item.childCount()):
            parent = widget_item.child(index)
            display_name = parent.text(1)
            contents = list(
                filter(
                    lambda k: k["display-name"] == display_name,
                    components,
                )
            )
            if not contents:
                continue
            values = copy.deepcopy(contents[0])
            values.pop("formats")

            if contents[0].get("entity-name"):
                values["entity-name"] = task["parent"]["name"]

            if values["type"] == "dirname":
                items = [
                    parent.child(x)
                    for x in range(parent.childCount())
                ]
            else:
                items = [parent.child(0)]

            for each in items:
                current_file = each.text(1)
                # format = utils.findFileFormat(current_file)
                filename, format = utils.findFileNameAndFormat(
                    current_file
                )
                values["file"] = current_file
                values["filename"] = filename
                values["format"] = format
                values["valid"] = True

                contexts.append(values.copy())

        if verbose:
            print(json.dumps(contexts, indent=4))
        return contexts


if __name__ == "__main__":

    from pipe.core import tasks

    tak = tasks.Connect()
    tak.authorization()
    task = tak.currentTask("1f123cd4-09e8-434b-b6be-54b24444b147")

    con = Connect()

    data = con.collectFromDirectory(
        task, path="Z:/templates/batman/lookdev/normal", verbose=True
    )
