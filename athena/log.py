"""
Basic athena logging tools
"""
import logging

from athena import settings


logger = logging.getLogger(settings.LOG_NAME)
logger.setLevel(settings.LOG_LEVEL)
fh = logging.FileHandler(settings.LOG_FILE)
fh.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s"))
fh.setLevel(settings.LOG_LEVEL)
logger.addHandler(fh)


def debug(msg):
    """ Logs a debug message to the logger """
    if logger.level <= logging.DEBUG:
        print('\n~ ' + msg)
    logger.debug(msg)


def info(msg):
    """ Logs an info message to the logger """
    if logger.level <= logging.INFO:
        print('\n~ ' + msg)
    logger.info(msg)


def error(msg):
    """ Logs an error message to the logger """
    if logger.level <= logging.ERROR:
        print('\n~ ' + msg)
    logger.info(msg)