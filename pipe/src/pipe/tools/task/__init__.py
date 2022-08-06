# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:16:Sunday-12:21:37:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core task create tool.

import os
import copy

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets
from pipe.tools.task import table

LOGGER = logger.getLogger(__name__)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)
        self.title = (
            kwargs.get("title") or "Studio-Pipe Tasks - 0.0.1"
        )
        self.wsize = kwargs.get("wsize") or [361, 138]
        self.taskicon = kwargs.get("taskicon") or [128, 128]
        self.titleicon = kwargs.get("titleicon") or [360, 68]
        self.version = os.getenv("PIPE-VERSION") or "unknown"

        self.iconpath = resources.getIconPath()
        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.browsepath = resources.getBrowsePath()
        self.current_project = dict()
        self.category_contexts = dict()
        self.project_contexts = dict()
        self.category_context = None
        self.current_category = None
        self.timeunits = dict()

        self.proj = studio.Project()
        self.step = studio.Steps()
        self.task = studio.Tasks()

        self.setupUi()
        self.setDeafult()
        self.setProjects()
        self.setupIcons()

        LOGGER.info(self.title)

    def setupUi(self):
        self.setObjectName("widget_tasks")
        self.setWindowTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])
        self.verticallayout = QtWidgets.QVBoxLayout(self)
        self.verticallayout.setSpacing(0)
        self.verticallayout.setObjectName("verticallayout")
        self.groupbox = QtWidgets.QGroupBox(self)
        self.groupbox.setTitle(
            "PIPE - Package Version: %s" % self.version
        )
        self.verticallayout.addWidget(self.groupbox)
        self.verticallayout_group = QtWidgets.QVBoxLayout(
            self.groupbox
        )
        self.verticallayout_group.setSpacing(1)
        self.verticallayout_group.setContentsMargins(5, 5, 5, 5)
        self.button_logo = QtWidgets.QPushButton(self.groupbox)
        self.button_logo.setFlat(True)
        self.verticallayout_group.addWidget(self.button_logo)
        self.line_up = QtWidgets.QFrame(self)
        self.line_up.setFrameShape(QtWidgets.QFrame.HLine)
        self.verticallayout_group.addWidget(self.line_up)
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.setContentsMargins(5, 5, 5, 5)
        self.gridlayout.setVerticalSpacing(5)
        self.gridlayout.setHorizontalSpacing(5)
        self.verticallayout_group.addLayout(self.gridlayout)
        self.label_project = QtWidgets.QLabel(self.groupbox)
        self.label_project.setAlignment(self.alignright)
        self.label_project.setText("Project")
        self.gridlayout.addWidget(self.label_project, 0, 0, 1, 1)
        self.combobox_project = QtWidgets.QComboBox(self.groupbox)
        self.combobox_project.currentIndexChanged.connect(
            self.setProject
        )
        self.gridlayout.addWidget(self.combobox_project, 0, 1, 1, 2)
        self.label_category = QtWidgets.QLabel(self.groupbox)
        self.label_category.setAlignment(self.alignright)
        self.label_category.setText("Category")
        self.gridlayout.addWidget(self.label_category, 1, 0, 1, 1)
        self.combobox_category = QtWidgets.QComboBox(self.groupbox)
        self.combobox_category.currentIndexChanged.connect(
            self.setCategory
        )
        self.gridlayout.addWidget(self.combobox_category, 1, 1, 1, 2)
        self.label_template = QtWidgets.QLabel(self.groupbox)
        self.label_template.setAlignment(self.alignright)
        self.label_template.setText("Task Template")
        self.gridlayout.addWidget(self.label_template, 2, 0, 1, 1)
        self.combobox_template = QtWidgets.QComboBox(self.groupbox)
        self.gridlayout.addWidget(self.combobox_template, 2, 1, 1, 2)
        self.button_import = QtWidgets.QPushButton(self.groupbox)
        self.button_import.setText("Import")
        self.button_import.clicked.connect(self.importTasks)
        self.gridlayout.addWidget(self.button_import, 3, 1, 1, 2)
        self.label_asset = QtWidgets.QLabel(self.groupbox)
        self.label_asset.setAlignment(self.alignright)
        self.label_asset.setText("Asset Name")
        self.gridlayout.addWidget(self.label_asset, 4, 0, 1, 1)
        self.combobox_asset = QtWidgets.QComboBox(self.groupbox)
        self.combobox_asset.setEditable(True)
        self.gridlayout.addWidget(self.combobox_asset, 4, 1, 1, 2)
        self.label_type = QtWidgets.QLabel(self.groupbox)
        self.label_type.setAlignment(self.alignright)
        self.label_type.setText("Type")
        self.gridlayout.addWidget(self.label_type, 5, 0, 1, 1)
        self.combobox_type = QtWidgets.QComboBox(self.groupbox)
        self.gridlayout.addWidget(self.combobox_type, 5, 1, 1, 2)
        self.label_sequence = QtWidgets.QLabel(self.groupbox)
        self.label_sequence.setAlignment(self.alignright)
        self.label_sequence.setText("Sequence")
        self.gridlayout.addWidget(self.label_sequence, 8, 0, 1, 1)
        self.combobox_sequence = QtWidgets.QComboBox(self.groupbox)
        self.combobox_sequence.setEditable(True)
        self.combobox_sequence.currentIndexChanged.connect(
            self.loadShotItems
        )
        self.gridlayout.addWidget(self.combobox_sequence, 8, 1, 1, 2)
        self.label_shot = QtWidgets.QLabel(self.groupbox)
        self.label_shot.setAlignment(self.alignright)
        self.label_shot.setText("Shot")
        self.gridlayout.addWidget(self.label_shot, 9, 0, 1, 1)
        self.combobox_shot = QtWidgets.QComboBox(self.groupbox)
        self.combobox_shot.setEditable(True)
        self.gridlayout.addWidget(self.combobox_shot, 9, 1, 1, 2)
        self.label_fps = QtWidgets.QLabel(self.groupbox)
        self.label_fps.setAlignment(self.alignright)
        self.label_fps.setText("FPS")
        self.gridlayout.addWidget(self.label_fps, 10, 0, 1, 1)
        self.combobox_fps = QtWidgets.QComboBox(self.groupbox)
        units = self.getTimeUnits()
        timeUnitIndex = self.getDefaultTimeUnitIndex()
        self.combobox_fps.addItems(units)
        self.combobox_fps.setCurrentIndex(timeUnitIndex)
        self.gridlayout.addWidget(self.combobox_fps, 10, 1, 1, 2)
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setSpacing(5)
        self.gridlayout.addLayout(self.horizontallayout, 11, 1, 1, 2)
        self.label_sframe = QtWidgets.QLabel(self.groupbox)
        self.label_sframe.setAlignment(self.alignright)
        self.label_sframe.setText("Start-Frame")
        self.horizontallayout.addWidget(self.label_sframe)
        self.spinbox_sframe = QtWidgets.QSpinBox(self.groupbox)
        sframe, eframe = self.getFrameRange()
        self.spinbox_sframe.setMinimum(1)
        self.spinbox_sframe.setMaximum(999999999)
        self.spinbox_sframe.setValue(sframe)
        self.spinbox_sframe.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.horizontallayout.addWidget(self.spinbox_sframe)
        self.label_eframe = QtWidgets.QLabel(self.groupbox)
        self.label_eframe.setAlignment(self.alignright)
        self.label_eframe.setText("End-Frame")
        self.horizontallayout.addWidget(self.label_eframe)
        self.spinbox_eframe = QtWidgets.QSpinBox(self.groupbox)
        self.spinbox_eframe.setMinimum(1)
        self.spinbox_eframe.setMaximum(999999999)
        self.spinbox_eframe.setValue(eframe)
        self.spinbox_eframe.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.horizontallayout.addWidget(self.spinbox_eframe)
        self.label_description = QtWidgets.QLabel(self.groupbox)
        self.label_description.setAlignment(self.alignright)
        self.label_description.setText("Description")
        self.gridlayout.addWidget(self.label_description, 12, 0, 1, 1)
        self.textedit_description = QtWidgets.QTextEdit(self.groupbox)
        self.gridlayout.addWidget(
            self.textedit_description, 12, 1, 1, 2
        )
        self.button_create = QtWidgets.QPushButton(self.groupbox)
        self.button_create.setText("Create")
        self.button_create.clicked.connect(self.create)
        self.gridlayout.addWidget(self.button_create, 13, 1, 1, 2)

    def setupIcons(self):
        widgets = [self]
        qwidgets.setWidgetsIcons(widgets)
        qwidgets.imageToButton(
            self.button_logo,
            self.titleicon[0],
            self.titleicon[1],
            locked=True,
            iconpath=utils.findIconpath(
                prefix="pipe-task", suffix=None
            ),
        )

    def getTimeUnits(self):
        timeUnit = self.proj.getTimeUnitContext()
        self.timeunits = copy.deepcopy(timeUnit["values"])
        context = list(map(lambda d: d["label"], self.timeunits))
        return context

    def getDefaultTimeUnitIndex(self):
        if not self.timeunits:
            self.getTimeUnits()
        timeUnitContext = self.proj.getDefaultTimeUnitContext()
        if timeUnitContext not in self.timeunits:
            return 0
        timeUnitIndex = self.timeunits.index(timeUnitContext)
        return timeUnitIndex

    def getFrameRange(self):
        frameRange = self.proj.getDefaultFrameRange()
        return frameRange

    @property
    def widgetTypes(self):
        widgets = {
            "assets": [
                # next release self.button_import,
                self.label_asset,
                self.combobox_asset,
                self.label_type,
                self.combobox_type,
                self.label_description,
                self.textedit_description,
                self.button_create,
            ],
            "sequence": [
                # next release self.button_import,
                self.label_sequence,
                self.combobox_sequence,
                self.label_shot,
                self.combobox_shot,
                self.label_fps,
                self.combobox_fps,
                self.label_sframe,
                self.spinbox_sframe,
                self.label_eframe,
                self.spinbox_eframe,
                self.label_description,
                self.textedit_description,
                self.button_create,
            ],
        }
        return widgets

    def hideWidgets(self):
        typed = self.widgetTypes
        widgets = sum(list(map(lambda k: typed[k], typed.keys())), [])
        for each in widgets:
            each.hide()

    def setDeafult(self):
        self.hideWidgets()
        self.button_import.hide()

    def cleanProject(self):
        self.combobox_asset.clear()
        self.combobox_type.clear()
        self.combobox_sequence.clear()
        self.combobox_shot.clear()
        self.textedit_description.clear()

    def cleanTaskComponents(self):
        self.textedit_description.clear()
        self.combobox_asset.setCurrentIndex(0)
        self.combobox_type.setCurrentIndex(0)
        self.combobox_sequence.setCurrentIndex(0)
        self.combobox_shot.setCurrentIndex(0)

    def setProjects(self):
        self.project_contexts = self.proj.getAllProjects()
        self.combobox_project.addItem("None")
        for each in self.project_contexts:
            iconpath = qwidgets.encodeIcon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox_project.addItem(icon, each["full_name"])

    def setProject(self):
        self.hideWidgets()
        self.cleanProject()
        current_index = self.combobox_project.currentIndex()
        if not current_index:
            LOGGER.warning("current project is null")
            return
        project = self.combobox_project.currentText()
        contexts = list(
            filter(
                lambda k: k["full_name"] == project,
                self.project_contexts,
            )
        )
        if not contexts:
            LOGGER.warning("invalid project name")
            return
        self.current_project = contexts[0]
        self.proj._setProject(self.current_project["name"])
        self.proj.getProject()
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        self.category_contexts = self.proj.getProjectCategories()
        self.combobox_category.clear()
        self.combobox_category.addItem("None")
        for each in self.category_contexts:
            iconpath = qwidgets.encodeIcon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox_category.addItem(icon, each["name"])
        self.task_contexts = self.step.getStepTemplates()
        self.combobox_template.clear()
        self.combobox_template.addItem("None")
        for each in self.task_contexts:
            self.combobox_template.addItem(icon, each["name"])
        QtWidgets.QApplication.restoreOverrideCursor()

    def setCategory(self):
        category = self.combobox_category.currentText()
        if category == "None":
            return
        category_contexts = list(
            filter(
                lambda k: k["name"] == category,
                self.category_contexts,
            )
        )
        if not category_contexts:
            return
        self.category_context = category_contexts[-1]
        self.current_category = self.category_context["name"]
        self.hideWidgets()
        if category not in self.widgetTypes:
            return
        for each in self.widgetTypes[category]:
            each.show()
        self.resize(361, 292)
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        if self.current_category == "assets":
            self.loadAssetItems()
        if self.current_category == "scene":
            self.loadSequenceItems()
        QtWidgets.QApplication.restoreOverrideCursor()

    def loadAssetItems(self):
        assets = self.step.getAssets(None)
        self.combobox_asset.clear()
        self.combobox_asset.addItem("")
        for each in assets:
            iconpath = qwidgets.encodeIcon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox_asset.addItem(icon, each["name"])
        self.combobox_type.clear()
        typed = self.step.getAssetTypes()
        for each in typed:
            self.combobox_type.addItem(each["name"])

    def loadSequenceItems(self):
        sequences = self.proj.find_sequences(
            self.current_project["id"], self.category_context["id"]
        )
        sequences = sorted(sequences, key=lambda k: (k["name"]))
        self.combobox_sequence.clear()
        self.combobox_sequence.addItem("")
        for each in sequences:
            iconpath = qwidgets.encodeIcon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox_sequence.addItem(icon, each["name"])

    def loadShotItems(self):
        sequence = self.combobox_sequence.currentText()
        if sequence in ["", None]:
            return
        shots = self.proj.find_shots(
            sequence, self.current_project["id"]
        )
        self.combobox_shot.clear()
        self.combobox_shot.addItem("")
        for each in shots:
            iconpath = qwidgets.encode_icon(
                each["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox_shot.addItem(icon, each["name"])

    def browse(self):
        filepath, format = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Browse your file to submit",
            self.browsepath,
            "(*.jpg *.png)",
        )
        directory = os.path.dirname(filepath)
        self.browsepath = directory

    def create(self):
        QtWidgets.QApplication.setOverrideCursor(
            QtCore.Qt.CustomCursor.WaitCursor
        )
        valid, message = False, "invalid execution"
        if self.current_category == "assets":
            valid, message = self.createAssetTask()
        if self.current_category == "sequence":
            valid, message = self.createSceneTask()
        QtWidgets.QApplication.restoreOverrideCursor()
        if not valid:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            LOGGER.warning(message)
            return
        self.setCategory()
        self.cleanTaskComponents()
        QtWidgets.QMessageBox.information(
            self, "information", message, QtWidgets.QMessageBox.Ok
        )

    def hasValidMainInputs(self):
        main_inputs = [
            [self.combobox_project, "project"],
            [self.combobox_category, "category"],
            [self.combobox_template, "template"],
        ]
        for each in main_inputs:
            current_index = each[0].currentIndex()
            if not current_index:
                LOGGER.warning("current %s is null" % each[1])
                return False
        return True

    def createAssetTask(self):
        name = self.combobox_asset.currentText()
        typed = self.combobox_type.currentText()
        template = self.combobox_template.currentText()
        description = self.textedit_description.toPlainText()
        if name in ["", None, "null"]:
            message = "Please enter your asset name"
            return False, message
        if typed in ["", None, "null"]:
            message = "Please select the your asset tier and try"
            return False, message
        valid, message, result = self.step.createNewAsset(
            name,
            typed,
            template,
            description=description,
        )
        return valid, message

    def createSceneTask(self):
        sequence = self.combobox_sequence.currentText()
        shot = self.combobox_shot.currentText()
        fps = self.combobox_fps.currentText()
        start = self.spinbox_sframe.value()
        end = self.spinbox_eframe.value()
        description = self.textedit_description.toPlainText()
        template = self.combobox_template.currentText()
        parent = self.current_category
        fps = float(fps.split(": ")[-1])
        if not self.hasValidMainInputs():
            return
        valid, message, result = self.step.createNewSequence(sequence)
        print("\n")
        LOGGER.info(message)
        print("\n")
        valid, message, result = self.step.createNewShot(
            shot,
            sequence,
            template,
            range=[start, end],
            description=description,
            fps=fps,
        )
        self.setCategory()
        return valid, message

    def importTasks(self):
        filepath, format = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Browse your %s input *.txt file" % self.current_category,
            self.browsepath,
            "(*.txt)",
        )
        kwargs = {
            "wsize": [800, 400],
            "filepath": filepath,
            "category": self.current_category,
            "project": self.current_project,
        }
        self.tawd = table.TableWindow(parent=None, **kwargs)
        self.tawd.show()

    @property
    def assetContext(self):
        project = self.current_project["id"]
        name = self.lineedit_name.text()
        fullname = self.lineedit_fullname.text()
        message = None
        if not fullname:
            message = "not found full name of the project"
        if not name:
            message = "not found short name of the project"
        if message:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
        context = {"name": name, "fullname": fullname}
        return context


if __name__ == "__main__":
    pass
