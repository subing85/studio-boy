import os
import stat
import time
import shutil
import tempfile

from pipe.core import logger
from common import resources


LOGGER = logger.getLogger(__name__)
from pprint import pprint


class Create(object):
    @classmethod
    def tempDirectory(cls, name="studio-pipe"):
        tempdir = resources.setPathResolver(
            tempfile.mktemp("", name, tempfile.gettempdir())
        )
        os.makedirs(tempdir)
        LOGGER.info("created temp directory, %s" % tempdir)
        return tempdir

    @classmethod
    def tempFile(cls):
        # ===========================================================================================
        # filepath = resources.setPathResolver(
        #     tempfile.mktemp(
        #         "/render.%s" % extension, extension.upper(), tempfile.gettempdir()
        #     )
        # )
        # ===========================================================================================
        filepath = resources.setPathResolver(
            tempfile.mktemp("/render", tempfile.gettempdir())
        )

        os.makedirs(os.path.dirname(filepath))
        LOGGER.info(
            "created temp directory, %s" % os.path.dirname(filepath)
        )
        return filepath

    @classmethod
    def directory(cls, directory, timestamp=None, force=False):
        timestamp = timestamp or time.time()
        splitext = os.path.splitext(directory)
        if splitext[1]:
            directory = os.path.dirname(directory)
        if force and os.path.isdir(directory):
            cls.removeAll(directory)
        else:
            LOGGER.warning("already exist the directory, %s" % directory)
            return
        
        if os.path.isdir(directory):
            LOGGER.warning("already exists directory, %s" % directory)
            return

        os.makedirs(directory)
        os.utime(directory, (timestamp, timestamp))
        LOGGER.info("created new directory, %s" % directory)

    @classmethod
    def removeDirectory(cls, directory):
        try:
            os.chmod(directory, stat.S_IWRITE)
        except Exception as error:
            LOGGER.error(error)
        removed = False
        try:
            shutil.rmtree(directory)
            removed = True
        except Exception as error:
            removed = False
        return removed

    @classmethod
    def removeFilepath(cls, filepath):
        try:
            os.chmod(filepath, stat.S_IWRITE)
        except Exception as error:
            LOGGER.error(error)
        try:
            os.remove(filepath)
        except Exception as error:
            LOGGER.error(error)

    @classmethod
    def removeAll(cls, directory):
        removed = cls.removeDirectory(directory)
        LOGGER.info("removed, %s" % directory)
        if removed:
            return removed
        for dir, folder, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(dir, file)
                cls.removeFilepath(filepath)
        removed = cls.removeDirectory(directory)
        return removed

    @classmethod
    def resolvePath(cls, path, folders=[], suffix=None):
        expand_path = os.path.expandvars(path)
        if folders:
            expand_path = os.path.join(expand_path, *folders)
        if suffix:
            expand_path = os.path.join(expand_path, suffix)
        if not os.path.isabs(expand_path):
            return path
        resolved_path = os.path.abspath(expand_path).replace("\\", "/")
        return resolved_path


        
        
        
