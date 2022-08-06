import threading

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from common import resources
from pipe.core import logger
from apis.studio import Event
from pipe.utils import qwidgets
from pipe.widgets import ProgressBar

LOGGER = logger.getLogger(__name__)

import importlib

importlib.reload(qwidgets)


class Window(QtWidgets.QMainWindow):

    taskType = None

    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [400, 190])

        LOGGER.info("current task type, %s" % self.taskType)

        if not self.taskType:
            raise Exception("invalid task type name <%s>" % self.task)

        self.input = resources.getConfigData("bake", self.taskType)
        if not self.input:
            raise Exception(
                "invalid task type inputs <%s>" % self.taskType
            )

        self.title = "%s Bake" % self.input["label"]

        self.taskList = dict()
        self.currentTask = None

        self.linkHistory = dict()
        self.inputLink = dict()
        self.outputLinks = dict()

        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.setupUi()

        self.setupTasks()
        LOGGER.info(self.title)

    def setupUi(self):
        self.resize(self.wsize[0], self.wsize[1])
        self.setWindowTitle(self.title)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.gridlayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setVerticalSpacing(0)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(self.alignright)
        self.label.setText("Tasks")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.setIconSize(QtCore.QSize(32, 32))
        self.combobox.setMinimumSize(QtCore.QSize(300, 0))
        self.gridlayout.addWidget(self.combobox, 0, 1, 1, 1)

        for index, item in enumerate(self.input["items"]):

            if item.get("type") == "enum":
                horizontallayout = QtWidgets.QHBoxLayout()
                horizontallayout.setContentsMargins(0, 0, 0, 0)
                label = QtWidgets.QLabel(self)
                label.setText(item.get("label"))
                horizontallayout.addWidget(label)
                self.itemwidget = QtWidgets.QComboBox(self)
                horizontallayout.addWidget(self.itemwidget)
                self.gridlayout.addLayout(
                    horizontallayout, index + 1, 1, 1, 1
                )

            else:
                self.itemwidget = QtWidgets.QPushButton(self)
                self.itemwidget.setText(item["label"])
                self.itemwidget.setMaximumSize(
                    QtCore.QSize(16777215, 24)
                )

                self.itemwidget.clicked.connect(
                    partial(self.trigger, item["event"])
                )
                self.itemwidget.setStyleSheet("text-align: left;")

                qwidgets.imageToButton(
                    self.itemwidget,
                    self.iconsize[0],
                    self.iconsize[1],
                    locked=False,
                    iconpath=resources.getIcon(item.get("icon")),
                )
                self.gridlayout.addWidget(
                    self.itemwidget, index + 1, 1, 1, 1
                )

            if item.get("link"):
                context = {
                    "widget": self.itemwidget,
                    "event": item["event"],
                }
                self.linkHistory[item["name"]] = context

        self.progressbar = ProgressBar(
            self, visible=True, plane=False
        )

        self.gridlayout.addWidget(
            self.progressbar, index + 2, 1, 1, 1
        )

        self.pipeButton = qwidgets.createPipeLogButton(
            size=6, iconsize=24
        )
        self.gridlayout.addWidget(self.pipeButton, index + 3, 1, 1, 1)
        self.combobox.currentIndexChanged.connect(self.setCurrentTask)

    def setupTasks(self):
        context = utils.searchContext(
            self.input["task"], "name", value="get"
        )
        item = context[0]["event"]

        self.inputLink = context[0].get("link")
        inputs = {
            "taskType": [self.taskType],
            "widget": self.combobox,
            # "progressbar": self.progressbar,
        }

        self.task_state = threading.Condition()
        self.task_thread = threading.Thread(
            target=self._setupTasks, args=([item, inputs])
        )
        self.task_thread.daemon = True
        self.task_thread.start()

    def _setupTasks(self, item, inputs):
        evnt = Event(item)
        evnt.initialize(input=inputs)
        self.taskList = evnt.output

    def setCurrentTask(self, *args):
        if self.task_thread.isAlive():
            LOGGER.warning("please wait, unit load all tasks")
            return
        if not self.taskList:
            LOGGER.warning("could not found current task")
            return
        header = self.combobox.currentText()
        if header == "Select your task!..." or not header:
            return
        if header not in self.taskList:
            LOGGER.warning(
                "could not found such task called %s" % header
            )
            return
        self.currentTask = self.taskList[header]

        self.setupLink()

    def setupLink(self):
        if not self.inputLink:
            return
        if self.inputLink not in self.linkHistory:
            return
        context = self.linkHistory[self.inputLink]

        evnt = Event(context["event"])
        inputs = {
            "task": self.currentTask,
            "widget": context.get("widget"),
        }
        evnt.initialize(input=inputs)
        self.outputLinks = evnt.output
        self.outputLinks["widget"] = context.get("widget")

    def trigger(self, item):
        if self.task_thread.isAlive():
            LOGGER.warning("please wait, unit load all tasks")
            return
        if not self.currentTask:
            LOGGER.warning(
                "could not found current task, please wait unit load tasks"
            )
            return
        LOGGER.info("current task, %s" % self.currentTask)

        input = {
            "task": self.currentTask,
            "taskType": self.taskType,
            "outputLinks": self.outputLinks,
        }

        evnt = Event(item)

        evnt.initialize(input=input)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {"taskType": "Modeling"}
    window = Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
