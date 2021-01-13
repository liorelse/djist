#!/usr/bin/python3
"""Djist: Logging
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import logging


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


def start_logging(log_file: str = 'djist.log', log_level: str = 'warning',
                  console_level: str = 'info'):
    """Set up logging"""
    logger = logging.getLogger('root')
    logger.setLevel(logging.NOTSET)
    # Console
    cons_handler = logging.StreamHandler()
    cons_handler.setLevel(get_level(console_level))
    c_fmt = '%(levelname)s: [%(module)s] %(message)s'
    cons_format = logging.Formatter(c_fmt)
    cons_handler.setFormatter(cons_format)
    logger.addHandler(cons_handler)
    # Log File
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(get_level(log_level))
    f_fmt = '%(asctime)s %(levelname)s: [%(module)s] %(message)s'
    file_format = logging.Formatter(f_fmt)
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
