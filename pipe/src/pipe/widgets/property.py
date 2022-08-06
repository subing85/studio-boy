import os
import sys
import importlib

from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from apis import studio

# from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets


LOGGER = logger.getLogger(__name__)


from pprint import pprint


class Connect(QtWidgets.QGroupBox):

    entity = None

    def __init__(self, parent, **kwargs):
        super(Connect, self).__init__(parent)

        self.wsize = kwargs.get("wsize") or [282, 611]
        self.visible = kwargs.get("visible") or False
        self.inputs = kwargs.get("inputs")
        if not self.inputs:
            inpt = studio.Inputs(typed="property")
            self.inputs = inpt.get()
        self.title = kwargs.get("title")
        self.application = kwargs.get("application") or None

        self.triggers = ["Open", "Refernce", "Build"]

        self.setupUi()
        self.setupDefault()

    def setupUi(self):
        self.setStyleSheet("QGroupBox:title {color:#ffaa00;}")
        # self.setTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(6)
        sizepolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Maximum,
        )

        for index, each in enumerate(self.inputs):
            self.label = QtWidgets.QLabel(self)
            self.label.setText(each["display-name"])
            self.label.setSizePolicy(sizepolicy)
            if each.get("fontsize"):
                self.label.setStyleSheet(
                    'font: %spt "MS Shell Dlg 2";' % each["fontsize"]
                )
            self.label.setAlignment(
                QtCore.Qt.AlignBottom
                | QtCore.Qt.AlignLeading
                | QtCore.Qt.AlignRight
            )
            self.gridLayout.addWidget(self.label, index, 0, 1, 1)
            if each["childType"] == "icon":
                self.field = QtWidgets.QPushButton(self)
                self.field.setFlat(True)
                sizePolicy = QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Minimum,
                    QtWidgets.QSizePolicy.Preferred,
                )
                self.field.setSizePolicy(sizePolicy)
                iconpath = utils.findIconpath(
                    prefix=each["childValue"]
                )
                qwidgets.imageToButton(
                    self.field,
                    each["childIconsize"][0],
                    each["childIconsize"][1],
                    locked=True,
                    iconpath=iconpath,
                )
                self.field.clicked.connect(self.reload)
            elif each["childType"] == "textEdit":
                self.field = QtWidgets.QTextEdit(self)
                self.field.setReadOnly(True)
                self.field.setText(each["childValue"])
            else:
                self.field = QtWidgets.QLineEdit(self)
                self.field.setReadOnly(True)
                self.field.setText(each["childValue"])

            self.field.setStyleSheet(
                "border: 1px; border-radius: 5px;"
            )
            self.gridLayout.addWidget(self.field, index, 1, 1, 1)

            each["keyWidget"] = self.label
            each["valueWidget"] = self.field

        index += 1

        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout.addWidget(self.line, index, 1, 1, 1)

        index += 1
        spaceritem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.gridLayout.addItem(spaceritem, index, 1, 1, 1)

        index += 1
        for each in self.triggers:
            self.trigger = QtWidgets.QPushButton(self)
            self.trigger.setText(each)
            self.trigger.clicked.connect(
                partial(self.triggerActions, each)
            )
            self.gridLayout.addWidget(self.trigger, index, 1, 1, 1)
            index += 1

            if not self.application:
                self.trigger.setVisible(False)

        # spaceritem = QtWidgets.QSpacerItem(
        #    20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        # )
        # self.gridLayout.addItem(spaceritem, index + 2, 1, 1, 1)

    def setupDefault(self):
        self.setVisible(self.visible)

    def setEntity(self, entity):
        self.entity = entity

    def update(self, entity=None):
        entity = entity or self.entity

        for each in self.inputs:
            parent_value = each["display-name"]
            child_value = None

            # update key widget
            if each.get("filed"):
                if entity.entity_type in each["filed"]:
                    filed = each["filed"][entity.entity_type]
                else:
                    filed = each["filed"]["common"]
                filedlist = filed.split(".")
                parent_value = utils.getFieldValue(
                    entity,
                    filedlist,
                    fieldchild=each.get("fieldchild"),
                )

            # update child value widget

            if entity.entity_type in each["childFiled"]:
                child_filed = each["childFiled"][entity.entity_type]
            else:
                child_filed = each["childFiled"]["common"]

            child_fileds = child_filed.split(".")

            if child_filed == "link":
                child_value = utils.getFieldValue(
                    entity, child_fileds, fieldchild=None
                )
                links = [k["name"] for k in child_value[1:]]
                child_value = "|" + "|".join(links)

            else:
                child_value = utils.getFieldValue(
                    entity, child_fileds, fieldchild=None
                )

            if not child_value:
                each["keyWidget"].hide()
                each["valueWidget"].hide()
                continue

            each["keyWidget"].show()
            each["valueWidget"].show()
            each["keyWidget"].setText(parent_value)

            if each["childType"] == "icon":
                iconpath = qwidgets.encodeIcon(child_value)
                qwidgets.imageToButton(
                    each["valueWidget"],
                    each["childIconsize"][0],
                    each["childIconsize"][1],
                    locked=True,
                    iconpath=iconpath,
                )

            elif each["childType"] == "textEdit" or "lineEdit":
                each["valueWidget"].setText(child_value)

    def triggerActions(self, typed):
        action = "pipe.tools.warehouse.actions"
        _module = importlib.import_module(action)

        if not hasattr(_module, "excute"):
            message = "not found <%s> function under the" % (
                _module.__package__
            )
            LOGGER.error(message)
            return False, message
        _module.excute(typed=typed, entity=self.entity)

    def reload(self):
        print(self.size())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    kwargs = {}
    window = Connect(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
