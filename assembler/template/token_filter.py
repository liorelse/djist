#!/usr/bin/python3
"""Djist: Built-in string filters
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import html
import logging
from ..generics import (core, date, msg)


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


def dictsort_filter(value: list, argument: str) -> list:
    try:
        return sorted(value, key=lambda arg: arg[argument])
    except KeyError as err:
        logging.warning(msg.FILTER_DICTSORT_WARNING, err)
        return []


def dictsortreversed_filter(value: list, argument: str) -> list:
    try:
        return sorted(value, key=lambda arg: arg[argument], reverse=True)
    except KeyError as err:
        logging.warning(msg.FILTER_DICTSORTREVERSED_WARNING, err)
        return []


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


def filesizeformat_filter(value: int or str, argument: str) -> str:
    """filesizeformat - Formats the value to a ‘human-readable’ file size
    """
    # Solution by nneonneo on stackoverflow.com
    try:
        value = int(value)
        suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB',
                    'PiB', 'EiB', 'ZiB', 'YiB']
        count = 0
        while value >= 1024 and count < len(suffixes)-1:
            value /= 1024.
            count += 1
        number = f'{value:.2f}'.rstrip('0').rstrip('.')
        filtered_value = f'{number} {suffixes[count]}'
    except (ValueError, TypeError):
        filtered_value = value
    return filtered_value


def first_filter(value: list, argument: str):
    """first - Returns the first item in a list
    """
    try:
        filtered_value = value[0]
    except TypeError as err:
        logging.error(msg.FILTER_FIRST_ERROR, err)
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
    # Return to this filter with autoescape tag
    filtered_value = value
    return filtered_value


def get_digit_filter(value: int or str, argument: int or str) -> int or str:
    """get_digit - Given a whole number, returns the requested digit

    Digits are counted from right to left, starting with 1. Returns the
    original value for invalid input (if input or argument is not an integer,
    or if argument is less than 1). Otherwise, output is always an integer.
    """
    try:
        number = str(value)
        digit = int(argument)
        number_len = len(number)
        if number_len >= digit > 0:
            return int(number[-digit])
        else:
            logging.error(msg.FILTER_GET_FILTER_ERROR, number_len, digit)
    except ValueError as err:
        logging.error(msg.FILTER_GET_FILTER_VALUE_ERROR, err)
    filtered_value = value
    return filtered_value


def iriencode_filter(value: str, argument: str) -> str:
    # Low priority
    """iriencode - 
    """
    filtered_value = value
    return filtered_value


def join_filter(value: list or str, argument: str) -> str:
    """join - Joins a list with a string

    If the value is a string, a split character must be specific, for example:
    {{ listof|join:"**;#" }}
    """
    filtered_value = value
    splitter = argument.split(';', 1)
    joiner = splitter.pop(0)
    try:
        if isinstance(value, str) and core.not_empty(splitter):
            filtered_value = filtered_value.replace(splitter[0], joiner)
        elif isinstance(value, list):
            filtered_value = joiner.join(value)
    except TypeError as err:
        logging.error(msg.FILTER_JOIN_ERROR, err)
    return filtered_value


def json_script_filter(value: str, argument: str) -> str:
    filtered_value = value
    return filtered_value


def last_filter(value: list, argument: str) -> str:
    """last - Returns the last item in a list
    """
    try:
        filtered_value = value[-1]
    except TypeError as err:
        logging.error(msg.FILTER_LAST_ERROR, err)
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


def linenumbers_filter(value: str or list, argument: list) -> str:
    """linenumbers - Displays text with line numbers

    Args (Defaults):
        [1] ("1") - starting number for list
        [2] ("1") - minimum spaces between symbol and text
        [3] (".") - symbol to display after number, "" for no symbol

    Example:
        {{ text_list|linenumbers:"200":"4":"" }}
        {{ text_list|linenumbers:"1":dataset_spaces:symbol }}
    """
    filtered_value = ''
    arg_defaults = '11.'
    args = []
    for num in range(3):
        if core.index_in_list(num, argument) \
                and isinstance(argument[num], (str, int)):
            current_arg = str(argument[num]).strip()
            if core.is_empty(current_arg) and num != 2:
                logging.info(msg.FILTER_LINENUMBERS_DEFAULT, (num + 1))
                args.append(arg_defaults[num])
            else:
                args.append(current_arg)
        else:
            logging.info(msg.FILTER_LINENUMBERS_DEFAULT, (num + 1))
            args.append(arg_defaults[num])
    lines = value
    if isinstance(value, str):
        value = value.replace('\\n\\n', '\n\n')
        lines = value.split('\n\n')
    number_length = len(str(int(args[0]) + (len(lines) - 1)))
    tab_size = number_length + len(args[2]) + int(args[1])
    number = int(args[0])
    for line in lines:
        prefix = str(number) + str(args[2])
        spaces = ' '*(tab_size - len(prefix))
        filtered_value += prefix + spaces + line + '\n'
        number += 1
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
