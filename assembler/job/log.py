#!/usr/bin/python3
"""Djist: Logging
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import logging
from . import config


def get_level(log_level: str = 'notset'):
    levels = {
        'notset': logging.NOTSET,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    try:
        return levels[log_level.lower()]
    except KeyError:
        return logging.WARNING


def start_logging():
    """Set up logging"""
    logger = logging.getLogger('root')
    logger.setLevel(logging.NOTSET)
    # Console
    if config.LOG_CONSOLE:
        cons_handler = logging.StreamHandler()
        cons_handler.setLevel(get_level(config.LOG_CONSOLE_LEVEL))
        c_fmt = '%(levelname)s: [%(module)s] %(message)s'
        cons_format = logging.Formatter(c_fmt)
        cons_handler.setFormatter(cons_format)
        logger.addHandler(cons_handler)
    if config.LOG_FILE:
        # Log File
        file_handler = logging.FileHandler(config.LOG_FILE_LOCATION)
        file_handler.setLevel(get_level(config.LOG_FILE_LEVEL))
        f_fmt = '%(asctime)s %(levelname)s: [%(module)s] %(message)s'
        file_format = logging.Formatter(f_fmt)
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)


def stop_logging():
    """Shut down logging"""
    logging.info('Djist assemble finished')
    logging.shutdown()
