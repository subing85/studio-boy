# Copyright (c) 2022, https:://www.subins-toolkits.com All rights reserved.
# Author: Subin. Gopi (subing85@gmail.com).
# Studio-Pipe Project Management in-house Tool.
# Last modified: 2022:January:04:Tuesday-10:17:38:AM.
# WARNING! All changes made in this file will be lost!.
# Description: studio-pipe python api.


from test import utils
from pipe.core import logger

LOGGER = logger.getLogger(__name__)


class UnitTest(object):
    def __init__(self, **kwargs):
        super(UnitTest, self).__init__(**kwargs)

        self.pipelinepath = utils.pipelinePath()

    def check(self):
        utils.checkPackages()

    def execute(self):
        modules = utils.checkModules()
        utils.checkPackages()
        utils.checkUnusedImport(modules=modules)
        utils.checkBlackFormatting(module=self.pipelinepath)
        self.cleanDevkit()
        print("completed!...")

    def getPackageModles(self, package):
        if package == "all":
            packages = utils.getPackages()
        else:
            packages = [package]
        for each in packages:
            utils.collectPackageModules(each)

    def fixUnusedImport(self, modules=None):
        utils.fixUnusedImport(modules=modules)


if __name__ == "__main__":
    pass
