# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe user task Management in-house Tool.
# Last modified:2022:January:26:Wednesday-08:35:59:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core launcher call.

import os
import sys

from PySide2 import QtWidgets

from apis import studio
from pipe.core import logger
from pipe.tools import mytasks


LOGGER = logger.getLogger(__name__)


def execute():
    logn = studio.Login()
    proj = studio.Project()

    appn = QtWidgets.QApplication(sys.argv)

    messages = None
    if not logn.isValidLogin():
        messages = [
            "not yet loin, login first and check-in project",
            'for example, pipe --set-username "name of the user name"',
        ]
    if not proj.isInProject():
        messages = [
            "not check-in the project",
            'for example to check-in project, pipe --set-project "name of the project"',
        ]

    if messages:
        QtWidgets.QMessageBox.critical(
            None,
            "critical",
            "Not able to launch Studio-Pipe Project\n\n%s"
            % "\n".join(messages),
            QtWidgets.QMessageBox.Ok,
        )
        print("\n")
        for message in messages:
            LOGGER.critical(message)
        return

    kwargs = {
        "wsize": [1600, 940],
    }
    window = mytasks.Window(parent=None, **kwargs)
    window.show()
    sys.exit(appn.exec_())


if __name__ == "__main__":
    execute()
