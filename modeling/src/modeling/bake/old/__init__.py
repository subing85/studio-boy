from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


from pipe import resources

from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class BModel(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(BModel, self).__init__(parent)

        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.setupUi()

    def setupUi(self):
        self.resize(360, 190)
        self.setWindowTitle("Model Bake")
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
        self.gridlayout.addWidget(self.combobox, 0, 1, 1, 1)
        self.button_workspace = QtWidgets.QPushButton(self)
        self.button_workspace.setText("Workspace")
        # self.button_workspace.clicked.connect(self.workspace)
        self.gridlayout.addWidget(self.button_workspace, 1, 1, 1, 1)
        self.button_look = QtWidgets.QPushButton(self)
        self.button_look.setText("Look")
        # self.button_look.clicked.connect(self.create_look)
        self.gridlayout.addWidget(self.button_look, 2, 1, 1, 1)
        self.button_mov = QtWidgets.QPushButton(self)
        self.button_mov.setText("Movie")
        # self.button_mov.clicked.connect(self.create_movie)
        self.gridlayout.addWidget(self.button_mov, 3, 1, 1, 1)
        self.button_uv = QtWidgets.QPushButton(self)
        self.button_uv.setText("Export-UV")
        # self.button_uv.clicked.connect(self.export_uv)
        self.gridlayout.addWidget(self.button_uv, 4, 1, 1, 1)
        self.button_export = QtWidgets.QPushButton(self)
        self.button_export.setText("Export-Scene")
        # self.button_export.clicked.connect(self.export_scene)
        self.gridlayout.addWidget(self.button_export, 5, 1, 1, 1)
