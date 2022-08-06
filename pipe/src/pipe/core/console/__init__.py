# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:49:17:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core custom console.

import sys

from PySide2 import QtGui
from PySide2 import QtCore
import warnings


class Connect(QtCore.QObject):
    _stdout = None
    _stderr = None
    message_written = QtCore.Signal(str)

    def __init__(self, widget=None):
        super(Connect, self).__init__()
        self.widget = widget

    def flush(self):
        pass

    def write(self, message):
        if self.signalsBlocked():
            return
        self.setTextColor(message)
        self.message_written.emit(message)

    @staticmethod
    def stdout(widget):
        if not Connect._stdout:
            Connect._stdout = Connect(widget)
            sys.stdout = Connect._stdout
        return Connect._stdout

    @staticmethod
    def stderr():
        if not Connect._stderr:
            sys.stderr = Connect._stderr
        return Connect._stderr

    def setTextColor(self, message):
        # header color, info color, warning color, error color
        clolor_bundle = self.getColorCode()
        if "#header" in message:
            clolor_code = clolor_bundle[0]
        elif "#info" in message:
            clolor_code = clolor_bundle[1]
        elif "#warning" in message:
            clolor_code = clolor_bundle[2]
        elif "#error" in message:
            clolor_code = clolor_bundle[3]
        elif "#failed" in message:
            clolor_code = clolor_bundle[3]
        else:
            clolor_code = clolor_bundle[1]
        self.widget.setTextColor(clolor_code)

    def getColorCode(self):
        info_color = QtGui.QColor("darkBlue")
        error_color = QtGui.QColor("red")
        warning_color = QtGui.QColor("magenta")
        header_color = QtGui.QColor("green")
        return header_color, info_color, warning_color, error_color


if __name__ == "__main__":
    pass
