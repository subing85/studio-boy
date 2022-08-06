# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-05:16:16:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe pyside wrapper.

import os
import requests

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe import utils
from pipe import resources


def encodeIcon(iconpath, prefix=None, suffix=None):
    if os.path.isfile(iconpath):
        image = imageToQImage(iconpath)
        return image

    if not iconpath:
        iconpath = utils.findIconpath(prefix=prefix, suffix=suffix)
        image = imageToQImage(iconpath)
        return image

    try:
        image = urlToImage(iconpath)
    except Exception:
        iconpath = utils.findIconpath(prefix=prefix, suffix=suffix)
        image = imageToQImage(iconpath)

    return image


def urlToImage(url_image):
    image = QtGui.QImage()
    image.loadFromData(requests.get(url_image).content)
    return image


def imageToQImage(image):
    qimage = QtGui.QImage(image)
    return qimage


def setWidgetsIcons(widgets):
    for widget in widgets:
        if not widget.objectName():
            continue
        name = widget.objectName().rsplit("_", 1)[-1]
        iconpath = os.path.join(
            resources.getIconPath(), "%s.png" % name
        )
        if not os.path.isfile(iconpath):
            iconpath = os.path.join(
                resources.getIconPath(), "unknown.png"
            )
        setWidgetIcon(widget, iconpath)


def setWidgetIcon(widget, iconpath, index=0):
    if not iconpath:
        iconpath = os.path.join(
            resources.getIconPath(), "unknown.png"
        )
    if isinstance(iconpath, str):
        if not os.path.isfile(iconpath):
            iconpath = os.path.join(
                resources.getIconPath(), "unknown.png"
            )
    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap(iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off
    )
    if isinstance(widget, QtWidgets.QMenu):
        widget.setIcon(icon)
    elif isinstance(widget, QtWidgets.QMainWindow) or isinstance(
        widget, QtWidgets.QWidget
    ):
        widget.setWindowIcon(icon)
    elif isinstance(widget, QtWidgets.QTreeWidgetItem):
        widget.setIcon(index, icon)
    else:
        widget.setIcon(icon)


def setItemTextAlignment(item, index, alignment=None):
    alignment = alignment or item.textAlignment(index)
    item.setTextAlignment(index, alignment)


def setItemTextAlignmentCenter(item, index):
    item.setTextAlignment(index, QtCore.Qt.AlignCenter)


def setItemTextAlignmentLeft(item, index):
    # item.setTextAlignment(index, QtCore.Qt.AlignLeft)
    item.setTextAlignment(
        index,
        QtCore.Qt.AlignLeading
        | QtCore.Qt.AlignLeft
        | QtCore.Qt.AlignVCenter,
    )


def setItemTextAlignmentRight(item, index):
    # item.setTextAlignment(index, QtCore.Qt.AlignRight)
    item.setTextAlignment(
        index,
        QtCore.Qt.AlignLeading
        | QtCore.Qt.AlignRight
        | QtCore.Qt.AlignVCenter,
    )


def setItemFont(item, index, size=None, bold=False):
    font = QtGui.QFont()
    if size:
        font.setPointSize(size)
    font.setBold(bold)
    item.setFont(index, font)


def setItemforegroundColor(item, index, color=(255, 85, 0)):
    if isinstance(color, str):
        qcolor = QtGui.QColor(color)
    else:
        qcolor = QtGui.QColor(color[0], color[1], color[2])
    brush = QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2]))
    brush.setStyle(QtCore.Qt.SolidPattern)
    item.setForeground(index, brush)


def setItembackgroundColor(item, index, color=(255, 85, 0)):
    if isinstance(color, str):
        qcolor = QtGui.QColor(color)
    else:
        qcolor = QtGui.QColor(color[0], color[1], color[2])
    brush = QtGui.QBrush(qcolor)
    brush.setStyle(QtCore.Qt.SolidPattern)
    item.setBackground(index, brush)


def imageToButton(button, width, height, iconpath, locked=False):
    icon = QtGui.QIcon()
    icon.addPixmap(
        QtGui.QPixmap(iconpath), QtGui.QIcon.Normal, QtGui.QIcon.Off
    )
    button.setIcon(icon)
    button.setIconSize(QtCore.QSize(width, height))
    if locked:
        button.setMinimumSize(QtCore.QSize(width, height))
        button.setMaximumSize(QtCore.QSize(width, height))


def findTreewidgetitems(treewidget):
    root_item = treewidget.invisibleRootItem()
    items = []
    for index in range(root_item.childCount()):
        item = root_item.child(index)
        if item.childCount():
            for x in range(item.childCount()):
                items.append(item.child(x))
        else:
            items.append(item)
    return items


def addListWidgetItem(*args, **kwargs):
    parent = args[0]
    label = args[1]
    statustip = kwargs.get("statustip", None)
    iconpath = kwargs.get("iconpath", None)
    resize = kwargs.get("resize", None)
    keepAspectRatio = kwargs.get("keepAspectRatio", False)

    item = QtWidgets.QListWidgetItem(parent)
    item.setText(label)
    item.setTextAlignment(
        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom
    )
    if not isinstance(statustip, str):
        statustip = str(statustip)
    item.setStatusTip(statustip)
    icon = QtGui.QIcon()
    image = encodeIcon(iconpath)
    if resize:
        if keepAspectRatio:
            image = image.scaled(
                resize[0], resize[1], QtCore.Qt.KeepAspectRatio
            )
        else:
            image = image.scaled(resize[0], resize[1])
        parent.setIconSize(
            QtCore.QSize(image.width(), image.height())
        )
    icon.addPixmap(
        QtGui.QPixmap(image), QtGui.QIcon.Normal, QtGui.QIcon.Off
    )
    item.setIcon(icon)
    return item


def deleteLayoutWidgets(layout):
    if not layout.count():
        return
    for index in range(layout.count()):
        if not layout.itemAt(index).widget():
            continue
        widget = layout.itemAt(index).widget()
        widget.deleteLater()


def removeTreeWidgetItems(parent, items):
    widget_item = parent.invisibleRootItem()
    for item in items:
        widget_item.removeChild(item)
        # parent.removeItemWidget(item, 0)


def findChildren(layout):
    widgets = []
    for index in range(layout.count()):
        if not layout.itemAt(index).widget():
            continue
        widget = layout.itemAt(index).widget()
        widgets.append(widget)
    return widgets


def setListIconWidget(widget):
    widget.setSortingEnabled(False)
    widget.setFlow(QtWidgets.QListView.LeftToRight)
    widget.setProperty("isWrapping", True)
    widget.setResizeMode(QtWidgets.QListView.Adjust)
    widget.setSpacing(0)
    widget.setUniformItemSizes(True)
    widget.setViewMode(QtWidgets.QListView.IconMode)
    widget.setMovement(QtWidgets.QListView.Static)
    widget.setSelectionRectVisible(True)


def setColorToItem(item, color, ground=True):
    treewidget = item.treeWidget()
    brush = QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2]))
    brush.setStyle(QtCore.Qt.SolidPattern)
    for index in range(treewidget.columnCount()):
        if ground:
            item.setForeground(index, brush)
        else:
            item.setBackground(index, brush)


def widgetVisibility(widgets, visible):
    if not widgets:
        return
    for widget in widgets:
        widget.setVisible(visible)


def clearWidgets(widgets):
    if not widgets:
        return
    for widget in widgets:
        widget.clear()


def setValue(context):
    if not context:
        return
    for widget, value in context.items():
        if isinstance(widget, QtWidgets.QComboBox):
            widget.setCurrentIndex(value)


def setEnableWidgets(widgets, enable=True):
    if not widgets:
        return
    for widget in widgets:
        widget.setEnabled(enable)


def createWidget(name, typed, color=[0, 140, 0]):
    widget = None
    if typed == "str":
        widget = QtWidgets.QLineEdit()
        widget.setObjectName("lineedit_%s" % name)
        widget.setReadOnly(True)
    if typed == "int":
        widget = QtWidgets.QSpinBox()
        widget.setObjectName("spinbox_%s" % name)
        widget.setMinimum(1)
        widget.setMaximum(999999999)
        widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
    if typed == "text":
        widget = QtWidgets.QTextEdit()
        widget.setObjectName("textedit_%s" % name)
        widget.setMinimumSize(QtCore.QSize(16777215, 40))
        widget.setMaximumSize(QtCore.QSize(16777215, 40))
        widget.setReadOnly(True)
    if widget:
        widget.setStyleSheet(
            "color: rgb(%s, %s, %s);" % (color[0], color[1], color[2])
        )
    return widget


def setWidgetValue(widget, value):
    if isinstance(widget, QtWidgets.QLineEdit):
        widget.setText(value)
        return True
    if isinstance(widget, QtWidgets.QComboBox):
        widget.setCurrentText(str(value))
        return True
    if isinstance(widget, QtWidgets.QSpinBox):
        value = value if value else 1
        widget.setValue(value)
        return True
    if isinstance(widget, QtWidgets.QTextEdit):
        widget.setText(value)
        return True
    return False


def getWidgetValue(widget):
    if isinstance(widget, QtWidgets.QLineEdit):
        value = widget.text()
        return value
    if isinstance(widget, QtWidgets.QComboBox):
        value = widget.currentText()
        return value
    if isinstance(widget, QtWidgets.QSpinBox):
        value = widget.value()
        return value
    if isinstance(widget, QtWidgets.QTextEdit):
        value = widget.toPlainText()
        return value
    return None


def messageBox(parent, title, message):
    messageBox = QtWidgets.QMessageBox(parent)
    messageBox.setWindowTitle(title)
    messageBox.setText(message)
    messageBox.addButton("Override", QtWidgets.QMessageBox.YesRole)
    messageBox.addButton("Skip", QtWidgets.QMessageBox.RejectRole)
    messageBox.addButton("Cancel", QtWidgets.QMessageBox.NoRole)
    reply = messageBox.exec_()
    return reply


def createButton(typed, **kwargs):
    size = kwargs.get("size", 15)
    font = kwargs.get("font", 12)
    bgcolor = kwargs.get("bgcolor", "#00b300")
    fgcolor = kwargs.get("fgcolor", "#ffffff")
    button = QtWidgets.QPushButton(None)
    button.setText(typed)
    button.setStyleSheet(
        'padding: 1px;\
        border-radius: %spx;\
        background-color: %s;\
        color: %s;\
        font: 87 %spt "Arial Black";'
        % (size, bgcolor, fgcolor, font)
    )
    button.setMinimumSize(QtCore.QSize(size * 2, size * 2))
    button.setMaximumSize(QtCore.QSize(size * 2, size * 2))
    return button


def createBulletButton(**kwargs):
    button = createButton("", **kwargs)
    return button

def createAddButton(**kwargs):
    button = createButton(u"\U0001F7A7", **kwargs)
    return button


def createPinButton(**kwargs):
    button = createButton(u"\U0001F4CC", **kwargs)
    return button


def createRemoveButton(**kwargs):
    button = createButton(u"\u274C", **kwargs)
    return button


def createHistoryButton(**kwargs):
    # u"\U0001F177" u"\U00010385" u"\u24BD" u"\U0001F157"  u"\U0001F117"
    button = createButton(u"\U0001F117", **kwargs)
    return button


def createClearButton(**kwargs):
    button = createButton(u"\u239A", **kwargs)
    return button


def createRunButton(**kwargs):
    button = createButton(u"\U0001F3C3", **kwargs)
    return button


def createValidateButton(**kwargs):
    button = createButton(u"\u2714", **kwargs)
    return button


def createPipeLogButton(**kwargs):
    size = kwargs.get("size", 8)
    color = kwargs.get("color", "#a3a3a3")
    iconsize = kwargs.get("iconsize", 24)

    iconpath = resources.getPipeLogo()

    button = QtWidgets.QPushButton(None)
    button.setText("www.subins-toolkits.com")
    button.setFlat(True)
    button.setStyleSheet(
        'padding: 1px;\
        border-radius: %spx;\
        color: %s;\
        font: 87 %spt "Arial Black";\
        text-align: right;'
        % (size, color, size)
    )

    imageToButton(
        button, iconsize, iconsize, locked=False, iconpath=iconpath
    )
    return button


def convertInvalidButton(button, **kwargs):
    kwargs["typed"] = u"\u2715"
    setButtonProperty(button, **kwargs)

def createRefreshButton(**kwargs):
    button = createButton(u"\u21BB", **kwargs)
    return button




def setButtonProperty(button, **kwargs):
    size = kwargs.get("size", 15)
    font = kwargs.get("font", 12)
    bgcolor = kwargs.get("bgcolor", "#00b300")
    fgcolor = kwargs.get("fgcolor", "#ffffff")
    typed = kwargs.get("typed", button.text())
    button.setText(typed)
    button.setStyleSheet(
        'padding: 1px;\
        border-radius: %spx;\
        background-color: %s;\
        color: %s;\
        font: 87 %spt "Arial Black";'
        % (size, bgcolor, fgcolor, font)
    )


def progressBarLine():
    pass


if __name__ == "__main__":
    pass
