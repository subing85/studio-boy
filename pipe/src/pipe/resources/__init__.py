# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-04:44:19:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core resources.

import os
import json
import arrow

from datetime import datetime

CURRENT_PATH = os.path.dirname(__file__)


def getPipeVersion():
    return "0.0.1"


def getIconPath():
    return os.path.join(CURRENT_PATH, "icons")


def getInputPath():
    return os.path.join(CURRENT_PATH, "inputs")


def getInputData(name, enable=False):
    path = os.path.join(getInputPath(), "%s.json" % name)
    data = getData(path)
    if not data.get("enable"):
        return None
    if not enable:
        return data["data"]
    enabled_data = list(
        filter(lambda k: k["enable"] == True, data["data"])
    )
    return enabled_data


def getData(path):
    if not os.path.isfile(path):
        raise IOError("not found path <%s>" % path)
    with open(path, "r") as file:
        data = json.load(file)
        return data


def getDateTime(context=None):
    now = context.now() if context else datetime.now()
    date_time = now.strftime("%Y:%m:%d-%I:%M:%p")
    return date_time


def getDateTimes(context=None):
    now = context.now() if context else datetime.now()
    date_time = now.strftime("%Y:%B:%d:%A-%I:%M:%S:%p")
    return date_time


def getTimeToDatetime(timestamp):
    date_time = datetime.fromtimestamp(timestamp).strftime(
        "%Y:%B:%d:%A-%I:%M:%S:%p"
    )
    return date_time


def getBrowsePath():
    path = os.getenv("PROJECT-PATH")
    if not path:
        path = os.path.expanduser("~/Documents")
    elif not os.path.isdir(path):
        path = os.path.expanduser("~/Documents")
    return path


def getStudioLogo():
    path = os.path.join(getIconPath(), "studio-pipe-logo.png")
    path = os.path.abspath(path).replace("\\", "/")
    return path


def getPipeLogo():
    path = os.path.join(getIconPath(), "pipe-logo.png")
    path = os.path.abspath(path).replace("\\", "/")
    return path


def getSubinsToolkits():
    toolkits = "https://www.subins-toolkits.com"
    return toolkits


def getPipeText():
    text = "www.subins-toolkits.com"
    return text


if __name__ == "__main__":
    pass
