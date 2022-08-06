import os
import sys
import importlib

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)
CURRENT_PATH = os.path.dirname(__file__)


class Model(QtWidgets.QMainWindow):
    """
    :example
        import shiboken2
        from maya import OpenMayaUI
        from PySide2 import QtWidgets
        from modeling import validate
        reload(validate)
        qwidget = OpenMayaUI.MQtUtil.mainWindow()
        main_window = shiboken2.wrapInstance(int(qwidget), QtWidgets.QWidget)
        model = validate.Model(parent=main_window, step='model')
        model.show()
    """

    def __init__(self, parent=None, **kwargs):
        super(Model, self).__init__(parent)
        self.step = kwargs.get("step")
        self.title = (
            kwargs.get("title")
            or "Studio-Pipe %s Validation Tool -0.0.1" % self.step
        )
        self.wsize = kwargs.get("wsize") or [500, 340]

        self.iconpath = kwargs.get("iconpath")
        self.action_path = os.path.join(CURRENT_PATH, "actions.json")

        self.color = {True: [0, 229, 0], False: [255, 0, 0]}
        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.setup_ui()
        self.setup_icons()
        self.setup_actions()

        LOGGER.info(self.title)

    def setup_ui(self):
        self.setObjectName("mainwindow_validate")
        self.setWindowTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])
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

    def setup_icons(self):
        qwidgets.set_widget_icon(self, self.iconpath)

    @property
    def actions(self):
        data = resources.getData(self.action_path)
        return data["data"]

    def setup_actions(self):
        LOGGER.info("action path, %s" % self.action_path)
        self.treewidget.clear()
        for index, each in enumerate(self.actions):
            if not each.get("enable"):
                continue
            item = QtWidgets.QTreeWidgetItem(self.treewidget)
            item.setText(0, str(index + 1))
            item.setText(1, each["name"])
            button = QtWidgets.QPushButton(self)
            button.setText("validate")
            button.setMinimumSize(QtCore.QSize(100, 0))
            button.setMaximumSize(QtCore.QSize(100, 16777215))
            button.clicked.connect(
                partial(self.vaidate, item, each["action"])
            )
            self.treewidget.setItemWidget(item, 2, button)
        self.treewidget.header().resizeSection(0, 60)
        self.treewidget.header().resizeSection(1, 300)

    def vaidate(self, item, action):
        module = importlib.import_module(action)
        if sys.version_info[:2] >= (3, 4):
            importlib.reload(module)
        else:
            reload(module)
        valid, message, result = module.execute()
        qwidgets.set_itemforeground_color(item, 1, self.color[valid])
        self.textedit.clear()
        self.textedit.setTextColor(
            QtGui.QColor(
                self.color[valid][0],
                self.color[valid][1],
                self.color[valid][2],
            )
        )
        if result:
            self.textedit.append("result")
            for each in result:
                self.textedit.append("\t%s".expandtabs(6) % each)
        self.textedit.append("\n%s" % message)
        self.treewidget.clearSelection()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    kwargs = {"wsize": [500, 340], "step": "model"}
    window = Model(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
