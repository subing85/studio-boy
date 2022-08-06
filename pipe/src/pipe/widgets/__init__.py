from pipe.widgets import projects
from pipe.widgets import property
from pipe.widgets import treeitems
from pipe.widgets import parameter
from pipe.widgets import progressbar


class ProjectList(projects.Connect):
    def __init__(self, parent, **kwargs):
        super(ProjectList, self).__init__(parent, **kwargs)


class ParametrTreeItem(treeitems.ParametrTreeItem):
    def __init__(self, parent, **kwargs):
        super(ParametrTreeItem, self).__init__(parent, **kwargs)


class RootTreeItem(treeitems.RootTreeItem):
    def __init__(self, parent, **kwargs):
        super(RootTreeItem, self).__init__(parent, **kwargs)


class AssetTreeItem(treeitems.AssetTreeItem):
    def __init__(self, parent, **kwargs):
        super(AssetTreeItem, self).__init__(parent, **kwargs)


class SequenceTreeItem(treeitems.SequenceTreeItem):
    def __init__(self, parent, **kwargs):
        super(SequenceTreeItem, self).__init__(parent, **kwargs)


class ShotTreeItem(treeitems.ShotTreeItem):
    def __init__(self, parent, **kwargs):
        super(ShotTreeItem, self).__init__(parent, **kwargs)


class HistoryTreeItem(treeitems.HistoryTreeItem):
    def __init__(self, parent, **kwargs):
        super(HistoryTreeItem, self).__init__(parent, **kwargs)


class StepParameter(parameter.Connect):
    def __init__(self, parent, **kwargs):
        super(StepParameter, self).__init__(parent, **kwargs)


class WidgetTreeItem(treeitems.WidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(WidgetTreeItem, self).__init__(parent, **kwargs)


class RootWidgetTreeItem(treeitems.RootWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(RootWidgetTreeItem, self).__init__(parent, **kwargs)


class AssetWidgetTreeItem(treeitems.AssetWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(AssetWidgetTreeItem, self).__init__(parent, **kwargs)


class SequenceWidgetTreeItem(treeitems.SequenceWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(SequenceWidgetTreeItem, self).__init__(parent, **kwargs)


class ShotWidgetTreeItem(treeitems.ShotWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(ShotWidgetTreeItem, self).__init__(parent, **kwargs)


class TaskWidgetTreeItem(treeitems.TaskWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(TaskWidgetTreeItem, self).__init__(parent, **kwargs)


class KindsWidgetTreeItem(treeitems.KindsWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(KindsWidgetTreeItem, self).__init__(parent, **kwargs)


class VersionWidgetTreeItem(treeitems.VersionWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(VersionWidgetTreeItem, self).__init__(parent, **kwargs)


class CommonWidgetTreeItem(treeitems.CommonWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(CommonWidgetTreeItem, self).__init__(parent, **kwargs)


class BuildWidgetTreeItem(treeitems.BuildWidgetTreeItem):
    def __init__(self, parent, **kwargs):
        super(BuildWidgetTreeItem, self).__init__(parent, **kwargs)


class EntityProperty(property.Connect):
    def __init__(self, parent, **kwargs):
        super(EntityProperty, self).__init__(parent, **kwargs)


class ProgressBar(progressbar.Connect):
    def __init__(self, parent, **kwargs):
        super(ProgressBar, self).__init__(parent, **kwargs)


if __name__ == "__main__":
    pass
