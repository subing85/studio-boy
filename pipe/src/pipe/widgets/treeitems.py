import os

from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets

from pipe.widgets import progressbar

LOGGER = logger.getLogger(__name__)


from pprint import pprint


class ParametrTreeItem(QtWidgets.QTreeWidgetItem):

    entity = None

    def __init__(self, parent, **kwargs):
        super(ParametrTreeItem, self).__init__(parent)

        self.name = kwargs.get("name") or "Name"
        self.category = kwargs.get("category") or None
        self.parameter = kwargs.get("parameter") or list()
        self.fontsize = kwargs.get("fontsize") or 15
        self.color = kwargs.get("color") or [0, 0, 0]
        self.index = kwargs.get("index") or 0
        self.item = kwargs.get("item") or None
        self.pin = kwargs.get("pin") or False

    @property
    def treewidget(self):
        return self.treeWidget()

    @property
    def getWidgetItem(self):
        return self.parent()

    def setEntity(self, entity):
        self.entity = entity

    def removeItem(self):
        self.parent().removeChild(self)

    def setupAllParameters(self, parameters):
        for x, each in enumerate(parameters):
            alignment = QtCore.Qt.AlignCenter
            fontsize, bold = self.fontsize - 1, False
            index = x + 1
            if x == 0:
                self.setToolTip(index, self.category)
                alignment = QtCore.Qt.AlignLeft
                fontsize = self.fontsize
                bold = True
            value = (
                each["value"]
                if each.get("value")
                else each.get("default")
            )
            self.setText(index, str(value))
            qwidgets.setItemTextAlignment(self, index, alignment)
            qwidgets.setItemFont(
                self, index, size=fontsize, bold=bold
            )
        qwidgets.setItemforegroundColor(self, 1, color=self.color)

    def setupNameParameter(self, name=None):
        name = name or self.name
        self.setText(1, name)
        self.setToolTip(1, self.category)
        qwidgets.setItemTextAlignmentLeft(self, 1)
        qwidgets.setItemFont(self, 1, size=self.fontsize, bold=True)
        qwidgets.setItemforegroundColor(self, 1, color=self.color)

    def setupParameters(self, parameter=None):
        parameter = parameter or self.parameter
        for index, param in enumerate(parameter):
            self.setText(index + 2, str(param))
            qwidgets.setItemTextAlignmentCenter(self, index + 2)
            if not self.fontsize:
                continue
            qwidgets.setItemFont(
                self, index + 2, size=self.fontsize, bold=False
            )


class RootTreeItem(ParametrTreeItem):
    def __init__(self, parent, **kwargs):
        super(RootTreeItem, self).__init__(parent, **kwargs)

        self.setFlags(
            QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsUserCheckable
            | QtCore.Qt.ItemIsEnabled
        )
        self.setupNameParameter()
        self.setupParameters()
        self.button = qwidgets.createAddButton(size=self.fontsize - 2)
        treewidget = self.treeWidget()
        treewidget.setItemWidget(self, 0, self.button)
        treewidget.header().resizeSection(0, 100)


class AssetTreeItem(ParametrTreeItem):
    def __init__(self, parent, **kwargs):
        super(AssetTreeItem, self).__init__(parent, **kwargs)


class SequenceTreeItem(RootTreeItem):
    def __init__(self, parent, **kwargs):
        super(SequenceTreeItem, self).__init__(parent, **kwargs)


class ShotTreeItem(ParametrTreeItem):
    def __init__(self, parent, **kwargs):
        super(ShotTreeItem, self).__init__(parent, **kwargs)


class HistoryTreeItem(ParametrTreeItem):
    def __init__(self, parent, **kwargs):
        super(HistoryTreeItem, self).__init__(parent, **kwargs)

        self.color = (0, 179, 0) if self.pin else (255, 170, 0)
        uui = utils.encodeBinascii(
            "%s:%s" % (self.index, self.item.__class__)
        )
        self.setText(0, str(self.index))
        self.setText(1, self.category)
        self.setText(2, uui)
        qwidgets.setItemforegroundColor(self, 1, color=self.color)
        treewidget = self.treeWidget()
        treewidget.header().resizeSection(0, 60)
        treewidget.header().resizeSection(1, 110)


class WidgetTreeItem(QtWidgets.QTreeWidgetItem):

    name = None
    idName = None
    entity = dict()
    inputs = dict()
    entityType = None
    # parentEntity = None
    parameters = dict()

    def __init__(self, parent, **kwargs):
        super(WidgetTreeItem, self).__init__(parent)
        self.name = kwargs.get("name") or "Name"
        self.path = kwargs.get("path") or None

        self.category = kwargs.get("category") or None
        self.fontsize = kwargs.get("fontsize") or 15
        self.color = kwargs.get("color") or [0, 0, 0]
        self.index = kwargs.get("index") or 0

        self.nullitem = None

        self.setupName()
        self.setupPath()
        self.setupWidgets()

    @property
    def treewidget(self):
        return self.treeWidget()

    @property
    def getWidgetItem(self):
        return self.parent()

    def setEntity(self, entity):
        self.name = entity.get("name")

        self.entity = entity
        self.entityType = entity.entity_type

    # =================================================================
    # def setParentEntity(self, entity):
    #     self.parentEntity = entity
    # =================================================================

    def setIDName(self, idName):
        self.idName = idName

    def setParameters(self, parameters):
        self.parameters = parameters.copy()

    def setInputs(self, inputs):
        self.inputs = inputs.copy()

    def setupName(self, name=None):
        name = name or self.name
        self.setText(0, name)
        self.setToolTip(0, self.category)
        qwidgets.setItemTextAlignmentLeft(self, 0)
        qwidgets.setItemFont(self, 0, size=self.fontsize, bold=True)
        qwidgets.setItemforegroundColor(self, 0, color=self.color)

    def setupPath(self, path=None):
        path = path or self.path
        if not path:
            LOGGER.warning("invalid path")
            return
        self.setText(1, path)
        qwidgets.setItemTextAlignmentLeft(self, 1)
        # qwidgets.setItemFont(self, 1, size=self.fontsize, bold=True)

        color = [0, 0, 0] if os.path.isdir(path) else [255, 0, 255]
        qwidgets.setItemforegroundColor(self, 1, color=color)

    def createNull(self):
        self.nullitem = QtWidgets.QTreeWidgetItem(self)

    def removeNullItem(self):
        self.removeChild(self.nullitem)
        self.nullitem = None

    def collapseItem(self):
        self.treewidget.collapseItem(self)

    def setupWidgets(self):
        self.groupbox = QtWidgets.QGroupBox(self.treewidget)
        # self.groupbox.setFlat(True)
        self.groupbox.setStyleSheet("border-radius: 4px;")
        self.treewidget.setItemWidget(self, 2, self.groupbox)

        self.horizontallayout = QtWidgets.QHBoxLayout(self.groupbox)

        self.progressbar = progressbar.Connect(
            self.treewidget, visible=True, plane=False, value=50
        )
        self.horizontallayout.addWidget(self.progressbar)

        self.downloadbutton = QtWidgets.QPushButton(self.treewidget)
        self.downloadbutton.setStyleSheet("border-radius: 4px;")

        # self.downloadbutton.setMinimumSize(QtCore.QSize(size * 2, size * 2))
        # self.downloadbutton.setMaximumSize(QtCore.QSize(size * 2, size * 2))
        self.horizontallayout.addWidget(self.downloadbutton)

        self.setDwonloadMode()

    def setProgressbarMode(self):
        self.downloadbutton.setText("Downloading....")
        self.progressbar.show()

    def setDwonloadMode(self):
        self.progressbar.hide()
        self.downloadbutton.setText("Download")


class RootWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(RootWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class AssetWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(AssetWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class SequenceWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(SequenceWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class ShotWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(ShotWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class TaskWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(TaskWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class KindsWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(KindsWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class VersionWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(VersionWidgetTreeItem, self).__init__(parent, **kwargs)


class CommonWidgetTreeItem(WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(CommonWidgetTreeItem, self).__init__(parent, **kwargs)
        self.createNull()


class BuildWidgetTreeItem(QtWidgets.QTreeWidgetItem):

    name = None
    typeName = None

    taskContext = list()
    taskList = list()
    taskName = None
    taskEntity = None

    kindContext = list()
    kindList = list()
    kindName = None

    versionContext = list()
    versionList = list()
    versionName = None
    location = None
    versionEntity = None
    filepath = None
    filename = None

    def __init__(self, parent, **kwargs):
        super(BuildWidgetTreeItem, self).__init__(parent)

        self.fontsize = kwargs.get("fontsize", 12)
        self.color = kwargs.get("color", [0, 200, 255])
        # self.items = kwargs.get("items", list())
        self.parameters = kwargs.get("parameters")
        self.filetype = kwargs.get("filetype")
        self.progressbar = kwargs.get("progressbar")
        
        self.node = kwargs.get("node")
        self.checkedState = QtCore.Qt.Checked if kwargs.get("checkState") else QtCore.Qt.Unchecked

        self.setupParameter(parameters=self.parameters)

    @property
    def treewidget(self):
        return self.treeWidget()
    
    def isCheckState(self):
        state = True if self.checkState(1) == QtCore.Qt.Checked else False
        return state

    def createCombobox(self, index):
        combobox = QtWidgets.QComboBox(self.treewidget)
        self.treewidget.setItemWidget(self, index, combobox)
        combobox.setStyleSheet("border-radius: 4px; color: rgb(%s, %s, %s);" % (self.color[0], self.color[1], self.color[2]))
        return combobox

    def createLocationButton(self, index):
        button = QtWidgets.QPushButton(self.treewidget)
        self.treewidget.setItemWidget(self, index, button)
        button.setStyleSheet("border-radius: 4px; text-align: left; background-color: rgb(43, 43, 43);")
        return button

    def setupParameter(self, parameters=None):
        self.parameters = parameters or self.parameters

        self.buttonRefresh= qwidgets.createRefreshButton(size=10, font=12)
        self.treewidget.setItemWidget(self, 0, self.buttonRefresh)
        self.buttonRefresh.clicked.connect(self.refreshItem)

        self.setCheckState(1, self.checkedState)

        for each in self.parameters[0:2]:
            self.setText(each["order"], each.get("value"))
            qwidgets.setItemTextAlignmentLeft(self, each["order"])
            qwidgets.setItemFont(
                self, each["order"], size=self.fontsize, bold=False
            )
            qwidgets.setItemforegroundColor(self, each["order"], color=self.color)

        self.name = self.parameters[0]["value"]
        self.typeName = self.parameters[1]["value"]
        self.taskContext = self.parameters[2]
        
        #===========================================================================================
        # from pprint import pprint
        #  
        # print ('\nparameters---------------------------')
        # pprint (parameters)
        # print ("\n\ntaskContext")
        # pprint(self.taskContext)
        # print ("----------------------------\n")
        #===========================================================================================
        
        self.setupTaskParameter()

    def getWidgetCode(self, value, values, index):
        colorSheet = None
        if value in values:
            nodeIndex = values.index(value)
            if index != nodeIndex:
                colorSheet = "color: rgb(255, 0, 255);"
            index = nodeIndex
        else:
            colorSheet = "color: rgb(255, 255, 0);"
        return colorSheet, index

        
    def refreshItem(self):
        
        taskName = self.node.getTaskName() if self.node else None
        taskIndex = self.typeList.index(self.taskContext["default"])
        self.typeList = [each["value"] for each in self.taskContext["values"]]
        self.setCombobox(self.comboboxTask, taskName, taskIndex, self.typeList)

        kindName = self.node.getKind() if self.node else None
        kindIndex = self.kindList.index(self.kindContext["default"])
        self.kindList = [each["kind"] for each in self.kindContext["components"]]
        self.setCombobox(self.comboboxKind, kindName, kindIndex, self.kindList)

        versionName = self.node.getVersion() if self.node else None
        self.versionList = [each["name"] for each in self.versionContext["versions"]]
        self.setCombobox(self.comboboxVersion, versionName, 0, self.versionList)


    def setCombobox(self, combobox, name, index, context):
        if name:
            colorSheet, index = self.getWidgetCode(name, context, index)
            if colorSheet:
                combobox.setStyleSheet("border-radius: 4px; %s" % colorSheet)
        combobox.setCurrentIndex(index)
        

    def setupTaskParameter(self):
        self.comboboxTask = self.createCombobox(self.taskContext["order"])
        self.comboboxKind = self.createCombobox(self.taskContext["kindIndex"])
        self.comboboxVersion = self.createCombobox(self.taskContext["versionIndex"])
        self.buttonLocation = self.createLocationButton(self.taskContext["locationIndex"])

        self.typeList = [each["value"] for each in self.taskContext["values"]]
        taskIndex = self.typeList.index(self.taskContext["default"])
        self.comboboxTask.addItems(self.typeList)
        self.comboboxTask.currentIndexChanged.connect(self.setupKindParameter)
        
        taskName = self.node.getTaskName() if self.node else None
        self.setCombobox(self.comboboxTask, taskName, taskIndex, self.typeList)

    def setupKindParameter(self, *args):
        self.taskContextValues = self.taskContext["values"]

        self.comboboxKind.clear()
        self.taskName = self.comboboxTask.currentText()
        
        self.kindContext = utils.searchContext(self.taskContextValues, "value", value=self.taskName, first=True)
        self.kindList = [each["kind"] for each in self.kindContext["components"]]
        self.comboboxKind.addItems(self.kindList)
        kindIndex = self.kindList.index(self.kindContext["default"])

        self.comboboxKind.currentIndexChanged.connect(self.setupVersionParameter)
        
        kindName = self.node.getKind() if self.node else None
        self.setCombobox(self.comboboxKind, kindName, kindIndex, self.kindList)

        self.taskEntity = self.kindContext["task"]
        
        

    def setupVersionParameter(self, *args):
        self.kindContextValue = self.kindContext["components"]

        self.comboboxVersion.clear()

        self.kindName = self.comboboxKind.currentText()

        self.versionContext = utils.searchContext(self.kindContextValue, "kind", value=self.kindName, first=True)

        self.versionList = [each["name"] for each in self.versionContext["versions"]]
        self.versionList = utils.sortedVersions(self.versionList, reverse=True)
        self.comboboxVersion.addItems(self.versionList)

        self.comboboxVersion.currentIndexChanged.connect(self.setupLocationParameter)

        versionName = self.node.getVersion() if self.node else None
        self.setCombobox(self.comboboxVersion, versionName, 0, self.versionList)

        self.setupLocationParameter(self.versionContext["versions"])

    def setupLocationParameter(self, *args):
        self.versionContextValue =  self.versionContext["versions"]

        self.buttonLocation.setText("  ")
        self.buttonLocation.setStyleSheet("text-align: left; background-color: rgb(43, 43, 43); color: rgb(%s, %s, %s);" % (self.color[0], self.color[1], self.color[2]))
        self.versionName = self.comboboxVersion.currentText()
        version_context = utils.searchContext(self.versionContextValue, "name", value=self.versionName, first=True)

        if not version_context:
            LOGGER.warning(
                "could not found %s|%s|%s %s"
                % (
                    self.name,
                    self.typeName,
                    self.taskName,
                    self.kindName,
                )
            )
            return

        self.location = version_context["path"]

        self.buttonLocation.setText("  %s" % self.location)
        self.buttonLocation.clicked.connect(self.openLocation)
        self.versionEntity = version_context["version"]

        self.filename = studio.Components().findComponentFileName(
            self.versionEntity["components"],
            self.filetype,
            first=True,
        )

        self.filepath = utils.setPathResolver(
            self.location, suffix=self.filename
        )

    def openLocation(self):
        if not self.location:
            LOGGER.warning("current location is None")
            return

        if not os.path.isdir(self.location):
            LOGGER.warning(
                "Could not exists location %s" % self.location
            )
            return

        utils.openLink(self.location)


if __name__ == "__main__":
    pass
