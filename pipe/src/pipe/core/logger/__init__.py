# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-12:48:14:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core logger.

import os
import sys
import logging
import tempfile


def Logger(**kwargs):
    tempdirname = os.path.join(tempfile.gettempdir(), "studio-pipe")
    if not os.path.isdir(tempdirname):
        os.makedirs(tempdirname)
    filename = kwargs.get("filename") or "pipe"
    filepath = os.path.join(tempdirname, "%s.log" % filename)
    format = "# %(asctime)s %(levelname)6s: %(module)s-line: %(lineno)d | %(message)s"
    date = "%Y/%m/%d %I:%M:%S:%p"
    formatter = logging.Formatter(fmt=format, datefmt=date)
    logging.basicConfig(
        filename=filepath,
        format=format,
        datefmt=date,
        filemode="a",
        level=logging.DEBUG,
    )
    logget = logging.getLogger()
    logget.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    return logget


def getLogger(name):
    logger = logging.getLogger(name)
    format = "# %(asctime)s%(levelname)8s: %(name)s-line: %(lineno)d | %(message)s"
    date = "%Y/%m/%d %I:%M:%S:%p"
    formater = logging.Formatter(fmt=format, datefmt=date)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(formater)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = 0
    return logger


def logTypes():
    types = [
        "info",
        "critical",
        "error",
        "warning",
        "warn",
        "debug",
    ]
    print(types)
    return types


if __name__ == "__main__":
    pass
