# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:04:01:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core status.

from pipe.core import inputs
from pipe.core import project

import json


class Connect(project.Connect):
    def __init__(self, **kwargs):
        super(Connect, self).__init__(**kwargs)

    def statusInputContexts(self):
        input = inputs.Connect("status")
        contexts = input.get()
        return contexts

    def searchTaskStatusContext(self, status):
        input_contexts = self.statusInputContexts()
        contexts = list(
            filter(lambda k: k.get("name") == status, input_contexts)
        )
        if not contexts:
            return
        return contexts[0]


if __name__ == "__main__":
    con = Connect()

    contexts = con.searchTaskStatusContext("Not started")

    print(json.dumps(contexts, indent=4))
