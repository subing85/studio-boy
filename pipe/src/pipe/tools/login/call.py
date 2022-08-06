import sys

from PySide2 import QtWidgets

from apis import studio
from pipe.tools import login


def execute():
    appn = QtWidgets.QApplication(sys.argv)
    kwargs = {
        "size": [650, 400],
    }
    window = login.Window(parent=None, **kwargs)
    window.show()
    sys.exit(appn.exec_())


if __name__ == "__main__":
    execute()
