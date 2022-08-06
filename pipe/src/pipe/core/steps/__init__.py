# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-01:04:54:PM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe core steps.

from pipe.core import project


class Connect(project.Connect):
    def __init__(self, **kwargs):
        super(Connect, self).__init__(**kwargs)


if __name__ == "__main__":
    pass
