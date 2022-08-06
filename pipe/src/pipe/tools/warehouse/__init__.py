import os
import sys
import copy
import threading

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets

from pipe.widgets import ProgressBar
from pipe.widgets import RootWidgetTreeItem
from pipe.widgets import ShotWidgetTreeItem
from pipe.widgets import TaskWidgetTreeItem
from pipe.widgets import AssetWidgetTreeItem
from pipe.widgets import KindsWidgetTreeItem
from pipe.widgets import CommonWidgetTreeItem
from pipe.widgets import VersionWidgetTreeItem
from pipe.widgets import SequenceWidgetTreeItem
from pipe.widgets import EntityProperty


LOGGER = logger.getLogger(__name__)

import json
from pprint import pprint


"""
download reparent 
select the item signal
build, open, reference
add progress bar
"""


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.title = "Studio-Pipe WareHouse -0.0.1"
        self.titleicon = kwargs.get("titleicon") or [768, 144]
        self.projecticon = kwargs.get("showicon") or [256, 144]
        self.wsize = kwargs.get("wsize") or [950, 650]
        self.pipe_version = os.getenv("PIPE-VERSION") or "unknown"
        self.application = kwargs.get("application") or None

        self.iconpath = resources.getIconPath()
        self.browsepath = resources.getBrowsePath()

        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.alignleft = (
            QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter
        )
        self.aligncenter = QtCore.Qt.AlignCenter

        self.proj = studio.Project()
        self.disp = studio.Discipline()
        self.categories = self.proj.searchCategory(None)
        self.kind = studio.Kinds()
        self.warh = studio.Inputs(typed="warehouse")
        self.vers = studio.Versions()

        self.hierarchy = self.warh.get()
        self.propery = studio.Inputs(typed="property")

        self.setupUi()
        self.setupDefault()
        self.setupDiscipline()
        # self.setupIcons()
        self.setupCategories()

    def setupUi(self):

        self.setObjectName("mainwindow_warehouse")
        self.setWindowTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticallayout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout)
        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setText("Unknown-User")
        self.label_user.setStyleSheet("font: 87 10pt 'Arial Black';")
        self.label_user.setAlignment(
            QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter
        )
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )
        self.label_user.setSizePolicy(size_policy)
        self.horizontallayout.addWidget(self.label_user)
        self.label_version = QtWidgets.QLabel(self)
        self.label_version.setText("PIPE Package Version:")
        self.label_version.setStyleSheet(
            "color:rgb(255,170,0); font: 87 10pt 'Arial Black';"
        )
        self.label_version.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )
        self.label_version.setSizePolicy(size_policy)
        self.horizontallayout.addWidget(self.label_version)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.verticallayout.addWidget(self.splitter)

        self.treewidget = QtWidgets.QTreeWidget(self.splitter)
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.treewidget.setColumnCount(3)
        self.treewidget.setContentsMargins(0, 0, 0, 0)
        self.treewidget.headerItem().setText(0, "")
        self.treewidget.headerItem().setText(1, "")
        self.treewidget.header().resizeSection(0, 200)

        # self.groupbox = QtWidgets.QGroupBox(self.splitter)
        self.groupbox = EntityProperty(
            self.splitter,
            title="Property",
            visible=False,
            application=self.application,
        )

        self.progressbar = ProgressBar(
            self, visible=True, plane=False
        )
        self.verticallayout.addWidget(self.progressbar)

        self.treewidget.itemClicked.connect(self.selectCurrentContext)
        self.treewidget.itemExpanded.connect(self.itemExpanded)

    def setupDefault(self):
        self.setupAlignment()
        for index in range(self.treewidget.columnCount()):
            self.treewidget.headerItem().setText(index, "")

    def setupAlignment(self):
        self.splitter.setSizes([649, 278])
        self.treewidget.header().resizeSection(0, 200)
        self.treewidget.header().resizeSection(1, 220)
        self.treewidget.header().resizeSection(2, 227)

    def setupDiscipline(self):
        self.currentdiscipline = self.currentDisciplineContext()
        if not self.currentdiscipline:
            LOGGER.warning("invalid user")
            return
        current_user = "%s: %s [%s]" % (
            self.currentdiscipline["username"],
            self.currentdiscipline["role"],
            self.currentdiscipline["privilege"],
        )
        r, g, b = self.currentdiscipline.get("color")
        self.label_user.setText(current_user)
        self.label_user.setStyleSheet(
            "color:rgb(%s, %s, %s); font: 87 10pt 'Arial Black';"
            % (r, g, b)
        )

    def currentDisciplineContext(self):
        value = os.getenv("PIPE-USER-DISCIPLINE")
        context = self.disp.searchDisciplineContext(value)
        if context:
            context["role"] = value
            context["username"] = os.getenv("PIPE-USER-NAME")
        return context

    def getNameParameters(self, value):
        contexts = utils.searchContext(
            self.categories, "type", value=value
        )
        if not contexts:
            for each in self.categories:
                if not each.get("children"):
                    continue
                contexts = utils.searchContext(
                    each["children"], "type", value="name"
                )
        if not contexts:
            return None
        parameters = contexts[0].get("parameter")
        if not parameters:
            return None
        context = self.getItemParameters(parameters)
        return context

    def getItemParameters(self, parameters):
        contexts = utils.searchContext(
            parameters, "name", value="name"
        )
        if not contexts:
            return None
        context = {
            "fontsize": contexts[0].get("fontsize"),
            "color": contexts[0].get("color"),
        }
        return context

    def selectCurrentContext(self, *args):
        current_item = args[0]

        self.groupbox.setVisible(True)
        self.setupAlignment()
        self.groupbox.setEntity(current_item.entity)
        self.groupbox.update()

    def setupCategories(self):
        self.proj.getProject()
        self.current_categories = self.proj.getProjectCategories()
        for context in self.current_categories:
            data = utils.searchContext(
                self.hierarchy, "name", value=context["name"]
            )

            if not data:
                LOGGER.warning(
                    'not found "%s" in the input configure'
                    % context["name"]
                )
                return

            input = data[0]
            path = self.vers.getLocalPath(context)
            root_treeitem = RootWidgetTreeItem(
                self.treewidget,
                name=context.get("name"),
                category=input.get("name"),
                fontsize=input.get("fontsize"),
                color=input.get("color"),
                path=path,
            )
            root_treeitem.setEntity(context)
            root_treeitem.setIDName(context.get("name"))
            root_treeitem.setInputs(input)

            root_treeitem.downloadbutton.clicked.connect(
                partial(self.download, root_treeitem, thread=True)
            )

    def itemExpanded(self, *args):
        current_item = args[0]

        print("entityType", current_item.entityType)

        if current_item.nullitem is None:
            LOGGER.warning("already loaded children")
            return

        if current_item.entityType == "Task":
            self.taskExpanded(current_item)
            return

        if current_item.entityType == "Kind":
            self.kindExpanded(current_item)
            return

        context = current_item.entity

        if not context["children"]:
            current_item.collapseItem()
            LOGGER.warning(
                "not find any children in the <%s> item"
                % current_item.name
            )
            return

        current_item.removeNullItem()

        children_inputs = current_item.inputs.get("children")

        self.progressbar.setMaximum(len(context["children"]))

        for index, child in enumerate(context["children"]):
            data = utils.searchContext(
                children_inputs, "type", value=child.entity_type
            )
            if not data:
                current_item.collapseItem()
                LOGGER.warning(
                    'not found children "%s" in the input configure'
                    % context["name"]
                )
                return

            input = data[0]

            header = self.proj.contextHeader(child)

            self.progressbar.setProgress(
                index, header, plane=True, error=False, thread=False
            )

            path = self.vers.getLocalPath(child)

            if child.entity_type == "AssetBuild":
                child_treeitem = AssetWidgetTreeItem(
                    current_item,
                    name=child["name"],
                    fontsize=input.get("fontsize"),
                    color=input.get("color"),
                    path=path,
                )

            elif child.entity_type == "Sequence":
                child_treeitem = SequenceWidgetTreeItem(
                    current_item,
                    name=child["name"],
                    fontsize=input.get("fontsize"),
                    color=input.get("color"),
                    path=path,
                )

            elif child.entity_type == "Shot":
                child_treeitem = ShotWidgetTreeItem(
                    current_item,
                    name=child["name"],
                    fontsize=input.get("fontsize"),
                    color=input.get("color"),
                    path=path,
                )

            elif child.entity_type == "Task":
                child_treeitem = TaskWidgetTreeItem(
                    current_item,
                    name=child["name"],
                    fontsize=input.get("fontsize"),
                    color=input.get("color"),
                    path=path,
                )
            else:
                child_treeitem = CommonWidgetTreeItem(
                    current_item,
                    name=child["name"],
                    fontsize=input.get("fontsize"),
                    color=input.get("color"),
                    path=path,
                )

            child_treeitem.setEntity(child)
            child_treeitem.setIDName(child.entity_type)
            child_treeitem.setInputs(input)

        self.progressbar.clear()

    def taskExpanded(self, *args):
        current_item = args[0]
        children_inputs = current_item.inputs.get("children")

        data = utils.searchContext(
            children_inputs, "type", value="Kind"
        )

        if not data:
            current_item.collapseItem()
            LOGGER.warning(
                'not found children "kind" in the input configure'
            )
            return

        input = data[0]
        current_item.removeNullItem()

        kinds = self.kind.get()

        self.progressbar.setMaximum(len(kinds))

        for index, each in enumerate(kinds):
            if not each.get("visible"):
                continue

            header = self.proj.contextHeader(current_item.entity)
            header = "%s|%s" % (header, each["name"])
            self.progressbar.setProgress(
                index, header, plane=True, error=False, thread=False
            )

            path = self.vers.getKindPath(
                current_item.entity, each["name"]
            )
            child_treeitem = KindsWidgetTreeItem(
                current_item,
                name=each["name"],
                color=each.get("color"),
                fontsize=each.get("fontsize"),
                path=path,
            )
            input["color"] = each.get("color")
            input["fontsize"] = each.get("fontsize")

            self.kind.setEntity(
                each["name"], parent=current_item.entity
            )

            child_treeitem.setEntity(self.kind.entity)
            child_treeitem.setIDName("kind")
            child_treeitem.setInputs(input)

        self.progressbar.clear()

    def kindExpanded(self, *args):
        current_item = args[0]
        children_inputs = current_item.inputs.get("children")
        data = utils.searchContext(
            children_inputs, "type", value="AssetVersion"
        )
        if not data:
            LOGGER.warning(
                'not found children "kind" in the input configure'
            )
            return

        input = data[0]

        versions = current_item.entity.get("children")

        if not versions:
            task = current_item.entity["parent"]
            name = current_item.name
            self.vers.authorization()
            versions = self.vers.searchKindVersions(
                taskid=task["id"], kind=name
            )

        if not versions:
            current_item.collapseItem()
            return

        current_item.removeNullItem()

        self.progressbar.setMaximum(len(versions))

        for index, each in enumerate(versions):

            header = self.proj.contextHeader(each)
            self.progressbar.setProgress(
                index, header, plane=True, error=False, thread=False
            )

            path, version = self.vers.versionPath(each)
            version_treeitem = VersionWidgetTreeItem(
                current_item,
                name=version,
                fontsize=input.get("fontsize"),
                color=input.get("color"),
                path=path,
            )
            version_treeitem.setEntity(each)
            version_treeitem.setIDName("version")
            version_treeitem.setInputs(input)

        self.progressbar.clear()

    def download(self, widgetitem, thread=False):
        self.downlad_state = threading.Condition()
        self.download_thread = threading.Thread(
            target=self._download, args=([widgetitem])
        )
        self.download_thread.daemon = True
        self.download_thread.start()

    def _download(self, widgetitem):
        import time

        widgetitem.setProgressbarMode()
        TIME_LIMIT = 100
        count = 0
        while count < TIME_LIMIT:
            count += 1
            time.sleep(0.2)
            widgetitem.progressbar.setValue(count)
        widgetitem.setDwonloadMode()


if __name__ == "__main__":
    os.environ["PROJECT-ID"] = "ad54bf94-ba83-41d3-899d-9ed3dc1ab699"
    os.environ["PROJECT-PATH"] = "Z:/projects/RAR"
    os.environ["PIPE-VERSION"] = "0.0.1"

    tag = 0
    if tag == 0:
        os.environ["PIPE-USER-NAME"] = "subingopi"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "Administrator"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"
    if tag == 1:
        os.environ["PIPE-USER-NAME"] = "leandra.rosa"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "72e1e0f0-a058-11e9-a359-d27cf242b68b"
    if tag == 2:
        os.environ["PIPE-USER-NAME"] = "tony.williams"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "ea90cf68-a057-11e9-8545-d27cf242b68b"

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {}
    window = Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
