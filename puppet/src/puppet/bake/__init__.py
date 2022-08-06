import importlib

from common import bake

importlib.reload(bake)


class Puppet(bake.Window):

    taskType = "Puppet"

    def __init__(self, parent=None, **kwargs):
        super(Puppet, self).__init__(parent, **kwargs)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [400, 310])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Puppet(parent=None)
    window.show()
    sys.exit(app.exec_())
