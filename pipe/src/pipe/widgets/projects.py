import os

from PySide2 import QtCore
from PySide2 import QtWidgets

from apis import studio
from pipe import resources
from pipe.utils import qwidgets


class Connect(QtWidgets.QListWidget):
    def __init__(self, parent, **kwargs):
        super(Connect, self).__init__(parent)

        self.iconsize = kwargs.get("iconsize") or [256, 144]
        self.context = kwargs.get("context")
        self.setMinimumSize(QtCore.QSize(self.iconsize[0] + 10, 0))
        self.setMaximumSize(
            QtCore.QSize(self.iconsize[0] + 10, 16777215)
        )
        self.setIconSize(
            QtCore.QSize(self.iconsize[0], self.iconsize[1])
        )
        qwidgets.setListIconWidget(self)

    def setupProjects(self):
        self.context = self.context or self.getProjectContext()
        self.clear()
        for each in self.context:
            iconpath = self.projectIconPath(each)
            item = qwidgets.addListWidgetItem(
                self,
                each["name"],
                iconpath=iconpath,
            )
        return self.context

    def getProjectContext(self):
        proj = studio.Project()
        contexts = proj.getAllProjects()
        return contexts

    def projectIconPath(self, project):
        iconpath = os.path.join(
            resources.getIconPath(), "unknown-project.png"
        )
        if project.get("thumbnail_url"):
            if project["thumbnail_url"].get("url"):
                iconpath = project["thumbnail_url"]["url"]
        return iconpath


if __name__ == "__main__":
    pass
