import glob
import threading

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from functools import partial

from pipe import utils
from pipe.core import logger
from pipe.utils import qwidgets
from pipe.tools.mytasks import stepwidgets

MAIN = None
LOGGER = logger.getLogger(__name__)

from pprint import pprint


def updatePrivileges():
    current_status = MAIN.current_task["status"]["name"]

    print("current_status", current_status)
    status_context = MAIN.stus.searchTaskStatusContext(current_status)

    if not status_context:
        LOGGER.warning(
            "invalid status context, please update the core.inputs.status.json"
        )
        return

    trigger = status_context.get("trigger")

    stepwidgets.MAIN = MAIN
    context = stepwidgets.getTriggerContext(trigger)

    qwidgets.clearWidgets(context.get("clear"))
    qwidgets.setValue(context.get("values"))
    qwidgets.setEnableWidgets(context.get("disable"), enable=False)
    qwidgets.setEnableWidgets(context.get("enable"), enable=True)

    MAIN.hideUserWidgets()
    qwidgets.widgetVisibility(context.get("visibility"), True)

    if status_context.get("description"):
        MAIN.setupStatusIcon(status_context.get("icon"))
        MAIN.label_tag.setText(
            " Tag: %s" % status_context.get("description")
        )
    else:
        MAIN.label_tag.setText("Tag: unknown")

    print("\nstatus_context", status_context.get("kind"))
    pprint(status_context)
    setupVersions(status_context.get("kind"))
    setupComponents()


def loadTasks(tasks, thread=False):
    if not MAIN.currentdiscipline:
        LOGGER.warning("not find user and user discipline")
        return
    privilege = MAIN.currentdiscipline["privilege"]
    LOGGER.info("privilege, %s" % privilege)
    LOGGER.info("total task, %s" % len(tasks))
    LOGGER.info("loading tasks, please wait")
    tasks = sorted(tasks, key=lambda k: (k["created_at"]))
    for index, task in enumerate(tasks):
        if not MAIN.stop_thread:
            break
        if thread:
            thread_state = threading.Condition()
            task_thread = threading.Thread(
                target=addTaskItem, args=([task, index + 1])
            )
            task_thread.daemon = True
            task_thread.start()
        else:
            addTaskItem(task, index + 1)
    LOGGER.info("loaded tasks, completed")


def addTaskItem(task, index):
    if not MAIN.stop_thread:
        return
    header = MAIN.task.contextHeader(task)
    LOGGER.info("loading tasks, %s. %s" % (index, header))
    iconpath = qwidgets.encodeIcon(task["thumbnail_url"]["url"])

    item = QtWidgets.QTreeWidgetItem(MAIN.treewidget_tasks)
    item.setText(0, str(index))
    item.setText(1, header)
    qwidgets.setWidgetIcon(item, iconpath, index=1)
    MAIN.tasks_items[header] = task["id"]


def setupVersions(kind):
    if not kind:
        return
    LOGGER.info("kind: %s" % kind)
    MAIN.label_versions.setText("Latest %s versions" % kind)
    MAIN.vers.authorization()
    # ===============================================================================================
    # submitted_versions = MAIN.vers.searchKindVersions(
    #     taskid=MAIN.current_task["id"], kind="submit"
    # )
    # ===============================================================================================

    submitted_versions = MAIN.vers.searchKindVersions(
        taskid=MAIN.current_task["id"], kind=kind
    )

    MAIN.combobox_versions.clear()
    if submitted_versions:
        for each in submitted_versions:
            each_version = MAIN.vers.findVersionFromAssetVersion(each)
            MAIN.combobox_versions.addItem(str(each_version))
    else:
        MAIN.combobox_versions.addItem("Null")
    MAIN.setupNextSemanticVersion()


def setupComponents():
    task_name = MAIN.current_task["type"]["name"]
    context = MAIN.comp.taskComponents(task_name)
    if not context:
        return
    components = context.get("components")
    if not components:
        LOGGER.warning(
            'not found any components in the task name called "%s"'
            % task_name
        )
        return
    MAIN.setupComponents(components)


def setupComponentItems(parent, typed, directory, formats=None):
    if typed == "dirname":
        valid_files = utils.collectSpecificFiles(
            directory, formats=formats
        )
    else:
        valid_files = [directory]
    for each in valid_files:
        item = QtWidgets.QTreeWidgetItem(parent)
        qwidgets.setItemFont(item, 1, size=10, bold=True)
        item.setText(1, each)
        item.setCheckState(1, QtCore.Qt.Checked)
        MAIN.treewidget.setItemExpanded(parent, 1)


def getSelectedComponentItems(treewidget):
    selected_items = treewidget.selectedItems()
    context = {}
    for each in selected_items:
        parent = each.parent()
        if parent:
            if parent in context:
                if each in context[parent]:
                    continue
                context[parent].append(each)
            else:
                context.setdefault(parent, []).append(each)
        else:
            chidren = [
                each.child(x) for x in range(each.childCount())
            ]
            context[each] = chidren
    return context


def searchComponentItems(treewidget):  # invalid function to remove
    widget_item = treewidget.invisibleRootItem()
    stack = [widget_item]
    items = {}
    while stack:
        item = stack.pop()
        if item.parent():
            items.setdefault(item.parent(), item)
        if not item.childCount():
            continue
        chidren = [item.child(x) for x in range(item.childCount())]
        stack.extend(chidren)
    return items
