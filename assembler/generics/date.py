#!/usr/bin/python3
"""Djist: Generic date/time operations
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import logging
from platform import system
from dateutil.parser import parse
from pyparsing import printables, Combine, Char, Literal, White, Word, ZeroOrMore
from . import msg


def platform_check(directive: str) -> str:
    """Change directive to correct style if Windows platform detected"""
    if system() == "Windows":
        return directive.replace("%-", "%#")
    return directive


def default_format() -> dict:
    """Named formatters"""
    return {
        "DATE_FORMAT": "",
        "DATETIME_FORMAT": "",
        "SHORT_DATE_FORMAT": "",
        "SHORT_DATETIME_FORMAT": "",
    }


def directives_dj_py() -> dict:
    """Django to Python directives"""
    return {
        # Day
        "d": "%d",  # Day of the month, 2 digits with leading zeros
        "j": "%-d",  # Day of the month without leading zeros
        "D": "%a",  # Day of the week, textual, 3 letters
        "l": "%A",  # Day of the week, textual, long
        #'S': '[ord]', # English ordinal suffix for day of the month, 2 chars
        "w": "%w",  # Day of the week, digits without leading zeros
        "z": "%-j",  # Day of the year
        # Week
        "W": "%V",  # ISO-8601 week number of year, with weeks starting on Mon
        # Month
        "m": "%m",  # Month, 2 digits with leading zeros
        "n": "%-m",  # Month without leading zeros
        "M": "%b",  # Month, textual, 3 letters (or abbreviated)
        #'b': '[low%b]', # Month, textual, 3 letters, lowercase
        "E": "%B",
        "F": "%B",  # Month, textual, long
        #'N': '[abr]',
        #'t': '[dim]',
        # Year
        "y": "%y",  # Year, 2 digits
        "Y": "%Y",  # Year, 4 digits
        #'L': '[lep]', # Boolean for whether it’s a leap year
        "o": "%G",  # ISO-8601 week-numbering year
        # Time
        "g": "%-I",  # Hour, 12-hour format without leading zeros
        "G": "%-H",  # Hour, 24-hour format without leading zeros
        "h": "%I",  # Hour, 12-hour format
        "H": "%H",  # Hour, 24-hour format
        "i": "%M",  # Minutes, 2 digits with leading zeros
        "s": "%S",  # Seconds, 2 digits with leading zeros
        "u": "%f",  # Microseconds
        #'a': '[apm%p]', # 'a.m.' or 'p.m.'
        "A": "%p",  # 'AM' or 'PM'.
        #'f': '[]', # 12-hour hours and minutes, minutes left off if zero
        #'P': '[]',
        # Timezone
        "e": "%Z",  # Timezone name. Could be in any format
        "I": "",  # Daylight Savings Time, whether it’s in effect or not
        "O": "%z",  # Difference to Greenwich time in hours
        "T": "",  # Time zone of this machine
        "Z": "",  # Time zone offset in seconds
        # Date/Time
        "c": "",  # ISO 8601 format.
        "r": "",  # RFC 5322 formatted date
        #'U': '%s', # Seconds since the Unix Epoch
    }


def translate_dj_py(dj_directive: str) -> str:
    """Translate a Django format directive into a Python directive"""
    py_directive = dj_directive
    if dj_directive in directives_dj_py().keys():
        py_directive = directives_dj_py()[dj_directive]
    return py_directive


def tokenize_format(format_string: str, format_type: str) -> list:
    """Tokenize a datetime format string"""
    tokens = []
    if format_type.lower() == "python":
        directives = "aAwdbBmyYHIpMSfzZjUWcxX%"
        match = ZeroOrMore(
            White()
            | Combine((Literal("%-") ^ Literal("%")) + Char(directives))
            | Word(printables)
        )
        tokens = match.parseString(format_string).asList()
    else:
        tokens = list(format_string)
    return tokens


def format_datetime(dt_value: str, dt_format: str, format_type: str) -> str:
    """Date/time string formatter

    Args:
        dt_value (str): Date/time string to be formatted, e.g. '21 March, 2015'
        dt_format (str): Formatting directives, e.g. 'j-M-Y H:i:s'
        format_type (str): Type of directives, 'django' or 'python' expected
            Unexpected format_type will be treated as 'django' format

    Returns:
        str: Formatted date/time string
    """
    datetime_value = parse(dt_value)
    tokens = tokenize_format(dt_format, format_type)
    strftime_format = ""
    if format_type.lower() == "python":
        for token in tokens:
            strftime_format += platform_check(token)
    else:
        for token in tokens:
            strftime_format += platform_check(translate_dj_py(token))
    try:
        return datetime_value.strftime(strftime_format)
    except ValueError:
        logging.error(msg.DATE_FORMAT_ERROR, format_type.lower(), strftime_format)
        return None
