# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2021:December:30:Thursday-10:42:28:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe python api.

from pipe.core import login
from pipe.core import kinds
from pipe.core import steps
from pipe.core import tasks
from pipe.core import event
from pipe.core import media
from pipe.core import status
from pipe.core import inputs
from pipe.core import project
from pipe.core import packages
from pipe.core import language
from pipe.core import versions
from pipe.core import discipline
from pipe.core import attributes
from pipe.core import dependency
from pipe.core import components
from pipe.core import applications


import importlib

importlib.reload(media)


class Login(login.Connect):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)


class Project(project.Connect):
    def __init__(self, **kwargs):
        super(Project, self).__init__(**kwargs)


class Attributes(attributes.Connect):
    def __init__(self, **kwargs):
        super(Attributes, self).__init__(**kwargs)


class Applications(applications.Connect):
    def __init__(self, **kwargs):
        super(Applications, self).__init__(**kwargs)


class Status(status.Connect):
    def __init__(self, **kwargs):
        super(Status, self).__init__(**kwargs)


class Steps(steps.Connect):
    def __init__(self, **kwargs):
        super(Steps, self).__init__(**kwargs)


class Tasks(tasks.Connect):
    def __init__(self, **kwargs):
        super(Tasks, self).__init__(**kwargs)


class Versions(versions.Connect):
    def __init__(self, **kwargs):
        super(Versions, self).__init__(**kwargs)


class Language(language.Connect):
    def __init__(self, **kwargs):
        super(Language, self).__init__(**kwargs)


class Discipline(discipline.Connect):
    def __init__(self, **kwargs):
        super(Discipline, self).__init__(**kwargs)


class Components(components.Connect):
    def __init__(self, **kwargs):
        super(Components, self).__init__(**kwargs)


class Kinds(kinds.Connect):
    def __init__(self, **kwargs):
        super(Kinds, self).__init__(**kwargs)


class Inputs(inputs.Connect):
    typed = None

    def __init__(self, typed=typed, **kwargs):
        super(Inputs, self).__init__(typed, **kwargs)


class MyTask(inputs.Connect):
    typed = "mytask"

    def __init__(self, typed=typed, **kwargs):
        super(MyTask, self).__init__(typed, **kwargs)


class Dependency(dependency.Connect):
    def __init__(self, task=None):
        super(Dependency, self).__init__(task)


class Event(event.Connect):
    def __init__(self, item, **kwargs):
        super(Event, self).__init__(item, **kwargs)


class Packages(packages.Connect):
    def __init__(self):
        super(Packages, self).__init__()


class Media(media.Connect):
    def __init__(self, **kwargs):
        super(Media, self).__init__()


if __name__ == "__main__":
    pass
