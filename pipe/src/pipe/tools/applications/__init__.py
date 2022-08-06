import os
import sys
import importlib

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial


from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger
from pipe.core import console
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)
        LOGGER.info("applications - 0.0.1")
        self.title = (
            kwargs.get("title") or "Pipe Studio applications-0.0.1"
        )
        self.size = kwargs.get("size") or [640, 535]
        self.icon = kwargs.get("icon_size") or [128, 128]
        self.appn = studio.Applications()
        self.contexts = self.appn.get()

        self.setupUi()
        # temporary blocked self.setupConsole()

    def setupUi(self):
        self.setObjectName("mainwindow_applications")
        self.setWindowTitle(self.title)
        self.resize(self.size[0], self.size[1])
        self.verticallayout_applications = QtWidgets.QVBoxLayout(self)
        self.splitter_applications = QtWidgets.QSplitter(self)
        self.splitter_applications.setOrientation(QtCore.Qt.Vertical)
        self.verticallayout_applications.addWidget(
            self.splitter_applications
        )
        self.listwidget_applications = QtWidgets.QListWidget(self)
        self.listwidget_applications.setIconSize(
            QtCore.QSize(self.icon[0], self.icon[1])
        )
        qwidgets.setListIconWidget(self.listwidget_applications)
        self.listwidget_applications.itemDoubleClicked.connect(
            self.setCurrentApplication
        )
        self.splitter_applications.addWidget(
            self.listwidget_applications
        )
        self.textedit_console = QtWidgets.QTextEdit(self)
        self.textedit_console.hide()
        self.splitter_applications.addWidget(self.textedit_console)
        self.splitter_applications.setSizes([477, 100])

    def setupConsole(self, enable):
        cons = console.Connect()
        if enable:
            cons.stdout(
                self.textedit_console
            ).message_written.connect(
                self.textedit_console.insertPlainText
            )
        else:
            LOGGER.warning("work in progress")

    def setCurrentProject(self):
        self.listwidget_applications.clear()
        for each in self.contexts:
            iconpath = os.path.join(
                resources.getIconPath(), each.get("icon")
            )
            if not os.path.isfile(iconpath):
                iconpath = os.path.join(
                    resources.getIconPath(),
                    "unknown-applicationa.png",
                )
            item = qwidgets.addListWidgetItem(
                self.listwidget_applications,
                each.get("label"),
                statustip=each.get("name"),
                iconpath=iconpath,
                resize=[128, 128],
            )

    def setCurrentApplication(self, *args):
        current_application = args[0].statusTip()
        print("\n")
        if not current_application:
            raise ValueError(
                "not found in the applications configure data"
            )
        LOGGER.info(
            "loading studio-pipe applications %s, please wait"
            % current_application
        )

        print("current_application", current_application)
        self.appn.startLaunch(current_application, thread=True)
        return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window(parent=None)
    window.show()
    sys.exit(app.exec_())
