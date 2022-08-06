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

LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Window(QtWidgets.QMainWindow):

    taskType = None

    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [500, 340])

        LOGGER.info("current task type, %s" % self.taskType)

        if not self.taskType:
            raise Exception("invalid task type name <%s>" % self.task)
        self.input = resources.getConfigData(
            "validate", self.taskType
        )

        if not self.input:
            raise Exception(
                "invalid task type inputs <%s>" % self.taskType
            )

        self.valid = False

        self.color = {
            None: [200, 200, 200],  # white
            True: [0, 229, 0],  # Green
            False: [255, 0, 0],  # Red
        }

        self.typed = {
            None: "\u2714",
            True: "\u2714",
            False: "\u2715",
        }
        self.history = dict()

        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.setupUi()
        self.setupActions()

    def setupUi(self):
        self.resize(self.wsize[0], self.wsize[1])
        self.setWindowTitle("%s Validate" % self.input["label"])
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.verticalLayout.addWidget(self.splitter)
        self.treewidget = QtWidgets.QTreeWidget(self)
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setHeaderHidden(True)
        self.treewidget.setColumnCount(3)
        self.splitter.addWidget(self.treewidget)
        self.textedit = QtWidgets.QTextEdit(self)
        self.splitter.addWidget(self.textedit)
        self.splitter.setSizes([167, 83])

    def setupActions(self):

        if not self.input:
            LOGGER.warning(
                "invalid input config <%s>" % self.taskType
            )
            return

        self.treewidget.clear()
        for index, each in enumerate(self.input["items"]):
            if not each.get("enable"):
                continue
            item = QtWidgets.QTreeWidgetItem(self.treewidget)
            item.setText(0, str(index + 1))
            item.setText(2, each["label"])
            qwidgets.setItemforegroundColor(item, 1, self.color[None])

            r, g, b = self.color[None]
            colorname = QtGui.QColor(r, g, b).name()

            button = qwidgets.createValidateButton(
                size=12, bgcolor=colorname
            )

            button.clicked.connect(
                partial(
                    self.trigger, item, each["check"], each.get("fix")
                )
            )

            self.treewidget.setItemWidget(item, 1, button)

        self.treewidget.header().resizeSection(0, 60)
        self.treewidget.header().resizeSection(1, 30)

    def trigger(self, item, check, fix):

        input = {"taskType": self.taskType}

        current = check
        if item in self.history:
            vaild = self.history[item].context["valid"]
            current = fix if vaild is False else check

        event = Event(current)
        event.initialize(input=input)
        valid = self.setupReaction(item, event.output)

        event.setContext("valid", valid)
        self.history.setdefault(item, event)

    def setupReaction(self, item, context):
        self.textedit.append("Header - <%s>" % self.taskType)

        if not context:
            context = {
                "nodes": list(),
                "message": "invalid python class",
            }

        for each in context["nodes"]:
            self.textedit.append("\t%s".expandtabs(6) % str(each))
        self.textedit.append("\n%s\n\n" % context["message"])

        self.treewidget.clearSelection()

        valid = context.get("valid")
        color = (
            self.color[valid]
            if valid in self.color
            else self.color[None]
        )

        qwidgets.setItemforegroundColor(item, 2, color)

        colorname = QtGui.QColor(color[0], color[1], color[2])

        button = self.treewidget.itemWidget(item, 1)
        qwidgets.setButtonProperty(
            button,
            typed=self.typed[valid],
            size=12,
            bgcolor=colorname.name(),
        )

        return valid


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {"taskType": "modeling"}
    window = Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
