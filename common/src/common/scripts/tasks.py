import ast

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe import utils
from pipe.core import logger
from apis.studio import Steps
from apis.studio import Tasks
from apis.studio import Kinds
from apis.studio import Versions
from pipe.utils import qwidgets
from common.hierarchy import Shot
from pipe.widgets.treeitems import BuildWidgetTreeItem

LOGGER = logger.getLogger(__name__)


class Query(object):

    eventEnable = True
    eventName = "queryTask"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        taskType = cls.input["taskType"]
        combobox = cls.input["widget"]
        progressbar = cls.input.get("progressbar")

        LOGGER.info("collecting your %s task" % taskType)
        task = Tasks()
        # task.authorization()

        if progressbar:
            message = "loading %s tasks, please wait!... " % taskType
            progressbar.setMessage(message)

        taskList = task.getMyTasks(names=taskType) or list()

        if progressbar:
            maximum = len(taskList) if len(taskList) else 2
            progressbar.setMaximum(maximum)

        combobox.clear()
        combobox.addItem("Select your task!...")
        

        for index, each in enumerate(taskList):
            header = task.contextHeader(each)
            
            if progressbar:
                progressbar.setProgress(
                    index,
                    header,
                    plane=True,
                    error=False,
                    thread=False,
                )

            iconpath = qwidgets.encodeIcon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            combobox.addItem(icon, header)
            cls.output[header] = each
            # break

        if progressbar:
            progressbar.clear()

        LOGGER.info("loaded %s task" % taskType)


class LookdevVersions(object):

    eventEnable = True
    eventName = "queryLookdevVersions"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input["task"]
        combobox = cls.input["widget"]
        LOGGER.info(
            "collecting lookdev versions %s task" % task["name"]
        )
        versions = cls.get(cls, task)

        context = {}
        for each in versions:
            combobox.addItem(each["metadata"]["version"])
            context[each["metadata"]["version"]] = each
        cls.output["versions"] = context

    def get(self, task):
        vers = Versions()
        asset_versions = vers.getDependencyVersions(
            task, "Lookdev", kind="publish"
        )
        if not asset_versions:
            return list()
        return asset_versions


class SetupShotAssets(object):

    eventEnable = True
    eventName = "setupShotAssets"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input["task"]
        treewidget = cls.input["widget"]
        progressbar = cls.input.get("progressbar")
        input = cls.input["input"]

        if progressbar:
            message = "loading assets, please wait!... "
            progressbar.setMessage(message)

        buildContext = utils.searchContext(
            input["scene"], "name", value="build", first=True
        )
        filetype = buildContext["filetype"]

        treewidget.clear()

        assetList = cls.getSceneAssembly(task)
        
        from pprint import pprint
        
        print ("\n+++++++++++++++++++++++++")
        print ("assetList")
        pprint (assetList)
        print ("--------------------------\n")        
        
        # print ("1assetList", assetList)
        
        context = SetupShotAssets.validate(assetList)

        if progressbar:
            maximum = len(context) if len(context) else 1
            progressbar.setMaximum(maximum)
            
        from pprint import pprint
        
        print ("\n--------------------------")
        pprint (context)
        print ("--------------------------\n")

        for index, each in enumerate(context):
            if progressbar:
                message = "loading %s versions " % each["name"]
                progressbar.setProgress(
                    index,
                    message,
                    plane=True,
                    error=False,
                    thread=False,
                )
            parameters = cls.setupParameter(each["name"], input["items"])

            treeItem = BuildWidgetTreeItem(
                treewidget,
                items=input["items"],
                parameters=parameters,
                fontsize=input.get("fontsize", 12),
                color=each.get("color"),
                filetype=filetype,
                progressbar=progressbar,
                node = each.get("node"),
                checkState=each.get("checkState")
            )

        if progressbar:
            progressbar.clear()
            
    @staticmethod
    def validate(context):
        sceneList = Shot.getChidren()
        if not sceneList:
            for each in context:
                each["color"] = [0, 255, 0]
            return context

        existsAssets = []
        newAssets = []
        deletedAssets = []
        
        nameList = [each["name"] for each in context]

        # find conflict and normal assets
        for each in sceneList:
            if each["name"] in nameList:
                existsList = [x["name"] for x in existsAssets]
                if each["name"] in existsList:
                    each["color"] = [255, 255, 0]
                    each["checkState"] = False
                    newAssets.append(each)
                else:
                    existsAssets.append(each)
            else:
                each["color"] = [255, 255, 0]
                each["checkState"] = False
                newAssets.append(each)

        nameList = [each["name"] for each in sceneList]
        
        # find deleted
        for each in context:
            if each["name"] in nameList:
                continue
            each["color"] = [255, 0, 0]
            each["checkState"] = True
            deletedAssets.append(each)

        result = existsAssets + newAssets + deletedAssets
        return result

    @classmethod
    def setupParameter(cls, name, items):
        assetEntity = Steps().getAssetByName(name)
        parameters = list()

        for each in ["Asset", "Type"]:
            currentItem = utils.searchContext(
                items, "name", value=each, first=True
            )
            parameter = {"order": currentItem["order"]}
            fileds = currentItem["field"].split(".")
            value = utils.getFieldValue(
                assetEntity, fileds, fieldchild=None
            )
            parameter["value"] = value
            parameters.append(parameter)

        taskItem = utils.searchContext(
            items, "name", value="Task", first=True
        )
        kindsItem = utils.searchContext(
            items, "name", value="Kinds", first=True
        )
        versionItem = utils.searchContext(
            items, "name", value="Version", first=True
        )
        locationItem = utils.searchContext(
            items, "name", value="Location", first=True
        )

        assetType = parameters[1]["value"]
        defaultItem = utils.searchContext(
            taskItem["default"], "type", value=assetType, first=True
        )

        taskParameter = {
            "order": taskItem["order"],
            "default": defaultItem["task"],
        }

        taskParameter["values"] = list()
        fileds = taskItem["field"].split(".")
        taskContextList = list()
        
        #===========================================================================================
        # from pprint import pprint
        # print ("\nchildField")
        # pprint(taskItem)
        # print ("\nassetEntity")
        # pprint (assetEntity)
        #===========================================================================================

        for task in assetEntity[taskItem["childField"]]:
            versionContext = SetupShotAssets.getTaskVersions(
                cls, task
            )
            value = utils.getFieldValue(task, fileds, fieldchild=None)
            context = {
                "task": task,
                "value": value,
                "components": versionContext,
                "default": kindsItem["default"],
            }
            taskContextList.append(context)

        taskParameter["values"] = taskContextList
        taskParameter["kindIndex"] = kindsItem["order"]
        taskParameter["versionIndex"] = versionItem["order"]
        taskParameter["locationIndex"] = locationItem["order"]

        parameters.append(taskParameter)
        return parameters

    def getTaskVersions(self, task):
        kindList = Kinds().getPrimaryKindList()
        contextList = list()
        for kind in kindList:
            versionsContex = Versions().getKindVersionsContext(
                task["id"], kind
            )
            context = {"kind": kind, "versions": versionsContex}
            contextList.append(context)
        return contextList

    @classmethod
    def getSceneAssembly(cls, task):
        assetList = []
        if not task["parent"]["metadata"]:
            return assetList
        metadata = task["parent"]["metadata"]
        if not metadata.get("sceneAssembly"):
            return assetList
        sceneAssembly = ast.literal_eval(metadata["sceneAssembly"])
        if not sceneAssembly.get("assets"):
            return assetList
        assetList = sceneAssembly["assets"]

        return assetList
    

        
        """
        [{'color': [170, 85, 255],
          'fontsize': 14,
          'id': '7a5a74ed-5146-4ca7-a642-a9c6d4f540ab',
          'name': 'generic',
          'type': 'AssetBuild'},
         {'color': [170, 85, 255],
          'fontsize': 14,
          'id': '8bec31c7-9926-40fb-b6ec-96615b072f6b',
          'name': 'jasmin',
          'type': 'AssetBuild'},
         {'color': [170, 85, 255],
          'fontsize': 14,
          'id': 'b6600730-3f25-4d29-8ad6-da9c9a18dfa0',
          'name': 'southcity',
          'type': 'AssetBuild'}]
        """
            
