import os
import sys
import copy

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from apis import studio
from pipe import resources
from pipe.core import logger
from pipe.utils import qwidgets

from pipe.tools.peon import model
from pipe.widgets import ProgressBar
from pipe.widgets import ProjectList
from pipe.widgets import RootTreeItem
from pipe.widgets import ShotTreeItem
from pipe.widgets import StepParameter
from pipe.widgets import AssetTreeItem
from pipe.widgets import HistoryTreeItem
from pipe.widgets import SequenceTreeItem
from pipe.widgets import SequenceTreeItem
from pipe.widgets import SequenceTreeItem
from pipe.tools.peon.record import History

LOGGER = logger.getLogger(__name__)


from pprint import pprint


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent)

        self.title = "Studio-Pipe Project Management Tool -0.0.1"
        self.titleicon = kwargs.get("titleicon") or [768, 144]
        self.projecticon = kwargs.get("showicon") or [256, 144]
        self.wsize = kwargs.get("wsize") or [1048, 523]
        self.pipe_version = os.getenv("PIPE-VERSION") or "unknown"
        self.iconpath = resources.getIconPath()
        self.browsepath = resources.getBrowsePath()
        self.current_categories = list()

        self.proj = studio.Project()
        self.disp = studio.Discipline()
        self.categories = self.proj.searchCategory(None)
        self.templates = None
        self.asset_types = None
        self.shot_contexts = None

        self.setupUi()
        self.setupDefault()
        self.setupDiscipline()
        self.setupIcons()

    def setupUi(self):
        self.setObjectName("mainwindow_project")
        self.setWindowTitle(self.title)
        self.resize(self.wsize[0], self.wsize[1])
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticallayout = QtWidgets.QVBoxLayout(
            self.centralwidget
        )
        self.horizontallayout = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout)
        self.label_user = QtWidgets.QLabel(self)
        self.label_user.setText("Unknown-User")
        self.label_user.setStyleSheet("font: 87 10pt 'Arial Black';")
        self.label_user.setAlignment(
            QtCore.Qt.AlignLeading
            | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter
        )
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )
        self.label_user.setSizePolicy(size_policy)
        self.horizontallayout.addWidget(self.label_user)
        self.label_version = QtWidgets.QLabel(self)
        self.label_version.setText("PIPE Package Version:")
        self.label_version.setStyleSheet(
            "color:rgb(255,170,0); font: 87 10pt 'Arial Black';"
        )
        self.label_version.setAlignment(
            QtCore.Qt.AlignRight
            | QtCore.Qt.AlignTrailing
            | QtCore.Qt.AlignVCenter
        )
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Fixed,
        )
        self.label_version.setSizePolicy(size_policy)
        self.horizontallayout.addWidget(self.label_version)
        self.horizontallayout_logo = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout_logo)
        self.button_logo = QtWidgets.QPushButton(self)
        self.button_logo.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.button_logo.setSizePolicy(sizePolicy)
        self.horizontallayout_logo.addWidget(self.button_logo)
        spacer_item = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout_logo.addItem(spacer_item)
        self.button_project = QtWidgets.QPushButton(self)
        self.button_project.setFlat(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.button_project.setSizePolicy(sizePolicy)
        self.horizontallayout_logo.addWidget(self.button_project)
        self.horizontallayout_project = QtWidgets.QHBoxLayout()
        self.verticallayout.addLayout(self.horizontallayout_project)
        self.projectList = ProjectList(
            self, context=None, iconsize=self.projecticon
        )
        self.project_context = self.projectList.setupProjects()
        self.horizontallayout_project.addWidget(self.projectList)
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.horizontallayout_project.addWidget(self.splitter)
        self.treewidget = QtWidgets.QTreeWidget(self.splitter)
        self.treewidget.setColumnCount(8)
        self.treewidget.setAlternatingRowColors(True)
        self.treewidget.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.treewidget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems
        )
        self.treewidget.setDragDropMode(
            QtWidgets.QAbstractItemView.DragOnly
        )
        self.widget_param = QtWidgets.QWidget(self.splitter)
        self.verticallayout_param = QtWidgets.QVBoxLayout(
            self.widget_param
        )
        self.splitter_parm = QtWidgets.QSplitter(self)
        self.splitter_parm.setOrientation(QtCore.Qt.Vertical)
        self.verticallayout_param.addWidget(self.splitter_parm)
        self.stepParameter = StepParameter(
            self.splitter_parm, visible=True
        )
        self.groupbox_history = QtWidgets.QGroupBox(
            self.splitter_parm
        )
        self.verticalLayout_history = QtWidgets.QVBoxLayout(
            self.groupbox_history
        )
        self.horizontallayout_history = QtWidgets.QHBoxLayout(
            self.groupbox_history
        )
        self.horizontallayout_history.setSpacing(5)
        self.horizontallayout_history.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_history.addLayout(
            self.horizontallayout_history
        )
        self.button_clear = qwidgets.createClearButton(size=12)
        self.button_clear.setToolTip("Clear")
        self.horizontallayout_history.addWidget(self.button_clear)
        self.button_pin = qwidgets.createPinButton(size=12)
        self.button_pin.setToolTip("Pin")
        self.horizontallayout_history.addWidget(self.button_pin)
        self.button_createall = qwidgets.createRunButton(size=12)
        self.button_createall.setToolTip("create all")
        self.horizontallayout_history.addWidget(self.button_createall)
        spacer_item = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum,
        )
        self.horizontallayout_history.addItem(spacer_item)
        self.treewidget_hsitory = QtWidgets.QTreeWidget(self)
        self.treewidget_hsitory.setHeaderHidden(True)
        self.treewidget_hsitory.setColumnCount(3)
        self.treewidget_hsitory.setAlternatingRowColors(True)
        self.verticalLayout_history.addWidget(self.treewidget_hsitory)
        spacer_item = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred,
        )
        self.verticallayout_param.addItem(spacer_item)
        self.progressbar = ProgressBar(
            self, visible=True, plane=False
        )
        self.verticallayout.addWidget(self.progressbar)
        self.projectList.itemClicked.connect(self.setCurrentProject)
        self.treewidget.itemClicked.connect(
            partial(self.setupParameters, None)
        )
        self.stepParameter.button_remove.clicked.connect(
            self.removeStep
        )
        self.stepParameter.button_create.clicked.connect(
            partial(self.createOrUpdate, False, True)
        )
        self.stepParameter.button_update.clicked.connect(
            partial(self.createOrUpdate, False, False)
        )
        self.button_clear.clicked.connect(self.clearUnPin)
        self.button_pin.clicked.connect(self.setupPin)
        self.button_createall.clicked.connect(
            partial(self.createOrUpdate, True, True)
        )
        self.button_project.clicked.connect(self.reload)

    def setupIcons(self):
        qwidgets.setWidgetIcon(
            self, utils.findIconpath(prefix="project")
        )
        contexts = [
            {
                "widget": self.button_logo,
                "size": self.titleicon,
                "icon": utils.findIconpath(prefix="pipe-project"),
            },
            {
                "widget": self.button_project,
                "size": self.projecticon,
                "icon": utils.findIconpath(prefix="unknown-project"),
            },
        ]
        for context in contexts:
            qwidgets.imageToButton(
                context["widget"],
                context["size"][0],
                context["size"][1],
                locked=True,
                iconpath=context["icon"],
            )

    def setupDefault(self):
        # self.setupClear()
        self.splitter.setSizes([1030, 376])
        self.label_version.setText(
            "PIPE - Package Version: %s" % self.pipe_version
        )
        self.widget_param.hide()
        for index in range(self.treewidget.columnCount()):
            self.treewidget.headerItem().setText(index, "")

    def setupClear(self):
        self.progressbar.clear()

    def setupParametreVisiblility(self, visible):
        self.widget_param.setVisible(visible)
        self.stepParameter.setVisible(visible)
        self.widget_param.show()

    def setupDiscipline(self):
        self.currentdiscipline = self.currentDisciplineContext()
        if not self.currentdiscipline:
            LOGGER.warning("invalid user")
            return
        current_user = "%s: %s [%s]" % (
            self.currentdiscipline["username"],
            self.currentdiscipline["role"],
            self.currentdiscipline["privilege"],
        )
        r, g, b = self.currentdiscipline.get("color")
        self.label_user.setText(current_user)
        self.label_user.setStyleSheet(
            "color:rgb(%s, %s, %s); font: 87 10pt 'Arial Black';"
            % (r, g, b)
        )

    def currentDisciplineContext(self):
        value = os.getenv("PIPE-USER-DISCIPLINE")
        context = self.disp.searchDisciplineContext(value)
        if context:
            context["role"] = value
            context["username"] = os.getenv("PIPE-USER-NAME")
        return context

    def setCurrentProject(self, *args):
        # QtWidgets.QApplication.setOverrideCursor(
        #    QtCore.Qt.CustomCursor.WaitCursor
        # )
        self.setupClear()
        History.clear()
        project_name = args[0].text()
        self.current_project = self.proj._setProject(project_name)
        iconpath = self.projectIconPath(self.current_project)
        iconpath = qwidgets.encodeIcon(iconpath)
        qwidgets.imageToButton(
            self.button_project,
            self.projecticon[0],
            self.projecticon[1],
            locked=True,
            iconpath=iconpath,
        )
        message = "searching  project %s" % project_name
        self.progressbar.setProgress(
            10, message, plane=True, error=False, thread=True
        )

        # self.progressbar.setMessage(message)

        self.proj.getProject()
        self.treewidget.clear()
        self.setupParametreVisiblility(False)

        self.setupCategories()

        self.template_context = (
            self.stepParameter.setupStepTemplates()
        )
        self.asset_type_context = self.stepParameter.setupAssetTypes()
        self.time_unit_context = self.stepParameter.setupFPS()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.progressbar.clear()

    def projectIconPath(self, project):
        iconpath = os.path.join(self.iconpath, "unknown-project.png")
        if project.get("thumbnail_url"):
            if project["thumbnail_url"].get("url"):
                iconpath = project["thumbnail_url"]["url"]
        return iconpath

    def setupCategories(self):
        self.current_categories = self.proj.getProjectCategories()

        message = "searching project categories"

        self.progressbar.setProgress(
            10, message, plane=True, error=False, thread=False
        )
        # self.progressbar.setMessage(message)

        for context in self.current_categories:
            data = utils.searchContext(
                self.categories, "name", value=context["name"]
            )
            if not data:
                LOGGER.warning(
                    'not found category "%s" in the configure'
                    % context["name"]
                )
                return

            category_context = data[0]
            parameter_context = category_context.get(
                "parameter"
            ).copy()
            primary_context = utils.searchContext(
                parameter_context, "primary", value=True
            )
            parameter = utils.searchConetxValues(
                "display-name", primary_context
            )
            self.rootTreeItem = RootTreeItem(
                self.treewidget,
                name=category_context.get("display-name"),
                category=category_context.get("name"),
                parameter=parameter[1:],
                fontsize=category_context.get("fontsize"),
                color=category_context.get("color"),
            )
            self.rootTreeItem.setEntity(context)
            self.rootTreeItem.button.clicked.connect(
                partial(
                    self.addStep,
                    category_context.get("name"),
                    self.rootTreeItem,
                    entity=False,
                )
            )
            self.loadSteps(
                self.rootTreeItem,
                context.get("name"),
                context.get("children"),
                category_context,
            )
        self.progressbar.clear()

    def loadSteps(self, parent, category, steps, context):
        parameter_context = context.get("parameter").copy()
        primary_context = utils.searchContext(
            parameter_context, "name", value=None
        )

        maximum = len(steps) if len(steps) else 1
        self.progressbar.setMaximum(maximum)

        for index, step in enumerate(steps):
            message = self.proj.contextHeader(step)
            message += " (%s)" % step["id"]

            self.progressbar.setProgress(
                index, message, plane=True, error=False, thread=False
            )

            self.addStep(
                category,
                parent,
                step=step,
                context=primary_context,
                entity=True,
                pin=True,
            )

            if not context.get("children"):
                continue
            for child in context.get("children"):
                self.loadSteps(
                    self.stepTreeItem,
                    "shots",
                    step.get("children"),
                    child,
                )
        self.progressbar.clear()

    def getCategoryParameters(self, category):
        contexts = utils.searchContext(
            self.categories, "name", value=category
        )
        if not contexts:
            for each in self.categories:
                if not each.get("children"):
                    continue
                contexts = utils.searchContext(
                    each["children"], "name", value=category
                )
        if not contexts:
            return None
        context = contexts[0].get("parameter")
        return context

    def addStep(self, category, parent, **kwargs):
        self.setupClear()
        step = kwargs.get("step") or None
        context = kwargs.get("context") or self.getCategoryParameters(
            category
        )
        entity = kwargs.get("entity") or False
        pin = kwargs.get("pin") or False
        sequence = kwargs.get("sequence") or None
        inputs = {
            "category": category,
            "fontsize": context[0].get("fontsize"),
            "color": context[0].get("color"),
        }
        if category == "assets":
            self.stepTreeItem = AssetTreeItem(parent, **inputs)
        elif category == "sequence":
            self.stepTreeItem = SequenceTreeItem(parent, **inputs)
            self.stepTreeItem.button.clicked.connect(
                partial(
                    self.addStep,
                    "shots",
                    self.stepTreeItem,
                    entity=False,
                    pin=False,
                    sequence=self.stepTreeItem,
                )
            )
        elif category == "shots":
            self.stepTreeItem = ShotTreeItem(parent, **inputs)
        else:
            self.stepTreeItem = None
            LOGGER.warning("invalid category name")
        if not self.stepTreeItem:
            return
        sequence_step = sequence.entity if sequence else None
        parameter_context = self.setupItems(
            self.stepTreeItem,
            step,
            category,
            context=context,
            sequence=sequence_step,
        )
        History.setWidget(self.stepTreeItem)
        History.setEntity(entity)
        History.setPin(pin)
        History.setCategory(category)
        History.setSequence(sequence_step)
        History.add(parameter_context)
        if not entity:
            self.treewidget.setItemSelected(self.stepTreeItem, True)
            self.treewidget.setItemExpanded(parent, 1)
            self.setupParameters(category, self.stepTreeItem)
        self.treewidget.clearSelection()
        self.setupHistoryItems()

    def setupItems(self, stepTreeItem, step, category, **kwargs):
        context = kwargs.get("context") or self.getCategoryParameters(
            category
        )
        sequence = kwargs.get("sequence") or None
        stepTreeItem.setEntity(step)
        # get the value from entity or widgets
        parameter_context = self.stepParameter.parameterContext(
            category, context, step=step, parent=sequence
        )
        primary_context = utils.searchContext(
            parameter_context, "primary", value=True
        )
        stepTreeItem.setupAllParameters(primary_context)
        self.setupHistoryItems()
        return parameter_context

    def setupParameters(self, category, *args):
        History.setWidget(args[0])
        self.setupClear()
        if not category:
            if not History.widgetitem.parent():
                History.setWidget(None)
                self.setupParametreVisiblility(False)
                return
            category = History.widgetitem.toolTip(1)
        if not category:
            History.setWidget(None)
            self.setupParametreVisiblility(False)
            return
        if category == "assets":
            self.splitter_parm.setSizes([262, 500])
        else:
            self.splitter_parm.setSizes([534, 228])
        self.setupParametreVisiblility(True)
        context = History.getContext()
        History.setLive(context)
        self.stepParameter.setupParameterWidgets(category, context)

    def setupHistoryItems(self):
        self.setupClear()
        self.treewidget_hsitory.clear()
        index = 1
        for each in History.context:
            entities = utils.searchContext(each, "entity", value=None)
            if entities:
                if entities[0].get("entity"):
                    continue
            categories = utils.searchContext(
                each, "category", value=None
            )
            parents = utils.searchContext(
                each, "widgetitem", value=None
            )
            pins = utils.searchContext(each, "pin", value=None)
            pin = True if pins else False
            kwargs = {
                "category": categories[0].get("category"),
                "item": parents[0].get("widgetitem"),
                "index": index,
                "pin": pin,
            }
            HistoryTreeItem(self.treewidget_hsitory, **kwargs)
            index += 1

    def setupPin(self):
        self.setupClear()
        default = self.stepParameter.hasDefaultValue(History.live)
        if default:
            message = "Name parameter value is default update the value and try"
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            return
        self.stepParameter.updateValues(History.live, pin=True)
        self.setupHistoryItems()

    def clearUnPin(self):
        self.setupClear()
        replay = QtWidgets.QMessageBox.question(
            self,
            "Question",
            "Are you sure, want to clear the unused items!...",
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if replay == QtWidgets.QMessageBox.No:
            LOGGER.warning("Abort the clear the unused items!...")
            return
        self.stepParameter.clearHistory(History.context, entity=False)
        self.setupHistoryItems()

    def removeStep(self):
        self.setupClear()
        replay = QtWidgets.QMessageBox.question(
            self,
            "Question",
            "Are you sure, want to remove the step item!...",
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if replay == QtWidgets.QMessageBox.No:
            LOGGER.warning("Abort the  remove the step item!...")
            return
        message = None
        if History.live not in History.context:
            message = "invalid current item context."
        if History.entity:
            message = "already created, try with newly added item!..."
        if message:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            return
        History.remove(item=History.live)
        History.widgetitem.removeItem()
        self.setupParametreVisiblility(False)

    def createOrUpdate(self, all, create):
        entity = False if all else True
        self.setupClear()
        vaild, message = History.validate(
            all=all, create=create, entity=entity
        )
        if not vaild:
            QtWidgets.QMessageBox.warning(
                self, "Warning", message, QtWidgets.QMessageBox.Ok
            )
            return False
        keyworld = "create" if create else "update"
        replay = QtWidgets.QMessageBox.question(
            self,
            "Question",
            "Are you sure, want to %s step!..." % keyworld,
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No,
        )
        if replay == QtWidgets.QMessageBox.No:
            LOGGER.warning("Abort the % step!..." % keyworld)
            return False
        self.setupPin()
        histories = History.get(all=all)
        self.progressbar.show()
        self.progressbar.setMaximum(len(histories))
        valid = False
        for index, history in enumerate(histories):
            context = History.toContext(history)
            widgetitem = context.get("widgetitem")
            if create and context.get("entity"):
                continue
            """
            example (context)
                {'assembly': [{'color': [170, 85, 255],
                               'fontsize': 14,
                               'id': '3189b06f-58b5-4281-8320-264514af535f',
                               'name': 'girl',
                               'type': 'AssetBuild'},
                              {'color': [170, 85, 255],
                               'fontsize': 14,
                               'id': '6dcb54ca-e940-40e7-936e-9f2267390c10',
                               'name': 'boy',
                               'type': 'AssetBuild'}],
                 'category': 'shots',
                 'entity': False,
                 'fend': 1025,
                 'fstart': 1001,
                 'name': '102',
                 'sequence': <dynamic ftrack Sequence object 1610861487176>,
                 'step': None,
                 'tag': False,
                 'template': '3D',
                 'widgetitem': <pipe.widgets.ShotTreeItem object at 0x000001770ED5F948>}
            """
            message = "creating, %s - %s" % (
                context["category"],
                context["name"],
            )
            self.progressbar.setProgress(
                index, message, plane=True, error=False, thread=False
            )
            QtWidgets.QApplication.setOverrideCursor(
                QtCore.Qt.CustomCursor.WaitCursor
            )

            try:
                valid, message, step = model.doIt(create, **context)
            except Exception as error:
                LOGGER.error(str(error))
                valid, message, step = False, str(error), None

            QtWidgets.QApplication.restoreOverrideCursor()

            if not valid:
                QtWidgets.QMessageBox.warning(
                    self, "Warning", message, QtWidgets.QMessageBox.Ok
                )
                self.progressbar.setProgress(
                    index,
                    message,
                    percentage=True,
                    error=True,
                    thread=False,
                )

            continue

            message = "created, %s (%s - %s)" % (
                step["id"],
                context["category"],
                context["name"],
            )
            self.progressbar.setProgress(
                index,
                message,
                percentage=True,
                error=False,
                thread=False,
            )
            parameter_context = self.setupItems(
                widgetitem, step, context["category"], context=None
            )
            History.update("entity", True, live=history)
            History.update("pin", True, live=history)
            if isinstance(widgetitem, SequenceTreeItem):
                History.update("sequence", step, live=history)
        self.progressbar.setProgress(
            len(histories),
            "success!...",
            percentage=False,
            error=False,
            thread=False,
        )
        QtWidgets.QMessageBox.information(
            self,
            "information",
            "success!...",
            QtWidgets.QMessageBox.Ok,
        )
        return True

    def reload(self):
        print("\nHistory.context")
        from pprint import pprint

        for each in History.context:
            pprint(each)
            print("\n")
        print("history length", len(History.context))

    def example(self):
        """
        example
            tag = 0
            if tag == 0:
                os.environ["PIPE-USER-NAME"] = "subingopi"  # re-do
                os.environ["PIPE-USER-DISCIPLINE"] = "Administrator"  # re-do
                os.environ["PIPE-USER-ID"] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"
            if tag == 1:
                os.environ["PIPE-USER-NAME"] = "leandra.rosa"  # re-do
                os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
                os.environ["PIPE-USER-ID"] = "72e1e0f0-a058-11e9-a359-d27cf242b68b"
            if tag == 2:
                os.environ["PIPE-USER-NAME"] = "tony.williams"  # re-do
                os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
                os.environ["PIPE-USER-ID"] = "ea90cf68-a057-11e9-8545-d27cf242b68b"

            app = QtWidgets.QApplication(sys.argv)
            kwargs = {}
            window = Window(parent=None, **kwargs)
            window.show()
            sys.exit(app.exec_())
        """
        pass


if __name__ == "__main__":
    tag = 0
    if tag == 0:
        os.environ["PIPE-USER-NAME"] = "subingopi"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "Administrator"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "bcdf57b0-acc6-11e1-a554-f23c91df1211"
    if tag == 1:
        os.environ["PIPE-USER-NAME"] = "leandra.rosa"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "72e1e0f0-a058-11e9-a359-d27cf242b68b"
    if tag == 2:
        os.environ["PIPE-USER-NAME"] = "tony.williams"  # re-do
        os.environ["PIPE-USER-DISCIPLINE"] = "User"  # re-do
        os.environ[
            "PIPE-USER-ID"
        ] = "ea90cf68-a057-11e9-8545-d27cf242b68b"

    app = QtWidgets.QApplication(sys.argv)
    kwargs = {}
    window = Window(parent=None, **kwargs)
    window.show()
    sys.exit(app.exec_())
