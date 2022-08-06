import importlib

from common import bake

importlib.reload(bake)


class Lookdev(bake.Window):

    taskType = "Lookdev"

    def __init__(self, parent=None, **kwargs):
        super(Lookdev, self).__init__(parent, **kwargs)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [400, 265])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Lookdev(parent=None)
    window.show()
    sys.exit(app.exec_())
