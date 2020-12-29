#!/usr/bin/python3


"""
Site Assembler: Generic functions
"""

__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


def evaluate(exp, vars):
    pass
    # parser = expression.Expression_Parser(variables=vars)
    # return parser.parse(exp)


def is_empty(obj):
    return len(obj) == 0


def not_empty(obj):
    return not is_empty(obj)


def is_none_or_empty(obj):
    return is_empty(obj) and obj is not None


def not_none_or_empty(obj):
    return not is_none_or_empty(obj)


def web_safe_subs():
    return {
        '"': '&#34;',
        "'": '&#39;',
        # '--': '<br />'
    }


def substitute(subs: dict, text: str):
    for k, v in subs.items():
        text = text.replace(k, v)
    return text


def web_safe_string(dirty_string: str):
    safe_string = substitute(web_safe_subs(), dirty_string)
    return safe_string


def web_safe_list(dirty_list: list):
    safe_list = []
    for x in dirty_list:
        safe_list.append(web_safe_string(x))
    return safe_list
