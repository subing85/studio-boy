import os
import sys

from PySide2 import QtWidgets

from apis import studio
from pipe.core import logger
from pipe.tools import project

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
    elif not logn.isSuperUser(userid=None):
        messages = [
            "current user not have the privilege to launch Studio-Pipe Project"
        ]
    else:
        kwargs = {
            "size": [361, 307],
        }
        window = project.Window(parent=None, **kwargs)
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
