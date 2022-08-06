import importlib

from common import bake

importlib.reload(bake)


class Modeling(bake.Window):

    taskType = "Modeling"

    def __init__(self, parent=None, **kwargs):
        super(Modeling, self).__init__(parent, **kwargs)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [400, 235])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Modeling(parent=None)
    window.show()
    sys.exit(app.exec_())
