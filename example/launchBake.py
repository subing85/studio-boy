import os
import sys

from PySide2 import QtWidgets

from common import bake

os.environ["PIPE-USER-EMAIL"] = "subing85@gmail.com"
os.environ["PIPE-USER-ID"] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"
os.environ["PIPE-USER-NAME"] = "subingopi"
os.environ["PIPE-USER-DISCIPLINE"] = "Administrator"

os.environ["PROJECT-NAME"] = "RAR"
os.environ["PROJECT-FULL-NAME"] = "Raja and Rani"
os.environ["PROJECT-ID"] = "57cfc315-c96d-4031-89f6-110ad66c0cbd"
os.environ[
    "PROJECT-THUMBNAIL"
] = "616d4835-a2a9-4db1-923b-84945aa45123"
os.environ["PROJECT-PATH"] = "Z:/projects/RAR"


os.environ["MAYA_VERSION"] = "maya2022"
os.environ[
    "MAYA_PLUG_IN_PATH"
] = "Z:/devkit/pipeline/resources/maya2022/plug-ins"
os.environ[
    "MAYA_SCRIPT_PATH"
] = "Z:/devkit/pipeline/resources/maya2022/scripts"
os.environ[
    "MAYA_SHELF_PATH"
] = "Z:/devkit/pipeline/resources/maya2022/shelves"
os.environ["PIPE-APPLICATION-NAME"] = "maya2022"


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    kwargs = {"step": "modeling"}
    window = bake.Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
