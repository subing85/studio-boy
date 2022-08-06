import importlib

from common import validate

importlib.reload(validate)


class Groom(validate.Window):

    taskType = "Groom"

    def __init__(self, parent=None, **kwargs):
        super(Groom, self).__init__(parent, **kwargs)

        self.iconsize = kwargs.get("iconsize", [18, 18])
        self.wsize = kwargs.get("wsize", [500, 340])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Groom(parent=None)
    window.show()
    sys.exit(app.exec_())
