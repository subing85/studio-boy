import os
import sys
import importlib

CURRENT_PATH = os.path.dirname(__file__)
VERSION = os.path.basename(os.path.dirname(CURRENT_PATH))
REPOSITORY = "pipe"


def MODULES():
    modules = [
        "pipe.widgets",
        "pipe.widgets.parameter",
        "pipe.widgets.progressbar",
        "pipe.widgets.treeitems",
        "pipe.widgets.projects",
        "pipe.widgets.property",
        "pipe.tools",
        "pipe.tools.applications",
        "pipe.tools.browser.call",
        "pipe.tools.browser.main",
        "pipe.tools.launcher",
        "pipe.tools.launcher.call",
        "pipe.tools.login",
        "pipe.tools.login.call",
        "pipe.tools.mytasks",
        "pipe.tools.mytasks.call",
        "pipe.tools.mytasks.setup",
        "pipe.tools.mytasks.stepwidgets",
        "pipe.tools.packages",
        "pipe.tools.peon",
        "pipe.tools.peon.call",
        "pipe.tools.peon.model",
        "pipe.tools.peon.record",
        "pipe.tools.project",
        "pipe.tools.project.call",
        "pipe.tools.task",
        "pipe.tools.task.call",
        "pipe.tools.task.table",
        "pipe.tools.warehouse",
        "pipe.tools.warehouse.actions",
        "pipe.core",
        "pipe.core.applications",
        "pipe.core.attributes",
        "pipe.core.components",
        "pipe.core.console",
        "pipe.core.dependency",
        "pipe.core.discipline",
        "pipe.core.ftrack",
        "pipe.core.inputs",
        "pipe.core.kinds",
        "pipe.core.language",
        "pipe.core.logger",
        "pipe.core.login",
        "pipe.core.packages",
        "pipe.core.project",
        "pipe.core.status",
        "pipe.core.steps",
        "pipe.core.tasks.approved",
        "pipe.core.tasks.declined",
        "pipe.core.tasks.manifest",
        "pipe.core.tasks.publish",
        "pipe.core.tasks.setStatus",
        "pipe.core.tasks.start",
        "pipe.core.tasks.submit",
        "pipe.core.tasks",
        "pipe.core.versions.download",
        "pipe.core.versions",
        "pipe.resources",
        "pipe.utils",
        "pipe.utils.qwidgets",
    ]
    return modules


def RELOAD():
    invalids = []
    for index, each in enumerate(MODULES()):
        try:
            module = importlib.import_module(each)
            print("\t\t %s. %s" % (index + 1, module))
        except Exception as error:
            module = None
            print(
                "\t\t %s reload error, %s [%s]"
                % (index + 1, error, each)
            )
            invalids.append(error)
        if not module:
            continue
        if sys.version_info[:2] >= (3, 4):
            importlib.reload(module)
        else:
            reload(module)
    if invalids:
        return False
    return True
