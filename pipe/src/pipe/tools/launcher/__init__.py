# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:16:Sunday-12:45:11:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core launcher tool.

import os
import webbrowser

from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger

# from pipe.tools import tasks
# from pipe.tools import packages
from pipe.utils import qwidgets
from pipe.tools import applications
from pipe.widgets import ProjectList

LOGGER = logger.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)
        self.title = (
            kwargs.get("title") or "Studio-Pipe launcher -0.0.1"
        )
        self.size = kwargs.get("size") or [640, 535]
        self.projecticon = [
            256,
            144,
        ]
        self.titleicon = kwargs.get("titleicon") or [768, 144]
        self.version = os.getenv("PIPE-VERSION") or "unknown"
        self.user = os.getenv("PIPE-USER-NAME") or None
        self.discipline = os.getenv("PIPE-USER-DISCIPLINE") or None
        self.iconpath = resources.getIconPath()
        self.project_contexts = []

        self.proj = studio.Project()
        self.lang = studio.Language()
        self.disp = studio.Discipline()
        self.apcw = applications.Window()

        self.setupUi()
        self.setupMenu()
        self.setupIcons()
        self.setupDiscipline()
        self.setupLanguage()
        self.setupProjects()
        self.setupEntities()

        LOGGER.info(self.title)

    def setupUi(self):
        self.setObjectName("mainwindow_launcher")
        self.setWindowTitle(self.title)
        self.resize(self.size[0], self.size[1])
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticallayout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )
        self.verticallayout.setSpacing(0)
        self.verticallayout.setContentsMargins(5, 5, 5, 5)
        self.groupbox = QtWidgets.QGroupBox(self)
        self.verticallayout.addWidget(self.groupbox)
        self.verticallayout_group = QtWidgets.QVBoxLayout(
            self.groupbox
        )
        self.verticallayout_group.setSpacing(5)
        self.verticallayout_group.setContentsMargins(5, 5, 5, 5)
        self.horizontallayout_language = QtWidgets.QHBoxLayout()
        self.horizontallayout_language.setContentsMargins(2, 2, 2, 2)
        self.verticallayout_group.addLayout(
            self.horizontallayout_language
        )
        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setAlignment(
            QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter
        )
        self.horizontallayout_language.addWidget(self.label_user)
        spaceritem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout_language.addItem(spaceritem)
        self.label_version = QtWidgets.QLabel(self)
        self.label_version.setText(
            "PIPE - Package Version: %s" % self.version
        )
        self.label_version.setAlignment(
            QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter
        )
        self.horizontallayout_language.addWidget(self.label_version)
        self.label_language = QtWidgets.QLabel(self)
        self.label_language.setText("Language")
        self.label_language.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.horizontallayout_language.addWidget(self.label_language)
        self.combobox_language = QtWidgets.QComboBox(self)
        self.combobox_language.currentIndexChanged.connect(
            self.setLanguage
        )
        # self.combobox_language.setEnabled(False)
        self.horizontallayout_language.addWidget(
            self.combobox_language
        )
        self.line_up = QtWidgets.QFrame(self.groupbox)
        self.line_up.setFrameShape(QtWidgets.QFrame.HLine)
        self.verticallayout_group.addWidget(self.line_up)

        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setContentsMargins(2, 2, 2, 2)
        self.verticallayout_group.addLayout(self.horizontallayout)
        self.button_logo = QtWidgets.QPushButton(self.groupbox)
        self.button_logo.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.button_logo.setSizePolicy(sizePolicy)
        self.horizontallayout.addWidget(self.button_logo)
        spaceritem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout.addItem(spaceritem)
        self.button_project = QtWidgets.QPushButton(self.groupbox)
        self.button_project.setFlat(True)
        self.horizontallayout.addWidget(self.button_project)
        self.line = QtWidgets.QFrame(self.groupbox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.verticallayout_group.addWidget(self.line)
        self.horizontallayout_pipe = QtWidgets.QHBoxLayout()
        self.verticallayout_group.addLayout(
            self.horizontallayout_pipe
        )

        self.listwidget_projects = ProjectList(
            self, iconsize=self.projecticon
        )
        self.horizontallayout_pipe.addWidget(self.listwidget_projects)

        self.listwidget_projects.itemClicked.connect(
            self.setCurrentProject
        )

        self.tabwidget = QtWidgets.QTabWidget(self)
        self.horizontallayout_pipe.addWidget(self.tabwidget)
        self.tab_applications = QtWidgets.QWidget()
        self.tabwidget.addTab(self.tab_applications, "Applications")
        self.horizontallayout_applications = QtWidgets.QHBoxLayout(
            self.tab_applications
        )

    def setupMenu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menu_create = QtWidgets.QMenu(self.menubar)
        self.menu_create.setTitle("Create")
        self.menubar.addAction(self.menu_create.menuAction())

        self.action_project = QtWidgets.QAction(self)
        self.action_project.setObjectName("action_project")
        self.action_project.setText("Create-Project")
        self.action_project.setEnabled(self.privilege)
        self.action_project.triggered.connect(self.createProject)
        self.menu_create.addAction(self.action_project)

        self.action_tasks = QtWidgets.QAction(self)
        self.action_tasks.setObjectName("action_tasks")
        self.action_tasks.setText("Create-Task")
        self.action_tasks.setEnabled(self.privilege)
        self.action_tasks.triggered.connect(self.createTask)
        self.menu_create.addAction(self.action_tasks)

        self.action_package = QtWidgets.QAction(self)
        self.action_package.setObjectName("action_packages")
        self.action_package.setText("Package-Release")
        self.action_package.setEnabled(self.privilege)
        self.action_package.setVisible(False)
        self.action_package.triggered.connect(self.packageRelease)
        self.menu_create.addAction(self.action_package)

        self.action_refresh = QtWidgets.QAction(self)
        self.action_refresh.setObjectName("action_refresh")
        self.action_refresh.setText("Refresh")
        self.action_refresh.triggered.connect(self.refresh)
        self.menu_create.addAction(self.action_refresh)

        self.action_exit = QtWidgets.QAction(self)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setText("Exit")
        self.action_exit.triggered.connect(self.close)
        self.menu_create.addAction(self.action_exit)

        self.menu_edit = QtWidgets.QMenu(self.menubar)
        self.menu_edit.setTitle("Edit")
        self.menubar.addAction(self.menu_edit.menuAction())

        self.action_console = QtWidgets.QAction(self)
        self.action_console.setObjectName("action_console")
        self.action_console.setText("Console")
        self.action_console.setCheckable(True)
        self.action_console.triggered.connect(self.setActiveConsole)
        self.menu_edit.addAction(self.action_console)

        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setTitle("Help")
        self.menubar.addAction(self.menu_help.menuAction())

        self.action_about = QtWidgets.QAction(self)
        self.action_about.setObjectName("action_about")
        self.action_about.setText("About")
        self.action_about.triggered.connect(self.about)
        self.menu_help.addAction(self.action_about)

    def setupIcons(self):
        widgets = [
            each for each in self.findChildren(QtWidgets.QAction)
        ]
        widgets.append(self)

        qwidgets.setWidgetsIcons(widgets)
        qwidgets.imageToButton(
            self.button_logo,
            self.titleicon[0],
            self.titleicon[1],
            locked=True,
            iconpath=utils.findIconpath("pipe-launcher"),
        )
        iconpath = os.path.join(self.iconpath, "unknown-project.png")
        qwidgets.imageToButton(
            self.button_project,
            self.projecticon[0],
            self.projecticon[1],
            locked=True,
            iconpath=iconpath,
        )

    def setupDefault(self):
        self.apcw.setCurrentProject()

    def currentDiscipline(self):
        value = os.getenv("PIPE-USER-DISCIPLINE")
        context = self.disp.searchDisciplineContext(value)
        return context

    def setupDiscipline(self):
        current_user = "unknown user"
        r, g, b = [255, 0, 0]
        if current_user:
            context = self.currentDiscipline()
            current_user = "%s: %s" % (self.discipline, self.user)
            r, g, b = context.get("color")
        self.label_user.setText(current_user)
        self.label_user.setStyleSheet(
            "color:rgb(%s, %s, %s); font: 87 8pt 'Arial Black';"
            % (r, g, b)
        )

    @property
    def privilege(self):
        discipline = self.currentDiscipline()
        if not discipline:
            return False
        if not discipline.get("privilege"):
            return False
        if discipline["privilege"] == "super-user":
            return True
        return False

    def setupLanguage(self):
        contexts = self.lang.get()
        for each in contexts:
            self.combobox_language.addItem(each["display-name"])

    def setupProjects(self):
        self.listwidget_projects.clear()
        self.project_contexts = self.proj.getAllProjects()
        for each in self.project_contexts:
            iconpath = self.projectIconPath(each)
            item = qwidgets.addListWidgetItem(
                self.listwidget_projects,
                each["name"],
                iconpath=iconpath,
            )
        return

    def projectIconPath(self, project):
        iconpath = os.path.join(self.iconpath, "unknown-project.png")
        if project.get("thumbnail_url"):
            if project["thumbnail_url"].get("url"):
                iconpath = project["thumbnail_url"]["url"]
        return iconpath

    def setupEntities(self):
        self.horizontallayout_applications.addWidget(
            self.apcw.splitter_applications
        )

    def setCurrentProject(self, *args):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        project_name = args[0].text()
        current_project = self.proj._setProject(project_name)
        iconpath = self.projectIconPath(current_project)
        iconpath = qwidgets.encodeIcon(iconpath)
        qwidgets.imageToButton(
            self.button_project,
            self.projecticon[0],
            self.projecticon[1],
            locked=True,
            iconpath=iconpath,
        )
        self.setupDefault()
        self.proj.getProject()
        QtWidgets.QApplication.restoreOverrideCursor()

    def setLanguage(self, *args):
        language = self.combobox_language.currentText()
        self.lang.setLanguage(language, key="display-name")
        self.lang.getLanguage(language, key="display-name")

    def setActiveConsole(self):
        enable = self.action_console.isChecked()
        self.apcw.textedit_console.show()
        self.apcw.setupConsole(enable)

    def createProject(self):
        command = "pipe launch project"
        utils.executeCommand(command)

    def createTask(self):
        command = "pipe launch tasks"
        utils.executeCommand(command)

    def packageRelease(self):
        command = "pipe launch packages"
        utils.executeCommand(command)

    def refresh(self):
        self.setupProjects()
        self.apcw.listwidget_applications.clear()

    def about(self):
        toolkits = resources.getSubinsToolkits()
        webbrowser.open(toolkits)
        LOGGER.info(toolkits)


if __name__ == "__main__":
    import sys

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

    os.environ[
        "RESOURCE-PATH"
    ] = "E:/venture/source_code/studio-pipe/devkit/pipeline/resources"
    os.environ[
        "TEMP-APPS-ENVS"
    ] = "C:/Users/sid/AppData/Local/Temp/pipe-app-envs.bat"

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {}
    window = Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
