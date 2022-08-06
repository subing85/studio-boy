import threading

from PySide2 import QtCore
from PySide2 import QtWidgets

from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class Connect(QtWidgets.QProgressBar):
    def __init__(self, parent, **kwargs):
        super(Connect, self).__init__(parent)

        self.textvisible = kwargs.get("textvisible", True)
        self.orientation = kwargs.get(
            "orientation", "horizontal"
        )  # vertical
        self.inverted = kwargs.get("inverted", False)
        self.direction = kwargs.get("direction", "TopToBottom")
        self.visible = kwargs.get("visible", True)
        self.fontsize = kwargs.get("font", 12)
        self.plane = kwargs.get("plane", False)
        self.stylesheet = self.getStyleSheet()
        self._orientation = (
            QtCore.Qt.Vertical
            if self.orientation == "vertical"
            else QtCore.Qt.Horizontal
        )
        self._direction = (
            QtWidgets.QProgressBar.TopToBottom
            if self.direction == "TopToBottom"
            else QtWidgets.QProgressBar.BottomToTop
        )
        self.setStyleSheet(self.stylesheet)
        self.setTextVisible(self.textvisible)
        self.setOrientation(self._orientation)
        self.setInvertedAppearance(self.inverted)
        self.setTextDirection(self._direction)
        self.setVisible(self.visible)
        self.clear()

    def setMessage(self, message):
        self.setFormat(message)

    def setProgress(self, index, message, **kwrags):
        plane = kwrags.get("plane", False)
        error = kwrags.get("error", True)
        thread = kwrags.get("thread", True)

        index = index if index else self.value()

        if thread:
            state = threading.Condition()
            current_thread = threading.Thread(
                target=self._setProgress,
                args=(
                    [
                        index,
                        message,
                        plane,
                        error,
                    ]
                ),
            )
            current_thread.daemon = True
            current_thread.start()
        else:
            self._setProgress(index, message, plane, error)

    def _setProgress(self, index, message, plane, error):
        stylesheet = self.getStyleSheet(red=error)
        self.setStyleSheet(stylesheet)
        message = (
            message if plane else "%s \t\t %s" % (message, "%p%")
        )
        self.currentValue = index
        self.setValue(self.currentValue)
        self.setFormat(message)
        LOGGER.info(message)

    def clear(self):
        # self.setValue(100)
        self.currentValue = 0
        self.setValue(self.currentValue)
        self.setFormat("")  # ("%p%")

    def getStyleSheet(self, red=False):
        color = "#ff0000" if red else "#000000"
        data = {
            False: """
                QProgressBar {border: 1px; border-radius: 10px; text-align: right; color: %s; font: %spt;}
                QProgressBar::chunk {background-color: #aaaa00; width: 5px; margin: 6px;}
            """
            % (
                color,
                self.fontsize,
            ),
            True: """
                QProgressBar {border: 1px; border-radius: 10px; text-align: right; color: %s; font: %spt;}
                QProgressBar::chunk {background-color: #ffaa00; height: 5px; margin: 0.5px;}
            """
            % (
                color,
                self.fontsize,
            ),
        }
        return data[self.plane]


if __name__ == "__main__":
    pass
