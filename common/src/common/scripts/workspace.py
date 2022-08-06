import os

from apis.studio import Versions


class Workspace(object):

    eventEnable = True
    eventName = "setWorkspace"
    eventType = "maya"
    eventAuthor = "subin gopi"

    input = dict()
    output = dict()

    @classmethod
    def execute(cls):
        task = cls.input["task"]
        vers = Versions()
        filepath = vers.kindPath("work", task=task)
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        os.startfile(filepath)
        cls.output["workspace"] = filepath
