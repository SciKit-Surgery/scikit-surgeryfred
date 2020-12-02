# coding=utf-8

"""scikit-surgeryfed tests"""

from os import path
from sksurgeryfredbe.logging.fred_logger import Logger

def test_empty_config():
    """
    Test that the app runs
    """

    config = {
        "tracker type" : "aruco",
        "video source" : "data/aruco_tag.avi"
        }

    logger = Logger(config)

    logger.log(message="testing")
    del logger


def test_non_empty_config():
    """
    Test that the app runs
    """

    config = {
        "logger" : {}
        }

    logger = Logger(config)

    logger.log(message="testing")
    assert path.exists("sksurgeryfred.log")

    del logger


def test_overwrite():
    """
    Test that overwrite works
    """

    config = {
        "logger" : {
            "log file name" : "testing_log_file.log",
            "overwrite existing" : True
            }
        }

    logger = Logger(config)
    logger.log(message="testing")
    assert path.exists("testing_log_file.log")

    del logger
