import ast
import copy

from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe import utils
from apis import studio
from pipe.core import logger
from pipe.utils import qwidgets


LOGGER = logger.getLogger(__name__)

from pprint import pprint


class Connect(QtWidgets.QGroupBox):
    def __init__(self, parent, **kwargs):
        super(Connect, self).__init__(parent, **kwargs)

        visible = kwargs.get("visible") or False
        self.framerange = [1001, 1002]
        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )

        self.step = studio.Steps()
        self.proj = studio.Project()

        self.setupUi()

    def setupUi(self):
        self.setStyleSheet("QGroupBox:title {color:#ffaa00;}")
        self.gridlayout = QtWidgets.QGridLayout(self)
        self.gridlayout.setContentsMargins(5, 5, 5, 5)
        self.gridlayout.setVerticalSpacing(5)
        self.gridlayout.setHorizontalSpacing(5)
        self.button_remove = qwidgets.createRemoveButton(size=12)
        self.gridlayout.addWidget(self.button_remove, 0, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(self)
        self.label_name.setAlignment(self.alignright)
        self.label_name.setText("Name")
        self.gridlayout.addWidget(self.label_name, 1, 0, 1, 1)
        self.lineedit_name = QtWidgets.QLineEdit(self)
        self.lineedit_name.setText("Name")
        self.gridlayout.addWidget(self.lineedit_name, 1, 1, 1, 1)
        self.label_type = QtWidgets.QLabel(self)
        self.label_type.setAlignment(self.alignright)
        self.label_type.setText("Type")
        self.gridlayout.addWidget(self.label_type, 2, 0, 1, 1)
        self.combobox_type = QtWidgets.QComboBox(self)
        self.gridlayout.addWidget(self.combobox_type, 2, 1, 1, 1)
        self.label_template = QtWidgets.QLabel(self)
        self.label_template.setAlignment(self.alignright)
        self.label_template.setText("Task Template")
        self.gridlayout.addWidget(self.label_template, 3, 0, 1, 1)
        self.combobox_template = QtWidgets.QComboBox(self)
        self.gridlayout.addWidget(self.combobox_template, 3, 1, 1, 1)
        self.label_fstart = QtWidgets.QLabel(self)
        self.label_fstart.setAlignment(self.alignright)
        self.label_fstart.setText("Start-Frame")
        self.gridlayout.addWidget(self.label_fstart, 4, 0, 1, 1)
        self.spinbox_fstart = QtWidgets.QSpinBox(self)
        self.spinbox_fstart.setMinimum(1)
        self.spinbox_fstart.setMaximum(999999999)
        self.spinbox_fstart.setValue(self.framerange[0])
        self.spinbox_fstart.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.gridlayout.addWidget(self.spinbox_fstart, 4, 1, 1, 1)
        self.label_fend = QtWidgets.QLabel(self)
        self.label_fend.setAlignment(self.alignright)
        self.label_fend.setText("End-Frame")
        self.gridlayout.addWidget(self.label_fend, 5, 0, 1, 1)
        self.spinbox_fend = QtWidgets.QSpinBox(self)
        self.spinbox_fend.setMinimum(1)
        self.spinbox_fend.setMaximum(999999999)
        self.spinbox_fend.setValue(self.framerange[1])
        self.spinbox_fend.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.NoButtons
        )
        self.gridlayout.addWidget(self.spinbox_fend, 5, 1, 1, 1)
        self.label_fps = QtWidgets.QLabel(self)
        self.label_fps.setAlignment(self.alignright)
        self.label_fps.setText("FPS")
        self.gridlayout.addWidget(self.label_fps, 6, 0, 1, 1)
        self.combobox_fps = QtWidgets.QComboBox(self)
        self.gridlayout.addWidget(self.combobox_fps, 6, 1, 1, 1)
        self.label_description = QtWidgets.QLabel(self)
        self.label_description.setAlignment(self.alignright)
        self.label_description.setText("Description")
        self.gridlayout.addWidget(self.label_description, 7, 0, 1, 1)
        self.textedit_description = QtWidgets.QTextEdit(self)
        self.textedit_description.setMinimumSize(QtCore.QSize(0, 100))
        self.textedit_description.setMaximumSize(
            QtCore.QSize(16777215, 100)
        )
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding,
        )
        self.textedit_description.setSizePolicy(size_policy)
        self.gridlayout.addWidget(
            self.textedit_description, 7, 1, 1, 1
        )
        self.label_assembly = QtWidgets.QLabel(self)
        self.label_assembly.setAlignment(self.alignright)
        self.label_assembly.setText("Asset\nAssembly")
        self.gridlayout.addWidget(self.label_assembly, 8, 0, 1, 1)
        self.treewidget_assembly = DropTreeToTreeWidget()
        self.gridlayout.addWidget(
            self.treewidget_assembly, 8, 1, 1, 1
        )
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.horizontallayout.setContentsMargins(2, 2, 2, 2)
        self.gridlayout.addLayout(self.horizontallayout, 9, 1, 1, 1)
        self.button_create = QtWidgets.QPushButton(self)
        self.button_create.setText("Create")
        self.horizontallayout.addWidget(self.button_create)
        self.button_update = QtWidgets.QPushButton(self)
        self.button_update.setText("Update")
        self.horizontallayout.addWidget(self.button_update)

    def setupDefault(self):
        self.lineedit_name.clear()
        self.combobox_type.setCurrentIndex(0)
        self.combobox_template.setCurrentIndex(0)
        self.spinbox_fstart.setValue(1001)
        self.spinbox_fend.setValue(1002)
        self.combobox_fps.setCurrentIndex(0)
        self.textedit_description.clear()
        self.treewidget_assembly.clear()

    def hideAllWidgets(self):
        for each in self.children():
            if isinstance(each, QtWidgets.QGridLayout):
                continue
            each.hide()

    @property
    def categoryWidgets(self):
        category_widgets = {
            "assets": [
                {"widget": self.lineedit_name, "name": "name"},
                {"widget": self.combobox_type, "name": "type"},
                {
                    "widget": self.combobox_template,
                    "name": "template",
                },
                {
                    "widget": self.textedit_description,
                    "name": "description",
                },
                {"widget": self.label_name, "lable": True},
                {"widget": self.label_type, "lable": True},
                {"widget": self.label_template, "lable": True},
                {"widget": self.label_description, "lable": True},
                {"widget": self.button_remove, "lable": True},
                {"widget": self.button_create, "lable": True},
                {"widget": self.button_update, "lable": True},
            ],
            "sequence": [
                {"widget": self.lineedit_name, "name": "name"},
                {
                    "widget": self.combobox_template,
                    "name": "template",
                },
                {"widget": self.combobox_fps, "name": "fps"},
                {"widget": self.spinbox_fstart, "name": "fstart"},
                {"widget": self.spinbox_fend, "name": "fend"},
                {
                    "widget": self.textedit_description,
                    "name": "description",
                },
                {
                    "widget": self.treewidget_assembly,
                    "name": "assembly",
                },
                {"widget": self.label_name, "lable": True},
                {"widget": self.label_template, "lable": True},
                {"widget": self.label_fps, "lable": True},
                {"widget": self.label_fstart, "lable": True},
                {"widget": self.label_fend, "lable": True},
                {"widget": self.label_description, "lable": True},
                {"widget": self.button_remove, "lable": True},
                {"widget": self.button_create, "lable": True},
                {"widget": self.button_update, "lable": True},
                {"widget": self.label_assembly, "lable": True},
            ],
            "shots": [
                {"widget": self.lineedit_name, "name": "name"},
                {
                    "widget": self.combobox_template,
                    "name": "template",
                },
                {"widget": self.spinbox_fstart, "name": "fstart"},
                {"widget": self.spinbox_fend, "name": "fend"},
                {
                    "widget": self.textedit_description,
                    "name": "description",
                },
                {
                    "widget": self.treewidget_assembly,
                    "name": "assembly",
                },
                {"widget": self.label_name, "lable": True},
                {"widget": self.label_template, "lable": True},
                {"widget": self.label_fstart, "lable": True},
                {"widget": self.label_fend, "lable": True},
                {"widget": self.label_description, "lable": True},
                {"widget": self.button_remove, "lable": True},
                {"widget": self.button_create, "lable": True},
                {"widget": self.button_update, "lable": True},
                {"widget": self.label_assembly, "lable": True},
            ],
        }
        return category_widgets

    def setupModeVisibility(self, mode):
        context = {
            "create": {
                self.button_create: True,
                self.button_update: False,
            },
            "update": {
                self.button_create: False,
                self.button_update: True,
            },
        }
        if not context.get(mode):
            return
        for k, v in context[mode].items():
            k.setVisible(v)

    def parameterContext(self, category, context, **kwargs):
        step = kwargs.get("step")
        result = copy.deepcopy(context)
        widgets = self.categoryWidgets.get(category)
        parent = kwargs.get("parent")
        for each in result:
            value = None
            if step:
                value = self.getFieldValue(
                    step,
                    each["field"],
                    fieldchild=each.get("fieldchild"),
                )
            if not value and parent and each.get("parent"):
                filed = each["field"]
                if each.get("fieldSuffix"):
                    filed = each["field"].rsplit(".", 1)[-1]
                value = self.getFieldValue(
                    parent, filed, fieldchild=each.get("fieldchild")
                )
            widget_contexts = utils.searchContext(
                widgets, "name", value=each.get("name")
            )
            widget_context = (
                widget_contexts[0] if widget_contexts else dict()
            )
            each["value"] = value
            each["widget"] = widget_context.get("widget")
        label_context = utils.searchContext(
            widgets, "lable", value=True
        )
        result.extend(label_context)
        return result

    def getFieldValue(self, step, filed, fieldchild=None):
        filedlist = filed.split(".")
        current = utils.getFieldValue(
            step, filedlist, fieldchild=fieldchild
        )
        return current

    def setupParameterWidgets(self, category, context):
        self.setupDefault()
        self.hideAllWidgets()
        self.setupWidgets(context)
        self.setTitle("%s-Parameters" % category)
        self.show()
        return context

    def setupWidgets(self, context):
        for each in context:
            if not each.get("widget"):
                continue
            each.get("widget").show()
            if not each.get("name"):
                continue
            value = (
                each["value"]
                if each.get("value")
                else each.get("default")
            )
            if isinstance(value, list):
                for x in value:
                    if each.get("color"):
                        x["color"] = each["color"]
                    if each.get("fontsize"):
                        x["fontsize"] = each["fontsize"]
            self.setWidgetValue(each["widget"], value)
        mode_context = utils.searchContext(
            context, "mode", value=None
        )
        self.setupModeVisibility(mode_context[0]["mode"])
        return context

    def setWidgetValue(self, widget, value):
        value = None if value == "null" else value
        if isinstance(widget, QtWidgets.QLineEdit):
            widget.clear()
            widget.setText(value)
            return True
        if isinstance(widget, QtWidgets.QComboBox):
            index = 0
            for x in range(widget.count()):
                data = widget.itemData(x)
                if data != value:
                    continue
                index = x
                break
            widget.setCurrentIndex(index)
            return True
        if isinstance(widget, QtWidgets.QSpinBox):
            value = value if value else 1
            widget.setValue(value)
            return True
        if isinstance(widget, QtWidgets.QTextEdit):
            widget.clear()
            widget.setText(value)
            return True
        if isinstance(widget, QtWidgets.QTreeWidget):
            if not value:
                return
            widget.clear()
            for index, each in enumerate(value):
                item = QtWidgets.QTreeWidgetItem(widget)
                item.setText(0, str(index + 1))
                item.setText(1, each.get("name"))
                item.setText(2, each.get("id"))
                item.setText(3, each.get("type"))
                qwidgets.setItemforegroundColor(
                    item, 1, color=each.get("color")
                )
                qwidgets.setItemFont(
                    item, 1, size=each.get("fontsize"), bold=True
                )
        return False

    def getWidgetValue(self, widget):
        if isinstance(widget, QtWidgets.QLineEdit):
            value = widget.text()
            return value
        if isinstance(widget, QtWidgets.QComboBox):
            index = widget.currentIndex()
            value = widget.itemData(index)
            if not value:
                value = widget.currentText()
            return value
        if isinstance(widget, QtWidgets.QSpinBox):
            value = widget.value()
            return value
        if isinstance(widget, QtWidgets.QTextEdit):
            value = widget.toPlainText()
            return value
        if isinstance(widget, QtWidgets.QTreeWidget):
            root_item = widget.invisibleRootItem()
            value = []
            for index in range(root_item.childCount()):
                item = root_item.child(index)
                color = item.foreground(1).color()
                font = item.font(1)
                context = {
                    "name": item.text(1),
                    "id": item.text(2),
                    "type": item.text(3),
                    "color": [
                        color.red(),
                        color.green(),
                        color.blue(),
                    ],
                    "fontsize": font.pointSize(),
                }
                value.append(context)
            return value

        return None

    def setupStepTemplates(self):
        self.templates_context = self.step.getStepTemplates()
        self.combobox_template.clear()
        self.combobox_template.addItem("None")
        for each in self.templates_context:
            self.combobox_template.addItem(each["name"], each["name"])
        return self.templates_context

    def setupAssetTypes(self):
        self.combobox_type.clear()
        self.assettype_context = self.step.getAssetTypes()
        self.combobox_type.addItem("None")
        for each in self.assettype_context:
            self.combobox_type.addItem(each["name"], each["name"])
        return self.assettype_context

    def setupFPS(self):
        timeunits, fpsindex = self.getFPSContext()
        for each in timeunits.get("values"):
            self.combobox_fps.addItem(
                each.get("label"), each.get("value")
            )
        self.combobox_fps.setCurrentIndex(fpsindex)
        return timeunits

    def getFPSContext(self):
        context = self.proj.getTimeUnitContext()
        default_timeunit = self.proj.getDefaultTimeUnitContext(
            context=context
        )
        index = 0
        if default_timeunit in context.get("values"):
            index = context.get("values").index(default_timeunit)
        return context, index

    def hasDefaultValue(self, context):
        name_context = utils.searchContext(
            context, "name", value="name"
        )
        if not name_context:
            LOGGER.warning("invalid context")
            return False
        value = qwidgets.getWidgetValue(name_context[0]["widget"])
        if not value:
            return True
        if value == name_context[0]["default"]:
            return True
        return False

    def updateValues(self, context, **kwargs):
        pin = kwargs.get("pin") or False
        for each in context:
            if each.get("widget"):
                value = self.getWidgetValue(each["widget"])
                each["value"] = value
            else:
                pass
            if "pin" in each:
                each["pin"] = pin
        return context

    def clearHistory(self, history, entity=True):
        context = history.copy()
        for each in context:
            if not entity:
                entity_context = utils.searchContext(
                    each, "entity", value=None
                )
                if entity_context:
                    continue
            pin_context = utils.searchContext(each, "pin", value=None)
            if pin_context:
                continue
            parent_context = utils.searchContext(
                each, "parent", value=None
            )
            if not parent_context:
                continue
            widgetitem = parent_context[0].get("parent")
            widgetitem.removeItem()
            history.remove(each)

    def removeStepItem(self, history):
        context = history.copy()


class DropTreeToTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent=None, **kwargs):
        super(DropTreeToTreeWidget, self).__init__(parent=None)

        self.color = kwargs.get("color") or [255, 170, 0]
        self.setColumnCount(4)
        self.setAlternatingRowColors(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.header().resizeSection(0, 50)
        self.header().resizeSection(1, 100)
        self.header().resizeSection(2, 0)
        self.headerItems = self.headerItem()
        self.headerItems.setText(0, "No")
        self.headerItems.setText(1, "Name")
        self.headerItems.setText(2, "ID")
        self.headerItems.setText(3, "Type")
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.setupMenu()
        self.setupIcons()

    def setupMenu(self):
        self.menu = QtWidgets.QMenu(self)
        self.menu.setTitle("Menu")
        self.action_remove = QtWidgets.QAction(self)
        self.action_remove.setText("Remove")
        self.menu.addAction(self.action_remove)
        self.action_remove.triggered.connect(self.removeItems)

    def setupIcons(self):
        qwidgets.setWidgetIcon(
            self.action_remove, utils.findIconpath(prefix="remove")
        )

    def dropEvent(self, event):
        source_treewidget = event.source()
        child_count = self.topLevelItemCount()
        for index, each in enumerate(
            source_treewidget.selectedItems()
        ):
            if not each.entity:
                message = "create the asset and try!..."
                QtWidgets.QMessageBox.warning(
                    self, "Warning", message, QtWidgets.QMessageBox.Ok
                )
                continue
            item = QtWidgets.QTreeWidgetItem(self)
            item.setText(0, str(index + 1 + child_count))
            item.setText(1, each.entity["name"])
            item.setText(2, each.entity["id"])
            item.setText(3, each.entity.entity_type)
            item.setFont(1, each.font(1))
            item.setForeground(1, each.foreground(1))
            item.setTextAlignment(1, each.textAlignment(1))

    def contextMenu(self, point):
        index = self.indexAt(point)
        if not index.isValid():
            return
        self.menu.exec_(self.mapToGlobal(point))

    def removeItems(self):
        widget_item = self.invisibleRootItem()
        for each in self.selectedItems():
            widget_item.removeChild(each)  # self.removeChild(each)


if __name__ == "__main__":
    pass
