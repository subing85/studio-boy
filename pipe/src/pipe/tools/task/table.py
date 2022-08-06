# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:16:Sunday-12:23:11:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core multi-task create tool.

import os
import sys
import threading

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from apis import studio
from pipe.core import logger
from pipe.utils import qwidgets

LOGGER = logger.getLogger(__name__)


class TableWindow(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(TableWindow, self).__init__(parent)

        self.wsize = kwargs.get("wsize") or [800, 400]
        self.title = (
            kwargs.get("title")
            or "Studio-Pipe Tasks Import Table - 0.0.1"
        )
        self.filepath = kwargs.get("filepath")
        self.category = kwargs.get("category")
        self.project = kwargs.get("project")

        self.info_color = [0, 0, 0]
        self.error_color = [255, 0, 0]
        self.invalids = []

        self.proj = studio.Project()
        self.task = studio.Tasks()

        self.setupUi()
        self.setupTable()
        self.setupIcons()

        LOGGER.info(self.title)

    def setupUi(self):
        self.setObjectName("widget_table")
        self.setWindowTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])
        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.verticallayout.setObjectName("verticalLayout")
        self.tablewidget = QtWidgets.QTableWidget(self)
        self.tablewidget.setAlternatingRowColors(True)
        self.tablewidget.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.tablewidget.horizontalHeader().setStretchLastSection(
            True
        )
        self.tablewidget.verticalHeader().setStretchLastSection(True)
        self.verticallayout.addWidget(self.tablewidget)
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setSpacing(5)
        self.verticallayout.addLayout(self.horizontallayout)
        self.button_reload = QtWidgets.QPushButton(self)
        self.button_reload.setText("Reload")
        self.button_reload.clicked.connect(self.reloadInput)
        self.horizontallayout.addWidget(self.button_reload)
        self.button_validate = QtWidgets.QPushButton(self)
        self.button_validate.setText("Validate")
        self.button_validate.clicked.connect(self.validate)
        self.horizontallayout.addWidget(self.button_validate)
        self.button_create = QtWidgets.QPushButton(self)
        self.button_create.setText("Create")
        self.button_create.clicked.connect(self.createTasks)
        self.horizontallayout.addWidget(self.button_create)

    def setupIcons(self):
        qwidgets.set_widgets_icons([self])

    @property
    def headers(self):
        header = {
            "assets": ["name", "type", "template", "description"],
            "sequence": [
                "sequence",
                "shot",
                "template",
                "fps",
                "start-frame",
                "end-frame",
                "description",
            ],
        }
        if self.category not in header:
            return None
        return header[self.category]

    def tableData(self):
        lines = []
        with open(self.filepath, "r") as file:
            lines = file.readlines()
        contexts, tmp = [], []
        for line in lines:
            if not line or line in ["\n", "\r\n"]:
                continue
            context = line.split(",")
            if context in contexts:
                continue
            context = [each.strip() for each in context]
            if len(context) == 1:
                continue
            if context[0:2] in tmp:
                continue
            tmp.append(context[0:2])
            contexts.append(context)
        return contexts

    def getContexts(self):
        rows = self.tablewidget.rowCount()
        columns = self.tablewidget.columnCount()
        contexts = []
        for row in range(rows):
            context = []
            for column in range(columns):
                item = self.tablewidget.item(row, column)
                if not item:
                    continue
                value = item.text()
                context.append(value)
            if not context:
                continue
            contexts.append(context)
        return contexts

    def reloadInput(self):
        self.setupTable()

    def validate(self):
        inputs = self.getContexts()
        contexts = self.validateInputs(inputs=inputs)
        self.setupTable(contexts=contexts)

    def validateInputs(self, inputs=None):
        inputs = inputs or self.tableData()
        context = []
        if self.category == "assets":
            context = self.validateAsset(inputs)
        if self.category == "sequence":
            context = self.validateSequence(inputs)
        return context

    def validateAsset(self, inputs):
        exists_assets = self.task.getAssetNames(
            None, id=self.project["id"]
        )
        asset_types = self.task.getAssetTypeNames(
            id=self.project["id"]
        )
        task_tempalte = self.task.getTaskTempalteNames(
            id=self.project["id"]
        )
        names = [exists_assets, asset_types, task_tempalte, []]
        contexts = []
        for input in inputs:
            _contexts = []
            for x in range(len(self.headers)):
                if len(input) <= x:
                    value = "null"
                else:
                    value = input[x].strip()
                if not value:
                    value = "null"
                context = {self.headers[x]: value}
                if self.headers[x] == "description":
                    _contexts.append(context)
                    continue
                if value == "null":
                    context["invalid"] = True
                    context["message"] = "null value"
                if x == 0:
                    if value in names[x]:
                        context["invalid"] = True
                        context[
                            "message"
                        ] = "already exists the same value"
                else:
                    if value not in names[x]:
                        context["invalid"] = True
                        context["message"] = "invalid value"
                _contexts.append(context)
            contexts.append(_contexts)
        return contexts

    def createContext(self, key, value):
        context = {key: value}
        if value == "null":
            context["invalid"] = True
            context["message"] = "null value"
        return context

    def validateSequence(self, inputs):
        contexts = []
        for input in inputs:
            input = list(filter(None, input))
            if len(input) < 3:
                sequence, shot, template = "null", "null", "null"
                fps, sframe, eframe, description = (
                    "null",
                    "null",
                    "null",
                    "null",
                )
            else:
                sequence = input[0].strip()
                shot = input[1].strip()
                template = input[2].strip()
            _sequence = self.createContext("sequence", sequence)
            _shot = self.createContext("shot", shot)
            _template = self.createContext("template", template)

            exists = self.task.isShotExists(
                sequence, shot, id=self.project["id"]
            )
            if exists:
                _shot["invalid"] = True
                _shot["message"] = "already exists the same value"
            _contexts = [_sequence, _shot, _template]

            for x in range(3, len(self.headers)):
                if len(input) <= x:
                    value = "null"
                else:
                    value = input[x].strip()
                if not value:
                    value = "null"
                other = {self.headers[x]: value}
                if self.headers[x] == "description":
                    _contexts.append(other)
                    continue
                if value == "null":
                    other["invalid"] = True
                    other["message"] = "null value"
                _contexts.append(other)
            contexts.append(_contexts)
        return contexts

    def setupTable(self, contexts=None):
        if not self.headers:
            return
        self.tablewidget.clear()
        self.tablewidget.removeRow(self.tablewidget.rowCount())
        self.tablewidget.removeColumn(self.tablewidget.colorCount())
        contexts = contexts or self.validateInputs(
            inputs=self.tableData()
        )
        if not contexts:
            return
        self.tablewidget.setColumnCount(len(self.headers))
        self.tablewidget.setHorizontalHeaderLabels(self.headers)
        self.invalids = []
        for row, context in enumerate(contexts):
            self.tablewidget.setRowCount(row + 1)
            self.addItems(context, row)
        self.tablewidget.setRowCount(row + 2)
        self.tablewidget.horizontalHeader().resizeSection(2, 350)

    def addItems(self, context, row):
        for column, each in enumerate(context):
            header = self.tablewidget.horizontalHeaderItem(
                column
            ).text()
            item = QtWidgets.QTableWidgetItem(each.get(header))
            self.tablewidget.setItem(row, column, item)
            r, g, b = self.info_color
            if each.get("invalid"):
                r, g, b = self.error_color
                item.setToolTip(each.get("message"))
                self.invalids.append(True)
            brush = QtGui.QBrush(QtGui.QColor(r, g, b))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)

    def createTasks(self):
        if self.invalids:
            replay = QtWidgets.QMessageBox.critical(
                self,
                "Critical",
                "find invalid inputs, fix and try to create",
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No,
            )
            LOGGER.warning(
                "find invalid inputs, fix and try to create"
            )
            return
        contexts = self.getContexts()
        replay = QtWidgets.QMessageBox.question(
            self,
            "Question",
            "Are you sure, you want to create %s tasks?"
            % self.category,
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if replay == QtWidgets.QMessageBox.No:
            LOGGER.warning("Abort the version create tasks!...")
            return
        if self.category == "assets":
            valid, message = self.createAssetsTask(
                contexts, thread=False
            )
        if self.category == "sequence":
            valid, message = self.createSceneTask(
                contexts, thread=False
            )
        QtWidgets.QMessageBox.information(
            self, "Information", message, QtWidgets.QMessageBox.Ok
        )
        LOGGER.warning(message)
        self.close()

    def createAssetsTask(self, contexts, thread=False):
        for each in contexts:
            if thread:
                self.thread_state = threading.Condition()
                self.task_thread = threading.Thread(
                    target=self.startAssetTask,
                    args=(
                        [
                            each[0],
                            each[1],
                            each[2],
                            each[3],
                            self.project["id"],
                        ]
                    ),
                )
                self.task_thread.daemon = True
                self.task_thread.start()
            else:
                self.startAssetTask(
                    each[0],
                    each[1],
                    each[2],
                    each[3],
                    self.project["id"],
                )
        return True, "create asset tasks done!..."

    def startAssetTask(self, name, typed, template, description, id):
        valid, message, result = self.task.createNewAsset(
            name, typed, template, description=description, id=id
        )
        if not valid:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            LOGGER.warning(
                "failed asset, (%s, %s) %s" % (name, typed, message)
            )
        else:
            LOGGER.info("created asset, (%s, %s)" % (name, typed))

    def createSceneTask(self, contexts, thread=False):
        for each in contexts:
            if thread:
                self.thread_state = threading.Condition()
                self.task_thread = threading.Thread(
                    target=self.startSceneTask,
                    args=(
                        [
                            each[0],
                            each[1],
                            each[2],
                            each[3],
                            each[4],
                            each[5],
                            each[6],
                            self.project["id"],
                        ]
                    ),
                )
                self.task_thread.daemon = True
                self.task_thread.start()
            else:
                self.startSceneTask(
                    each[0],
                    each[1],
                    each[2],
                    each[3],
                    each[4],
                    each[5],
                    each[6],
                    self.project["id"],
                )
        return True, "create shot tasks done!..."

    def startSceneTask(
        self,
        sequence,
        shot,
        template,
        fps,
        sframe,
        eframe,
        description,
        id,
    ):
        valid, message, result = self.task.createNewShot(
            sequence,
            shot,
            template,
            [int(sframe), int(eframe)],
            description=description,
            fps=float(fps),
            id=id,
        )
        if not valid:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            LOGGER.warning(
                "failed asset, (%s, %s) %s"
                % (sequence, shot, message)
            )
        else:
            LOGGER.info("created, (%s, %s)" % (sequence, shot))


if __name__ == "__main__":
    pass
