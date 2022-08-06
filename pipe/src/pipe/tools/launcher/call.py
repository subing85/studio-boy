# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:16:Sunday-12:45:40:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core launcher call.

import os
import sys

from PySide2 import QtWidgets

from apis import studio
from pipe.core import logger
from pipe.tools import launcher

LOGGER = logger.getLogger(__name__)


def execute():
    logn = studio.Login()
    appn = QtWidgets.QApplication(sys.argv)

    messages = None
    if not logn.isValidLogin():
        messages = [
            "not yet loin, login first and try to launch the Studio-Pipe Project",
            'for example, pipe --set-username "name of the user name"',
        ]
    else:
        kwargs = {
            "size": [640, 535],
        }
        window = launcher.Window(parent=None, **kwargs)
        window.show()
        sys.exit(appn.exec_())
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


if __name__ == "__main__":
    execute()
