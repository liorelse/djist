#!/usr/bin/python3
"""Djist: Built-in string filters
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import html
import logging
from ..generics import core
from ..generics import date
import html


def add_filter(value: str, argument: str) -> str:
    """add - Adds the argument to the value

    This filter will first try to coerce both values to integers. If this
    fails, it’ll concatenate the strings together.
    """
    try:
        filtered_value = str(int(value) + int(argument))
    except (ValueError, TypeError):
        filtered_value = value + argument
    return filtered_value


def addslashes_filter(value: str, argument: str) -> str:
    """addslashes - Adds slashes before quotes

    Useful for escaping strings in CSV, for example.
    """
    filtered_value = value.replace("'", "\\'").replace('"', '\\"')
    return filtered_value


def capfirst_filter(value: str, argument: str) -> str:
    """capfirst - Capitalizes the first character of the value

    First character is capitalized, while the remaining characters are left
    as-is. If the first character is not a letter, this filter has no effect.
    """
    filtered_value = value[0].capitalize() + value[1:]
    return filtered_value


def capitalize_filter(value: str, argument: str) -> str:
    """capitalize - Capitalizes the value

    First character is capitalized, and remaining characters are changed to
    lowercase.
    """
    filtered_value = value.capitalize()
    return filtered_value


def center_filter(value: str, argument: str) -> str:
    """center - Centers the value in a field of a given width
    """
    argument_list = argument.split(';', 1)
    try:
        argument_width = int(argument_list.pop(0))
    except ValueError:
        argument_width = 0
    if core.not_empty(argument_list):
        argument_fillchar = argument_list.pop(0)[0]
    else:
        argument_fillchar = ' '
    filtered_value = value.center(argument_width, argument_fillchar)
    return filtered_value


def cut_filter(value: str, argument: str) -> str:
    """cut - Removes all instances of the argument from the given string
    """
    filtered_value = value.replace(argument, '')
    return filtered_value


def date_filter(value: str, argument: str) -> str:
    """date - Formats a date according to the given format

    Default format is Django/PHP style directives. Standard Python (strftime)
    directives are used by adding ';python' to the date format.

    Example: {{ value|date:"D d M Y" }} {{ value|date:"%a, %d %b %Y;python" }}
    """
    argument_list = argument.split(';', 1)
    dt_format = argument_list.pop(0)
    format_type = 'django'
    if core.not_empty(argument_list):
        format_type = argument_list.pop(0)
    filtered_value = date.format_datetime(value, dt_format, format_type)
    return filtered_value


def default_filter(value: str, argument: str) -> str:
    """default - If value evaluates to False, uses the given default
    """
    if value:
        return value
    return argument


def default_if_none_filter(value: str, argument: str) -> str:
    """default - If (and only if) value is None, uses the given default
    """
    if value is None:
        return argument
    return value


def dictsort_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def dictsortreversed_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def divisibleby_filter(value: str, argument: str) -> bool:
    """divisibleby - Returns True if the value is divisible by the argument
    """
    try:
        filtered_value = int(value) % int(argument) == 0
    except (ValueError, TypeError):
        filtered_value = False
    return filtered_value


def escape_filter(value: str, argument: str) -> str:
    """escape - Escapes a string’s HTML
    """
    filtered_value = core.substitute(core.esc_html(), value, True)
    filtered_value = html.escape(filtered_value)
    return filtered_value


def escapejs_filter(value: str, argument: str) -> str:
    """escapejs - Escapes characters for use in JavaScript strings

    This does not make the string safe for use in HTML or JavaScript template
    literals, but does protect you from syntax errors when using templates to
    generate JavaScript/JSON.
    """
    filtered_value = core.substitute(core.esc_js(), value, True)
    filtered_value = core.substitute(core.esc_js(), value)
    return filtered_value


def filesizeformat_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def first_filter(value: list, argument: str):
    """first - Returns the first item in a list
    """
    if isinstance(value, (list, dict)):
        filtered_value = value[0]
    else:
        filtered_value = value
    return filtered_value


def floatformat_filter(value: float or str, argument: int or str = -1) -> str:
    """floatformat -  rounds a floating-point number to the given decimal place

    When used without an argument, rounds a floating-point number to one
    decimal place – but only if there’s a decimal part to be displayed.
    If used with a numeric integer argument, floatformat rounds a number to
    that many decimal places.
    Particularly useful is passing 0 (zero) as the argument which will round
    the float to the nearest integer.
    If the argument passed to floatformat is negative, it will round a number
    to that many decimal places – but will not pad the return with zeros.
    Using floatformat with no argument is equivalent to using floatformat with
    an argument of -1.
    """
    if value is None or value == '':
        value = 0.0
    if argument is None or argument == '':
        argument = -1
    try:
        value = float(value)
        decimals = int(argument)
        if decimals == 0 or core.sign(decimals) == 1:
            filtered_value = f'{value:.{decimals}f}'
        else:
            filtered_value = round(value, abs(decimals))
            if filtered_value == int(filtered_value):
                filtered_value = int(filtered_value)
    except (ValueError, TypeError):
        filtered_value = value
    return filtered_value


def force_escape_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def get_digit_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def iriencode_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def join_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def json_script_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def last_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def length_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def length_is_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def linebreaks_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def linebreaksbr_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def linenumbers_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def ljust_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def lower_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value.lower()


def make_list_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def phone2numeric_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def pluralize_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def post_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value + argument


def pprint_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def pre_filter(value: str, argument: str) -> str:
    return argument + value


def random_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def rjust_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def safe_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def safeseq_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def slice_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def slugify_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def stringformat_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def striptags_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def time_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def timesince_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def timeuntil_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def title_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def truncatechars_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def truncatechars_html_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def truncatewords_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def truncatewords_html_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def unescape_filter(value: str, argument: str) -> str:
    """unescape - Unescapes an escaped HTML string
    """
    filtered_value = html.unescape(value)
    return filtered_value


def unordered_list_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def upper_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def urlencode_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def urlize_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def urlizetrunc_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def wordcount_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def wordwrap_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def yesno_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


boolean_filters = [
    'divisibleby',
]


filterselect = {
    'add': add_filter,
    'addslashes': addslashes_filter,
    'capfirst': capfirst_filter,
    'capitalize': capitalize_filter,
    'center': center_filter,
    'cut': cut_filter,
    'date': date_filter,
    'default': default_filter,
    'default_if_none': default_if_none_filter,
    'dictsort': dictsort_filter,
    'dictsortreversed': dictsortreversed_filter,
    'divisibleby': divisibleby_filter,
    'escape': escape_filter,
    'escapejs': escapejs_filter,
    'filesizeformat': filesizeformat_filter,
    'first': first_filter,
    'floatformat': floatformat_filter,
    'force_escape': force_escape_filter,
    'get_digit': get_digit_filter,
    'iriencode': iriencode_filter,
    'join': join_filter,
    'json_script': json_script_filter,
    'last': last_filter,
    'length': length_filter,
    'length_is': length_is_filter,
    'linebreaks': linebreaks_filter,
    'linebreaksbr': linebreaksbr_filter,
    'linenumbers': linenumbers_filter,
    'ljust': ljust_filter,
    'lower': lower_filter,
    'make_list': make_list_filter,
    'phone2numeric': phone2numeric_filter,
    'pluralize': pluralize_filter,
    'post': post_filter,
    'pprint': pprint_filter,
    'pre': pre_filter,
    'random': random_filter,
    'rjust': rjust_filter,
    'safe': safe_filter,
    'safeseq': safeseq_filter,
    'slice': slice_filter,
    'slugify': slugify_filter,
    'stringformat': stringformat_filter,
    'striptags': striptags_filter,
    'time': time_filter,
    'timesince': timesince_filter,
    'timeuntil': timeuntil_filter,
    'title': title_filter,
    'truncatechars': truncatechars_filter,
    'truncatechars_html': truncatechars_html_filter,
    'truncatewords': truncatewords_filter,
    'truncatewords_html': truncatewords_html_filter,
    'unescape': unescape_filter,
    'unordered_list': unordered_list_filter,
    'upper': upper_filter,
    'urlencode': urlencode_filter,
    'urlize': urlize_filter,
    'urlizetrunc': urlizetrunc_filter,
    'wordcount': wordcount_filter,
    'wordwrap': wordwrap_filter,
    'yesno': yesno_filter,
}
