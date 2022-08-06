import os
import sys
import json
import warnings

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import core
from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.title = (
            kwargs.get("title")
            or "Studio-Pipe Package Release - 0.0.1"
        )
        self.wsize = kwargs.get("wsize") or [500, 500]
        self.iconpath = resources.getIconPath()

        self.blue_color = (0, 0, 255)
        self.black_color = (0, 0, 0)
        self.green_color = (0, 148, 0)
        self.red_color = (255, 0, 0)

        self.pack = core.Packages()
        self.pack.authorization()

        self.setupUi()
        self.setupIcons()

        LOGGER.info(self.title)

    def setupUi(self):
        self.setObjectName("mainwindow_packages")
        self.setWindowTitle(self.title)
        self.resize(300, 420)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticallayout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )
        self.treewidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treewidget.setColumnCount(2)
        self.treewidget.setHeaderHidden(True)
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.treewidget.itemClicked.connect(self.isItemChecked)
        self.verticallayout.addWidget(self.treewidget)
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout)
        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setText("Reload")
        self.button_load.clicked.connect(self.reloads)
        self.horizontallayout.addWidget(self.button_load)
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout.addItem(spacerItem)
        self.button_release = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.button_release.setText("Release")
        self.button_release.clicked.connect(self.release)
        self.horizontallayout.addWidget(self.button_release)
        self.button_live = QtWidgets.QPushButton(self.centralwidget)
        self.button_live.setText("Make it Live")
        self.button_live.clicked.connect(self.live)
        self.horizontallayout.addWidget(self.button_live)

    def setupIcons(self):
        widgets = [self]
        qwidgets.set_widgets_icons(widgets)

    def setupPack(self):
        contexts = self.pack.config_context()
        if not contexts:
            LOGGER.warning("invalid config data")
            return
        contexts = sorted(contexts, key=lambda k: (k.get("order")))
        self.treewidget.clear()
        for context in contexts:
            item = QtWidgets.QTreeWidgetItem(self.treewidget)
            item.setText(0, str(context["order"]))
            item.setText(1, context["name"])
            qwidgets.set_item_font(item, 1, size=12, bold=False)
            self.setupTags(
                item, context["name"], version=context.get("version")
            )  #
            LOGGER.info(
                "package-%s, version-%s"
                % (context["name"], context.get("version"))
            )
        self.treewidget.header().resizeSection(0, 60)

    def setupTags(self, parent, project, version=None):
        project = self.pack.find_project(project, group=None)
        if not project:
            return
        tages = self.pack.get_tags(project)
        for tage in tages:
            item = QtWidgets.QTreeWidgetItem(parent)
            item.setText(1, tage.name)
            item.setCheckState(1, QtCore.Qt.Unchecked)
            color, tooltip = self.red_color, "new"
            has_project = self.pack.has_project(
                project.name, tag=tage.name
            )
            if has_project:
                color, tooltip = self.blue_color, "new"
            if tage.name == version:
                color, tooltip = self.green_color, "live"
            qwidgets.setItemforegroundColor(item, 1, color)
            item.setToolTip(1, tooltip)

    def isItemChecked(self, *args):
        item = args[0]
        parent = item.parent()
        if not parent:
            return
        for index in range(parent.childCount()):
            child = parent.child(index)
            if item == child:
                continue
            child.setCheckState(1, QtCore.Qt.Unchecked)
        if item.toolTip(1) == "live":
            item.setCheckState(1, QtCore.Qt.Unchecked)
            LOGGER.warning(
                "this is the current live version <%s>" % item.text(1)
            )

    def collectProjects(self):
        widget_item = self.treewidget.invisibleRootItem()
        projects = {}
        for index in range(widget_item.childCount()):
            parent = widget_item.child(index)
            for x in range(parent.childCount()):
                child = parent.child(x)
                if not child.checkState(1):
                    continue
                projects.setdefault(parent.text(1), child.text(1))
        return projects

    def reloads(self):
        self.setupPack()

    def release(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        projects = self.collectProjects()
        if not projects:
            LOGGER.warning("versions are not selected")
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        for project, tag in projects.items():
            self.pack.clone_project(project, tag=tag)
        self.setupPack()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "release completed!...",
            QtWidgets.QMessageBox.Ok,
        )

    def live(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        projects = self.collectProjects()
        if not projects:
            LOGGER.warning("versions are not selected")
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.pack.update_config(projects)
        self.setupPack()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "make live completed!...",
            QtWidgets.QMessageBox.Ok,
        )


if __name__ == "__main__":
    pass
