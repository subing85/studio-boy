import os
import sys
import importlib

from PySide2 import QtWidgets
from functools import partial


from pipe.core import logger
from toolkits import resources
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)


class Menu(QtWidgets.QMenu):
    def __init__(self, parent, **kwargs):
        super(Menu, self).__init__(parent)

        self.name = kwargs.get("name")
        self.parent = parent
        self.title = "Studio-Pipe"
        self.iconpath = resources.getIconPath()

        self.setupUi()

    def setupUi(self):
        self.action_reload = QtWidgets.QAction(None)
        self.action_reload.setText("Reload")
        self.setActionIcon(self.action_reload, icon="reload")
        # self.action_reload.triggered.connect(self.reloadAction)

    def createMenu(self, actions):
        self.setTitle(self.title)
        self.setObjectName(self.name)

        for each in actions:
            for step, modules in each.items():
                menu = QtWidgets.QMenu(self)
                menu.setTitle(step)
                self.setActionIcon(menu, icon=step.lower())
                self.addAction(menu.menuAction())
                modules = list(sorted(modules, key=lambda k: k.ORDER))
                for module in modules:
                    action = QtWidgets.QAction(menu)
                    action.setText(module.NAME)
                    menu.addAction(action)
                    self.setActionIcon(action, module=module)
                    action.triggered.connect(
                        partial(self.executeAction, module)
                    )
        self.addAction(self.action_reload)
        if isinstance(self.parent, QtWidgets.QMenuBar):
            self.parent.addAction(self.menuAction())

    def setActionIcon(self, action, module=None, icon=None):
        iconpath = self.findIconPath(module=module, icon=icon)
        qwidgets.setWidgetIcon(action, iconpath)

    def findIconPath(self, module=None, icon=None):
        if module:
            if hasattr(module, "ICON"):
                icon = module.ICON
        if not icon:
            iconpath = os.path.join(self.iconpath, "unknown.png")
            return iconpath
        iconpath = os.path.join(self.iconpath, "%s.png" % icon)
        if not os.path.isfile(iconpath):
            iconpath = os.path.join(self.iconpath, "unknown.png")
            return iconpath
        return iconpath

    def _removeWidgets(self, widgets, close=False):
        if not widgets:
            return
        for each in widgets:
            if close:
                each.close()
            else:
                each.deleteLater()

    def executeAction(self, module):
        if not module:
            LOGGER.warning("invalid toolkit package")
            return
        try:
            result = module.execute()
        except Exception as error:
            LOGGER.warning("failed,  %s" % str(error))

    def deleteMenu(self):
        if not self.parent:
            return
        children = self.parent.findChildren(
            QtWidgets.QMenu, self.name
        )
        self._removeWidgets(children)
