import os
import sys
import shiboken2

try:
    from maya import OpenMayaUI
except:
    pass

from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe.core import logger
from toolkits import resources
from toolkits.core.menu import Menu

from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)

try:
    SWIG = int(OpenMayaUI.MQtUtil.mainWindow())
    MQ_WIDGET = shiboken2.wrapInstance(SWIG, QtWidgets.QWidget)
except:
    pass


class Connect(object):
    def __init__(self, **kwargs):
        super(Connect, self).__init__(**kwargs)

        self.name = kwargs.get("name", "menu_studio_pipe")
        self.buttonName = "button_studio_pipe"
        self.displayname = "Studio-Pipe"
        self.iconpath = resources.getIconPath()
        self.browser_window = None

        # self.mmenu = menu.Connect(parent=self.parent, name=self.name)

    @property
    def path(self):
        dirname = os.path.dirname(os.path.dirname(__file__))
        _path = os.path.join(dirname, os.getenv("MAYA_VERSION"))
        return _path

    @property
    def packages(self):
        packages = resources.getPackages(self.path)
        context = {}
        for each in packages:
            loc = each.LOCATION.split("/")
            context.setdefault(loc[0], []).append(each)
        return context

    @property
    def menuList(self):
        input_context = resources.getInputData("menu", enable=False)
        context = [each["display-name"] for each in input_context]
        return context

    def actions(self):
        context = []
        for each in self.menuList:
            if each not in self.packages:
                continue
            module = {each: self.packages[each]}
            context.append(module)
        return context

    def mayaMenuBar(self):
        menubar = MQ_WIDGET.findChild(QtWidgets.QMenuBar)
        return menubar

    def mayaButtonLayout(self):
        layout = MQ_WIDGET.findChild(QtWidgets.QLayout, "flowLayout2")
        return layout

    def mayaTableWidget(self):
        channel_box = MQ_WIDGET.findChild(
            QtWidgets.QWidget, "ChannelBoxLayerEditor"
        )
        tabwidget = channel_box.parent().parent()
        return tabwidget

    def pipeMenu(self):
        menubar = MQ_WIDGET.findChildren(QtWidgets.QMenu, self.name)
        return menubar

    def pipeButton(self):
        button_bar = MQ_WIDGET.findChildren(
            QtWidgets.QPushButton, self.buttonName
        )
        return button_bar

    def reloadAction(self):
        from test import utils

        utils.checkPackages()
        self.create()

    def deletePipeButton(self):
        for each in self.pipeButton():
            each.deleteLater()

    def create(self):
        actions = self.actions()
        self.createPipeMenu(actions=actions)
        self.createPipeButton(actions=actions)

    def createPipeMenu(self, actions=None):
        actions = actions or self.actions()
        menubar = self.mayaMenuBar()
        mn = Menu(menubar, name=self.name)
        mn.deleteMenu()
        mn.createMenu(actions)
        mn.action_reload.triggered.connect(self.reloadAction)

    def createPipeButton(self, actions=None):
        actions = actions or self.actions()
        mn = Menu(None, name=self.name)
        mn.deleteMenu()
        mn.createMenu(actions)
        mn.action_reload.triggered.connect(self.reloadAction)
        self.deletePipeButton()
        button = self.craeteButton(self.mayaButtonLayout())
        button.customContextMenuRequested.connect(
            partial(self.context_menu, mn, button)
        )
        button.clicked.connect(self.pipeTool)

    def context_menu(self, menu, widget, point):
        menu.exec_(widget.mapToGlobal(point))

    def craeteButton(self, layout):
        # self.removeWidgets(self.pipeButton())
        button = QtWidgets.QPushButton()
        button.setObjectName(self.buttonName)
        button.setFlat(True)
        button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        iconpath = os.path.join(self.iconpath, "pipe-button.png")
        if not os.path.isfile(iconpath):
            iconpath = os.path.join(self.iconpath, "unknown.png")
        qwidgets.imageToButton(button, 36, 36, iconpath, locked=True)
        layout.addWidget(button)
        return button

    def pipeTool(self):
        browser_tabs = self.hasPipeTool()
        if browser_tabs:
            replay = QtWidgets.QMessageBox.question(
                MQ_WIDGET,
                "Question",
                "Are you sure, you want to close the Studio-Pipe Browser?",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No,
            )
            if replay == QtWidgets.QMessageBox.No:
                LOGGER.warning("Abort close Studio-Pipe Browser!...")
                return

            self.removeWidgets(browser_tabs)
            LOGGER.info("removed Studio-Pipe Button from maya.")
            return
        LOGGER.info(
            "connecting to Studio-Pipe Button, please wait!..."
        )
        table_widget = self.mayaTableWidget()
        tab_browser = QtWidgets.QWidget()
        tab_browser.setObjectName("tab_studiopipe")
        table_widget.addTab(tab_browser, "Studio-Pipe")

        # =============================================================
        # from pipe.tools import browser
        # self.browser_window = browser.Maya(parent=MQ_WIDGET)
        # verticallayout = QtWidgets.QVBoxLayout(tab_browser)
        # verticallayout.setContentsMargins(0, 0, 0, 0)
        # verticallayout.addWidget(self.browser_window.centralwidget)
        # =============================================================

    def hasPipeTool(self):
        browser_tab = MQ_WIDGET.findChildren(
            QtWidgets.QWidget, "tab_studiopipe"
        )
        return browser_tab
