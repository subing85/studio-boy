import os
import sys

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from apis import studio
from pipe.core import logger
from pipe.tools import launcher
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)
        self._title = "Studio-Pipe Login -0.0.1"
        self._label = "STUDIO-PIPE"
        self._size = kwargs.get("size") or [650, 400]
        self._version = os.getenv("PIPE-VERSION") or "unknown"
        self.logn = studio.Login()
        self.setupUi()
        self.loadHistory()
        self.setupIcons()

    def setupUi(self):
        self.setObjectName("login")
        self.resize(self._size[0], self._size[1])
        self.setStyleSheet("font: 14pt;")
        self.setWindowTitle(self._title)
        self.gridlayout_main = QtWidgets.QGridLayout(self)
        self.gridlayout_main.setObjectName("gridlayout_main")
        spaceritem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridlayout_main.addItem(spaceritem, 0, 1, 1, 1)
        spaceritem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridlayout_main.addItem(spaceritem, 2, 1, 1, 1)
        spaceritem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.gridlayout_main.addItem(spaceritem, 1, 2, 1, 1)
        spaceritem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.gridlayout_main.addItem(spaceritem, 1, 0, 1, 1)
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setObjectName("gridlayout")
        self.gridlayout_main.addLayout(self.gridlayout, 1, 1, 1, 1)
        self.button_icon = QtWidgets.QPushButton(self)
        self.button_icon.setObjectName("button_icon")
        self.button_icon.setFlat(True)
        self.gridlayout.addWidget(self.button_icon, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.label.setText(self._label)
        self.label.setStyleSheet("font: 87 14pt 'Arial Black';")
        self.label.setAlignment(
            QtCore.Qt.AlignBottom
            | QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
        )
        self.gridlayout.addWidget(self.label, 0, 1, 1, 1)
        self.combobox_id = QtWidgets.QComboBox(self)
        self.combobox_id.setObjectName("combobox_id")
        self.combobox_id.setMinimumSize(QtCore.QSize(450, 0))
        self.combobox_id.setEditable(True)
        self.combobox_id.setInsertPolicy(
            QtWidgets.QComboBox.InsertBeforeCurrent
        )
        self.combobox_id.setSizeAdjustPolicy(
            QtWidgets.QComboBox.AdjustToContents
        )
        self.combobox_id.addItem("")
        self.gridlayout.addWidget(self.combobox_id, 1, 0, 1, 2)
        self.lineedit_id = QtWidgets.QLineEdit(self)
        self.lineedit_id.setObjectName("lineedit_id")
        self.lineedit_id.setEchoMode(
            QtWidgets.QLineEdit.PasswordEchoOnEdit
        )
        self.lineedit_id.setCursorPosition(4)
        self.lineedit_id.hide()
        self.gridlayout.addWidget(self.lineedit_id, 2, 0, 1, 2)
        self.lineedit_old = QtWidgets.QLineEdit(self)
        self.lineedit_old.setObjectName("lineedit_old")
        self.lineedit_old.setText("old - passwod")
        self.lineedit_old.setEchoMode(
            QtWidgets.QLineEdit.PasswordEchoOnEdit
        )
        self.lineedit_old.hide()
        self.gridlayout.addWidget(self.lineedit_old, 3, 0, 1, 2)
        self.lineedit_new = QtWidgets.QLineEdit(self)
        self.lineedit_new.setObjectName("lineedit_new")
        self.lineedit_new.setText("new - passwod")
        self.lineedit_new.setEchoMode(
            QtWidgets.QLineEdit.PasswordEchoOnEdit
        )
        self.lineedit_new.hide()
        self.gridlayout.addWidget(self.lineedit_new, 4, 0, 1, 2)
        self.button_login = QtWidgets.QPushButton(self)
        self.button_login.setObjectName("button_login")
        self.button_login.setText("Login")
        self.button_login.clicked.connect(self.userlogin)
        self.gridlayout.addWidget(self.button_login, 5, 0, 1, 2)
        self.button_reset = QtWidgets.QPushButton(self)
        self.button_reset.setObjectName("button_reset")
        self.button_reset.setText("Reset")
        self.button_reset.hide()
        self.gridlayout.addWidget(self.button_reset, 6, 0, 1, 2)
        self.button_apply = QtWidgets.QPushButton(self)
        self.button_apply.setObjectName("button_apply")
        self.button_apply.setText("Apply")
        self.button_apply.hide()
        self.gridlayout.addWidget(self.button_apply, 7, 0, 1, 2)

    def setupIcons(self):
        qwidgets.setWidgetIcon(self, utils.findIconpath("login"))
        qwidgets.imageToButton(
            self.button_icon,
            128,
            128,
            locked=True,
            iconpath=utils.findIconpath("users"),
        )

    def loadHistory(self):
        history = self.logn.readHistory()
        LOGGER.info("your login history")
        if not history:
            LOGGER.warning("not found login history")
            return
        for each in history:
            print("\t", " ".join(each))
        usernames = list(set([each[2] for each in history]))
        self.combobox_id.addItems(usernames)

    def userlogin(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        username = self.combobox_id.currentText()
        if not username:
            message = "please enter your Login ID"
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            LOGGER.warning(message)
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        valid = self.logn.setUsername(username)
        QtWidgets.QApplication.restoreOverrideCursor()
        if not valid:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "invalid user name",
                QtWidgets.QMessageBox.Ok,
            )
            LOGGER.warning(message)
            return
        self.logn.getUsername()
        LOGGER.info("login success!...")
        self.close()
        command = "pipe launch launcher"
        os.system(command)


if __name__ == "__main__":
    pass
