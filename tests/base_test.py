import inspect
import logging

import pytest

from utils.config import TestData


@pytest.mark.usefixtures("setup")
class BaseTest:

    @staticmethod
    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler = logging.FileHandler(TestData.ROOT_PATH + "/logs/" + 'logfile.log')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)  # filehandler object
        logger.setLevel(logging.DEBUG)
        return logger
