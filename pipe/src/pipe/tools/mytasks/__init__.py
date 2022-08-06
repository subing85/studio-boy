import os
import sys
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
from pipe.tools.mytasks import setup
from pipe.tools.mytasks import stepwidgets

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.title = "Studio-Pipe Task Management Tool -0.0.1"
        self.titleicon = kwargs.get("titleicon") or [768, 144]
        self.projecticon = kwargs.get("showicon") or [256, 144]
        self.wsize = kwargs.get("wsize") or [1600, 940]
        self.pipe_version = os.getenv("PIPE-VERSION") or "unknown"
        self.iconpath = resources.getIconPath()
        self.browsepath = resources.getBrowsePath()

        self.tasks_items = dict()
        self.current_task = None
        self.stop_thread = False

        self.proj = studio.Project()
        self.disp = studio.Discipline()
        self.stps = studio.Steps()
        self.task = studio.Tasks()
        self.stus = studio.Status()
        self.vers = studio.Versions()
        self.comp = studio.Components()

        self.current_project = self.proj.getCurrentProject()

        setup.MAIN = self
        stepwidgets.MAIN = self

        self.setupUi()
        self.setupDefault()
        self.setupDiscipline()
        self.setupMenu()
        self.setupComponentMenu()
        self.setupIcons()

    def setupUi(self):
        self.setObjectName("mainwindow_launcher")
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

        self.horizontallayout_logo = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout_logo)

        self.button_logo = QtWidgets.QPushButton(self)
        self.button_logo.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.button_logo.setSizePolicy(sizePolicy)
        self.horizontallayout_logo.addWidget(self.button_logo)

        spacer_item = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout_logo.addItem(spacer_item)

        self.button_project = QtWidgets.QPushButton(self)
        self.button_project.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.button_project.setSizePolicy(sizePolicy)
        self.horizontallayout_logo.addWidget(self.button_project)

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.verticallayout.addWidget(self.splitter)

        self.groupbox_menu = QtWidgets.QGroupBox(self.splitter)
        self.groupbox_menu.setMaximumSize(QtCore.QSize(47, 16777215))

        self.verticallayout_menu = QtWidgets.QVBoxLayout(
            self.groupbox_menu
        )
        self.verticallayout_menu.setSpacing(10)
        self.verticallayout_menu.setContentsMargins(0, 0, 0, 0)

        self.button_filter = QtWidgets.QPushButton(self)
        self.button_filter.setFlat(True)
        self.button_filter.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu
        )
        self.button_filter.customContextMenuRequested.connect(
            self.contextMenu
        )
        self.verticallayout_menu.addWidget(self.button_filter)

        self.button_reload = QtWidgets.QPushButton(self)
        self.button_reload.setFlat(True)
        self.verticallayout_menu.addWidget(self.button_reload)

        spacer_item = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.verticallayout_menu.addItem(spacer_item)

        self.horizontallayout_progressbar = QtWidgets.QHBoxLayout()
        self.verticallayout_menu.addLayout(
            self.horizontallayout_progressbar
        )

        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setValue(0)
        self.progressbar.setTextVisible(False)
        self.progressbar.setOrientation(QtCore.Qt.Vertical)
        # self.progressbar.setInvertedAppearance(True)
        self.progressbar.setTextDirection(
            QtWidgets.QProgressBar.TopToBottom
        )
        self.progressbar.setStyleSheet(
            "QProgressBar {border: 1px;}"
            "QProgressBar::chunk {background-color: #ffaa00;height: 5px;margin: 2px;}"
        )
        self.horizontallayout_progressbar.addWidget(self.progressbar)

        self.treewidget_tasks = QtWidgets.QTreeWidget(self.splitter)
        self.treewidget_tasks.setHeaderHidden(True)
        self.treewidget_tasks.setColumnCount(2)
        self.treewidget_tasks.setStyleSheet("font: 12pt;")
        self.treewidget_tasks.setIconSize(QtCore.QSize(64, 64))
        self.treewidget_tasks.setAlternatingRowColors(True)

        self.treewidget = QtWidgets.QTreeWidget(self.splitter)
        self.treewidget.setStyleSheet("font: 12pt;")
        self.treewidget.setHeaderHidden(True)
        self.treewidget.setColumnCount(2)
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        self.treewidget.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu
        )
        self.treewidget.customContextMenuRequested.connect(
            self.componentContextMenu
        )

        self.groupbox = QtWidgets.QGroupBox(self.splitter)
        self.groupbox.setMaximumSize(QtCore.QSize(319, 16777215))

        self.verticalayout_group = QtWidgets.QVBoxLayout(
            self.groupbox
        )
        self.verticalayout_group.setSpacing(20)

        self.label_tag = QtWidgets.QLabel(self)
        self.label_tag.setStyleSheet(
            "background-color: #ffaa00;font: 75 12pt"
        )
        self.label_tag.setMinimumSize(QtCore.QSize(0, 30))

        self.verticalayout_group.addWidget(self.label_tag)

        self.horizontallayout_status = QtWidgets.QHBoxLayout()
        self.verticalayout_group.addLayout(
            self.horizontallayout_status
        )

        self.button_status = QtWidgets.QPushButton(self)
        self.button_status.setFlat(True)
        self.button_status.setMaximumSize(QtCore.QSize(128, 128))
        self.button_status.setMinimumSize(QtCore.QSize(128, 128))
        self.horizontallayout_status.addWidget(self.button_status)

        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setSpacing(6)
        self.verticalayout_group.addLayout(self.gridlayout)

        self.label_versions = QtWidgets.QLabel(self)
        self.label_versions.setText("Latest kind versions")
        self.label_versions.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.gridlayout.addWidget(self.label_versions, 0, 0, 1, 1)

        self.combobox_versions = QtWidgets.QComboBox(self)
        self.gridlayout.addWidget(self.combobox_versions, 0, 1, 1, 1)

        self.label_semanticversion = QtWidgets.QLabel(self)
        self.label_semanticversion.setText("Version Type")
        self.label_semanticversion.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.gridlayout.addWidget(
            self.label_semanticversion, 1, 0, 1, 1
        )

        self.combobox_semanticversion = QtWidgets.QComboBox(self)
        self.combobox_semanticversion.addItems(
            ["Major", "Minor", "Patch"]
        )
        self.gridlayout.addWidget(
            self.combobox_semanticversion, 1, 1, 1, 1
        )

        self.label_nextversion = QtWidgets.QLabel(self)
        self.label_nextversion.setText("Next version")
        self.label_nextversion.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.gridlayout.addWidget(self.label_nextversion, 2, 0, 1, 1)

        self.lineedit_nextversion = QtWidgets.QLineEdit(self)
        self.lineedit_nextversion.setEnabled(False)
        self.gridlayout.addWidget(
            self.lineedit_nextversion, 2, 1, 1, 1
        )

        self.label_comments = QtWidgets.QLabel(self)
        self.label_comments.setText("Comments")
        self.label_comments.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.gridlayout.addWidget(self.label_comments, 3, 0, 1, 1)

        self.textedit_comments = QtWidgets.QTextEdit(self)
        self.textedit_comments.setMinimumSize(QtCore.QSize(0, 100))
        self.textedit_comments.setMaximumSize(
            QtCore.QSize(16777215, 100)
        )
        self.gridlayout.addWidget(self.textedit_comments, 3, 1, 1, 1)

        self.button_start = QtWidgets.QPushButton(self)
        self.button_start.setText("Start")
        self.gridlayout.addWidget(self.button_start, 4, 1, 1, 1)

        self.button_submit = QtWidgets.QPushButton(self)
        self.button_submit.setText("Submit")
        self.gridlayout.addWidget(self.button_submit, 5, 1, 1, 1)

        self.button_decline = QtWidgets.QPushButton(self)
        self.button_decline.setText("Decline-Approval")
        self.gridlayout.addWidget(self.button_decline, 6, 1, 1, 1)

        self.button_approved = QtWidgets.QPushButton(self)
        self.button_approved.setText("Approved")
        self.gridlayout.addWidget(self.button_approved, 7, 1, 1, 1)

        self.button_publish = QtWidgets.QPushButton(self)
        self.button_publish.setText("Publish")
        self.gridlayout.addWidget(self.button_publish, 8, 1, 1, 1)

        self.button_deploy = QtWidgets.QPushButton(self)
        self.button_deploy.setText("Deploy-Submission")

        self.verticalayout_group.addWidget(self.button_deploy)

        spacer_item = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.verticalayout_group.addItem(spacer_item)

        self.button_reload.clicked.connect(self.reload)
        self.treewidget_tasks.itemClicked.connect(
            self.setupCurrentTask
        )

        self.button_start.clicked.connect(self.startTask)
        self.button_submit.clicked.connect(self.submitTask)
        self.button_deploy.clicked.connect(self.deployTask)
        self.button_decline.clicked.connect(self.declineApproval)
        self.button_approved.clicked.connect(self.approvedTask)
        self.button_publish.clicked.connect(self.publishTask)

        self.combobox_semanticversion.currentIndexChanged.connect(
            self.setupNextSemanticVersion
        )

    def setupIcons(self):
        qwidgets.setWidgetIcon(
            self, utils.findIconpath(prefix="mytasks")
        )
        qwidgets.setWidgetIcon(
            self.action_remove, utils.findIconpath(prefix="remove")
        )
        contexts = [
            {
                "widget": self.button_logo,
                "size": self.titleicon,
                "icon": utils.findIconpath(prefix="pipe-mytasks"),
            },
            {
                "widget": self.button_project,
                "size": self.projecticon,
                "icon": qwidgets.encodeIcon(
                    self.current_project["thumbnail_url"]["url"]
                ),
            },
            {
                "widget": self.button_filter,
                "size": [44, 44],
                "icon": utils.findIconpath(prefix="filter"),
            },
            {
                "widget": self.button_reload,
                "size": [44, 44],
                "icon": utils.findIconpath(prefix="reload"),
            },
        ]

        for context in contexts:
            qwidgets.imageToButton(
                context["widget"],
                context["size"][0],
                context["size"][1],
                locked=True,
                iconpath=context["icon"],
            )

    def setupDefault(self):
        self.splitter.setSizes([47, 403, 798, 319])
        self.label_version.setText(
            "PIPE - Package Version: %s" % self.pipe_version
        )
        self.progressbar.hide()
        self.hideUserWidgets()

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

    def contextMenu(self, point):
        self.filter_menu.exec_(self.button_filter.mapToGlobal(point))

    def setupMenu(self):
        self.filter_menu = QtWidgets.QMenu(self)
        self.filter_menu.setTitle("Filter")
        self.filter_menu.setTearOffEnabled(True)
        self.task_types = self.stps.getTasks(None)
        for each in self.task_types:
            action = QtWidgets.QAction(self)
            action.setText(each["name"])
            action.setCheckable(True)
            action.setChecked(False)
            self.filter_menu.addAction(action)
            action.triggered.connect(self.setupFilter)

    def setupComponentMenu(self):
        self.component_menu = QtWidgets.QMenu(self)
        self.component_menu.setTitle("Components")

        self.action_remove = QtWidgets.QAction(self)
        self.action_remove.setText("Remove-Component")
        self.component_menu.addAction(self.action_remove)
        self.action_remove.triggered.connect(
            self.removeComponentItems
        )

    def componentContextMenu(self, point):
        index = self.treewidget.indexAt(point)
        if not index.isValid():
            return
        self.component_menu.exec_(self.treewidget.mapToGlobal(point))

    def getFilters(self):
        actions = {}
        for each in self.filter_menu.actions():
            actions.setdefault(each.isChecked(), []).append(
                each.text()
            )
        return actions

    def cleanTaskItems(self):
        self.treewidget_tasks.clear()
        self.treewidget.clear()
        self.textedit_comments.clear()

    def setupFilter(self):
        if not self.currentdiscipline:
            LOGGER.warning("current user is invalid")
            return
        filters = self.getFilters()
        self.stop_thread = False
        if not filters.get(True):
            LOGGER.warning("not find any filter")
            return
        LOGGER.info("collecting your tasks, please wait")
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        tasks = self.task.getMyTasks(names=filters[True])
        QtWidgets.QApplication.restoreOverrideCursor()
        if not tasks:
            LOGGER.warning(
                "not assigned any task to the current user"
            )
            return
        self.stop_thread = True
        self.cleanTaskItems()
        setup.loadTasks(tasks, thread=True)

    def setProgress(self, thread):  # work in progress
        index = 0
        while thread.isAlive():
            self.progressbar.setMaximum(100 + (index + 1))
            self.progressbar.setValue(index)
            index += 1
        self.progressbar.setValue(100)

    def setupCurrentTask(self, *args):
        task_header = args[0].text(1)
        if task_header not in self.tasks_items:
            LOGGER.warning("invalid task selected")
            return
        taskid = self.tasks_items[task_header]
        self.current_task = self.task.currentTask(taskid)
        print("\n")
        LOGGER.info("Current Task ID: %s" % self.current_task["id"])
        LOGGER.info("Current Task : %s" % task_header)
        LOGGER.info(
            "Current Status : %s"
            % self.current_task["status"]["name"]
        )
        setup.updatePrivileges()

    def hideUserWidgets(self):
        widgets = stepwidgets.getAllWidgets()
        qwidgets.widgetVisibility(widgets, False)

    def setupStatusIcon(self, icon):
        if not icon:
            return
        self.button_status.show()
        iconpath = os.path.join(self.iconpath, "%s.png" % icon)
        qwidgets.imageToButton(
            self.button_status, 64, 64, locked=True, iconpath=iconpath
        )

    def getVersionsFromCombox(self):
        all_versions = []
        nulls = ["null", "none"]
        for i in range(self.combobox_versions.count()):
            item = self.combobox_versions.itemText(i)
            all_versions.append(item)
        if not all_versions:
            return None
        if all_versions[0].lower() in nulls:
            return None
        return all_versions

    def setupNextSemanticVersion(self):
        index = self.combobox_semanticversion.currentIndex()
        latest_versions = self.getVersionsFromCombox()
        if not latest_versions:
            next_version = self.vers.start_version
        else:
            next_version = self.vers.getNextVersion(
                latest_versions[0], index
            )
        self.lineedit_nextversion.setText(next_version)

    def setupComponents(self, components):
        for component in components:
            item = QtWidgets.QTreeWidgetItem(self.treewidget)
            qwidgets.setItemFont(item, 1, size=12, bold=True)
            button = qwidgets.createAddButton()
            item.setStatusTip(1, str(component))
            item.setText(1, component["display-name"])
            button.clicked.connect(
                partial(
                    self.browseComponent,
                    item,
                    component["name"],
                    component["formats"],
                    typed=component.get("type"),
                )
            )
            self.treewidget.setItemWidget(item, 0, button)
        self.treewidget.header().resizeSection(0, 50)

    def browseComponent(self, item, name, formats, typed=None):
        typed = typed or "path"
        if typed == "dirname":
            directory = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Browse your file to submit", self.browsepath
            )
            filepath = directory
        else:
            qformats = utils.formatsToQFormats(formats)
            filepath, format = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Browse your file to submit",
                self.browsepath,
                qformats,
            )
            directory = os.path.dirname(filepath)
        if not filepath:
            return
        directory = utils.setPathResolver(filepath)
        setup.setupComponentItems(
            item, typed, directory, formats=formats
        )
        self.browsepath = directory

    def removeComponentItems(self):
        context = setup.getSelectedComponentItems(self.treewidget)
        items = sum(context.values(), [])
        qwidgets.removeTreeWidgetItems(self.treewidget, items)

    def startTask(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        task, message = self.task.startMyTask(self.current_task["id"])
        if not task:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.current_task = task
        setup.updatePrivileges()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def submitTask(self):
        version_type = self.combobox_semanticversion.currentText()
        comments = self.textedit_comments.toPlainText()

        components = self.comp.collectFromWidget(
            self.current_task, self.treewidget
        )

        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        (
            task_context,
            version_context,
            message,
        ) = self.task.releaseKindTask(
            self.current_task["id"],
            "submit",
            version=version_type.lower(),
            path=None,
            components=components,
            comments=comments,
        )
        if not task_context:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.current_task = task_context
        setup.updatePrivileges()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def deployTask(self):
        versions = self.combobox_versions.currentText()
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        components = self.vers.downloadVersions(
            taskid=self.current_task["id"],
            kind="submit",
            versions=versions,
            progressbar=self.progressbar,
        )
        if not components:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "failed", QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def declineApproval(self):
        header = self.task.contextHeader(self.current_task)
        message = "%s \n%s \n%s" % (
            "Are you sure, you want to decline the approval?...",
            header,
            self.current_task["id"],
        )
        replay = QtWidgets.QMessageBox.question(
            self,
            "Question",
            message,
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if replay == QtWidgets.QMessageBox.No:
            LOGGER.warning("Abort the decline the approval!...")
            return
        versions = self.combobox_versions.currentText()
        comments = self.textedit_comments.toPlainText()
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        (
            task_context,
            version_context,
            message,
        ) = self.task.declineUserTask(
            self.current_task["id"],
            version=versions,
            comment=comments,
        )
        if message:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.current_task = task_context
        setup.updatePrivileges()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def approvedTask(self):
        versions = self.combobox_versions.currentText()
        comments = self.textedit_comments.toPlainText()
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        (
            task_context,
            version_context,
            message,
        ) = self.task.approvedUserTask(
            self.current_task["id"],
            version=versions,
            comment=comments,
        )
        if message:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.current_task = task_context
        setup.updatePrivileges()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def publishTask(self):
        version_type = self.combobox_semanticversion.currentText()
        comments = self.textedit_comments.toPlainText()

        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        (
            task_context,
            version_context,
            message,
        ) = self.task.releaseKindTask(
            self.current_task["id"],
            "publish",
            version=version_type.lower(),
            comments=comments,
        )

        if not task_context:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.current_task = task_context
        setup.updatePrivileges()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )

    def reload(self):
        self.setupFilter()


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
