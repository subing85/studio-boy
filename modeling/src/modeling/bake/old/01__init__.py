import os
import sys
import tempfile
import subprocess

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets

# from apis import media
from apis import studio
from pipe import utils
from pipe import resources

from pipe.core import logger
from pipe.utils import qwidgets

# =====================================================================
# from modeling.scripts import uv
# from modeling.scripts import movie
# from modeling.scripts import camera
# from modeling.scripts import generic
# =====================================================================

LOGGER = logger.getLogger(__name__)
CURRENT_PATH = os.path.dirname(__file__)


class Model(QtWidgets.QMainWindow):
    """
    :example
        import shiboken2
        from maya import OpenMayaUI
        from PySide2 import QtWidgets
        from modeling import bake
        qwidget = OpenMayaUI.MQtUtil.mainWindow()
        main_window = shiboken2.wrapInstance(int(qwidget), QtWidgets.QWidget)
        model = bake.Model(parent=main_window, step='model')
        model.show()
    """

    def __init__(self, parent=None, **kwargs):
        super(Model, self).__init__(parent)
        self.step = kwargs.get("step")
        self.iconpath = kwargs.get("iconpath")
        self.format = "tif"
        self.path = tempfile.mktemp(
            self.format, self.step, tempfile.gettempdir()
        )
        self.frames = kwargs.get("frames") or [1]
        self.scriptpath = modeling.scrtptPath()

        self.alignright = (
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        self.resolution = [1024, 1024]
        self.tasks = {}
        self.current_task = None

        self.stud = studio.Connect()

        self.setup_ui()
        self.setup_icons()
        self.setup_tasks()

        LOGGER.info("studio-pipe %s Bake Tool -0.0.1" % self.step)

    def setup_ui(self):
        self.resize(360, 190)
        self.setWindowTitle("Model Bake")
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.gridlayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridlayout.setHorizontalSpacing(10)
        self.gridlayout.setVerticalSpacing(0)
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(self.alignright)
        self.label.setText("Tasks")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.setIconSize(QtCore.QSize(32, 32))
        self.gridlayout.addWidget(self.combobox, 0, 1, 1, 1)
        self.button_workspace = QtWidgets.QPushButton(self)
        self.button_workspace.setText("Workspace")
        self.button_workspace.clicked.connect(self.workspace)
        self.gridlayout.addWidget(self.button_workspace, 1, 1, 1, 1)
        self.button_look = QtWidgets.QPushButton(self)
        self.button_look.setText("Look")
        self.button_look.clicked.connect(self.create_look)
        self.gridlayout.addWidget(self.button_look, 2, 1, 1, 1)
        self.button_mov = QtWidgets.QPushButton(self)
        self.button_mov.setText("Movie")
        self.button_mov.clicked.connect(self.create_movie)
        self.gridlayout.addWidget(self.button_mov, 3, 1, 1, 1)
        self.button_uv = QtWidgets.QPushButton(self)
        self.button_uv.setText("Export-UV")
        self.button_uv.clicked.connect(self.export_uv)
        self.gridlayout.addWidget(self.button_uv, 4, 1, 1, 1)
        self.button_export = QtWidgets.QPushButton(self)
        self.button_export.setText("Export-Scene")
        self.button_export.clicked.connect(self.export_scene)
        self.gridlayout.addWidget(self.button_export, 5, 1, 1, 1)

    def setup_icons(self):
        qwidgets.set_widget_icon(self, self.iconpath)

    def setup_tasks(self):
        LOGGER.info("collecting your %s task" % self.step)
        self.combobox.clear()
        self.combobox.addItem("Select your task!...")
        for task in self.stud.user_tasks(step=self.step):
            header = self.stud.taskheader(task)
            iconpath = qwidgets.encode_icon(
                task["thumbnail_url"]["url"]
            )
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(iconpath),
                QtGui.QIcon.Normal,
                QtGui.QIcon.Off,
            )
            self.combobox.addItem(icon, header)
            self.tasks[header] = task

    def update_task(self):
        self.current_task = None
        header = self.combobox.currentText()
        if header == "Select your task!..." or not header:
            return
        if header not in self.tasks:
            LOGGER.warning("not found such task called %s" % header)
            return
        self.current_task = self.tasks[header]
        return True

    def validate_task(self):
        task = self.update_task()
        if not self.current_task:
            QtWidgets.QMessageBox.warning(
                self,
                "Warning",
                "Select your valid task!...",
                QtWidgets.QMessageBox.Ok,
            )
            return False
        if not os.path.isdir(self.filepath):
            os.makedirs(self.filepath)
            LOGGER.info(
                "create the current %s workspace, %s"
                % (self.step, self.filepath)
            )
        return task

    @property
    def filepath(self):
        kindpath = self.stud.kind_path(self.current_task, "work")
        return kindpath

    def workspace(self):
        validate = self.validate_task()
        if not validate:
            return
        try:
            os.startfile(self.filepath)
        except Exception as error:
            LOGGER.error(str(error))
        LOGGER.warning(
            "already exists the workspace, %s" % self.filepath
        )

    def create_look(self):
        validate = self.validate_task()
        if not validate:
            LOGGER.warning("invalid task")
            return
        kwargs = {
            "format": "tif",
            "filepath": "%s/look" % self.filepath,
            "resolution": self.resolution,
        }
        LOGGER.info("path %s" % self.filepath)
        images = media.Playblast.create(**kwargs)
        script = os.path.join(self.scriptpath, "image.py")
        output = "%s/look.jpg" % self.filepath
        self.stamping(images[-1], script, output=output, display=True)
        utils.delete_files(images)
        LOGGER.info("look, %s" % output)
        QtWidgets.QMessageBox.information(
            self, "information", "done!...", QtWidgets.QMessageBox.Ok
        )

    def stamping(self, image, script, output=None, display=False):
        user = self.stud.current_user
        user_name = "%s %s" % (
            user.get("first_name"),
            user.get("last_name"),
        )
        user_type = self.stud.user_type(user)
        context = {
            "background": self.background,
            "forground": image,
            "project_logo": self.stud.create_project_icon(
                self.current_task["project"]
            ),
            "studio_logo": resources.getStudioLogo(),
            "resolution": self.resolution,
            "output": output,
            "font": "arialbd.ttf",
            "size": 20,
            "task_context": self.task_context,
            "user_context": self.user_context,
        }
        # remove python 2.7 studio-pipe package for execute python 3.7
        utils.remove_temp_env("PYTHONPATH")

        popen = subprocess.Popen(
            [os.environ["PYTHON-EXE"], "-s", script, str(context)],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        popen_err = popen.stderr.readlines()
        for each in popen_err:
            print(each)
        popen_out = popen.stdout.readlines()
        for each in popen_out:
            print(each)
        communicate = popen.communicate()

        # revert back python 2.7 studio-pipe package
        utils.append_temp_env("PYTHONPATH")

        utils.delete_files([context["project_logo"]])
        return output

    def create_movie(self):
        validate = self.validate_task()
        if not validate:
            LOGGER.warning("invalid task")
            return
        LOGGER.info("asset path %s" % self.filepath)
        temppath = "%s/%s/turnaround" % (
            self.filepath,
            self.temp_name,
        )
        default_camera, nodes = camera.create(1, 180)
        kwargs = {
            "format": "tif",
            "filepath": temppath,
            "resolution": self.resolution,
            "fstart": 1,
            "fend": 180,
        }
        images = media.Playblast.multicreate(**kwargs)
        camera.delete_camera(default_camera, nodes)
        moviepath = "%s/turnaround.avi" % self.filepath
        script = os.path.join(self.scriptpath, "movie.py")
        self.batch_movie(
            temppath,
            script,
            output=None,
            display=False,
            moviepath=moviepath,
        )
        LOGGER.info("turnaround %s" % moviepath)
        QtWidgets.QMessageBox.information(
            self, "information", "done!...", QtWidgets.QMessageBox.Ok
        )

    def batch_movie(self, dirname, script, display=False, **kwargs):
        user = self.stud.current_user
        user_name = "%s %s" % (
            user.get("first_name"),
            user.get("last_name"),
        )
        user_type = self.stud.user_type(user)
        context = {
            "background": self.background,
            "images": dirname,
            "project_logo": self.stud.create_project_icon(
                self.current_task["project"]
            ),
            "studio_logo": resources.getStudioLogo(),
            "resolution": self.resolution,
            "font": "arialbd.ttf",
            "size": 20,
            "task_context": self.task_context,
            "user_context": self.user_context,
            "fps": media.TimeUnit.fps,
            "moviepath": kwargs.get("moviepath"),
            "project": display,
            "fstart": kwargs.get("fstart"),
        }
        script = movie.create_script(context)

        # remove python 2.7 studio-pipe package for execute python 3.7
        utils.remove_temp_env("PYTHONPATH")

        popen = subprocess.Popen(
            [os.environ["PYTHON-EXE"], "-s", script, str(context)],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        popen_err = popen.stderr.readlines()
        for each in popen_err:
            print(each)
        popen_out = popen.stdout.readlines()
        for each in popen_out:
            print(each)
        communicate = popen.communicate()

        # revert back python 2.7 stuio pipe package
        utils.append_temp_env("PYTHONPATH")

        dumps = [
            os.path.dirname(dirname),
            script,
            context["project_logo"],
        ]
        utils.delete_files(dumps)

    def export_uv(self):
        validate = self.validate_task()
        if not validate:
            LOGGER.warning("invalid task")
            return
        LOGGER.info("asset path %s" % self.filepath)
        uvpath = "%s/uv.json" % self.filepath
        context = self.list_to_dict(self.filter_task_context)
        uv.exports(uvpath, context)
        LOGGER.info("uv,%s" % uvpath)
        QtWidgets.QMessageBox.information(
            self, "information", "done!...", QtWidgets.QMessageBox.Ok
        )

    def export_scene(self):
        validate = self.validate_task()
        if not validate:
            return
        LOGGER.info("saving your scene to workspace")

        generic.export_scene(self.maya_path, format="mayaAscii")
        LOGGER.info(
            "save your scene to workspace, %s" % self.maya_path
        )
        LOGGER.info(self.maya_path)
        QtWidgets.QMessageBox.information(
            self, "information", "done!...", QtWidgets.QMessageBox.Ok
        )

    @property
    def background(self):
        path = os.path.join(CURRENT_PATH, "images", "background.tiff")
        path = os.path.abspath(path).replace("\\", "/")
        return path

    @property
    def project_path(self):
        return self.stud.project_path

    @property
    def step_suffix_path(self):
        suffix_path = self.stud.step_suffix_path(
            self.current_task, "work"
        )
        return suffix_path

    @property
    def maya_path(self):
        mayapath = self.stud.maya_path(self.current_task, "work")
        return mayapath

    @property
    def temp_maya_path(self):
        mayapath = self.stud.temp_path(".ma")
        return mayapath

    @property
    def temp_name(self):
        return os.path.basename(tempfile.mktemp())

    @property
    def filter_task_context(self):
        if self.current_task["parent"]["type"]:
            context = [
                {"id": self.current_task["id"]},
                {"name": self.current_task["parent"]["name"]},
                {"type": self.current_task["parent"]["type"]["name"]},
                {"step": self.current_task["type"]["name"]},
                {"category": self.current_task["link"][1]["name"]},
                {
                    "project": self.current_task["project"][
                        "full_name"
                    ]
                },
            ]
        else:
            context = [
                {"id": self.current_task["id"]},
                {"name": self.current_task["parent"]["name"]},
                {"step": self.current_task["type"]["name"]},
                {"category": self.current_task["link"][1]["name"]},
                {
                    "project": self.current_task["project"][
                        "full_name"
                    ]
                },
            ]
        return context

    @property
    def task_context(self):
        if self.current_task["parent"]["type"]:
            context = [
                {"name": self.current_task["parent"]["name"]},
                {"type": self.current_task["parent"]["type"]["name"]},
                {"step": self.current_task["type"]["name"]},
                {"category": self.current_task["link"][1]["name"]},
                {
                    "project": self.current_task["project"][
                        "full_name"
                    ]
                },
            ]
        else:
            context = [
                {"name": self.current_task["parent"]["name"]},
                {"step": self.current_task["type"]["name"]},
                {"category": self.current_task["link"][1]["name"]},
                {
                    "project": self.current_task["project"][
                        "full_name"
                    ]
                },
            ]
        return context

    @property
    def user_context(self):
        user = self.stud.current_user
        user_name = "%s %s" % (
            user.get("first_name"),
            user.get("last_name"),
        )
        user_type = self.stud.user_type(user)
        user_context = [
            {user["email"]: "email"},
            {user_name: "name"},
            {user_type: "type"},
            {resources.getDateTime(): "date"},
        ]
        return user_context

    def list_to_dict(self, context):
        dict_context = {}
        for each in context:
            dict_context.update(each)
        return dict_context


if __name__ == "__main__":

    tag = 1

    if tag == 0:
        os.environ["TIAKO-USER-NAME"] = "josbuttler"  # re-do
        os.environ["TIAKO-USER-DISCIPLINE"] = "artist"  # re-do
        os.environ[
            "TIAKO-USER-ID"
        ] = "ef8fffdc-c825-11eb-8f35-0a58ac1e0978"
    if tag == 1:
        os.environ["TIAKO-USER-NAME"] = "davidmiller"  # re-do
        os.environ["TIAKO-USER-DISCIPLINE"] = "artist"  # re-do
        os.environ[
            "TIAKO-USER-ID"
        ] = "1d414c56-c826-11eb-8f35-0a58ac1e0978"
    if tag == 2:
        os.environ[
            "TIAKO-USER-NAME"
        ] = "shaofuzhang@studios.com"  # re-do
        os.environ["TIAKO-USER-DISCIPLINE"] = "supervisor"  # re-do
        os.environ[
            "TIAKO-USER-ID"
        ] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {"wsize": [360, 190]}
    window = Model(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
