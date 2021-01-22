#!/usr/bin/python3
"""Djist: Built-in string filters
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import html
import logging
from ..generics import (core, date, msg)
from . import processor


def arg_default_types(filter_name: str) -> list:
    """Get default types for specific filter"""
    return filter_defaults[filter_name][0]


def arg_default_values(filter_name: str) -> list:
    """Get default values for specific filter"""
    return filter_defaults[filter_name][1]


def arg_default_disallowed(filter_name: str) -> list:
    """Get default values for specific filter"""
    return filter_defaults[filter_name][2]


def resolve_arguments(filter_name: str, argument: list) -> list:
    """Check arguments and replace with defaults where required"""
    types = arg_default_types(filter_name)
    default_values = arg_default_values(filter_name)
    disallowed_values = arg_default_disallowed(filter_name)
    return_arguments = []
    for index, expected_type in enumerate(types):
        if core.index_in_list(index, argument):
            template_value = argument[index]
            if isinstance(template_value, expected_type):
                if not template_value in disallowed_values[index]:
                    return_arguments.append(template_value)
                else:
                    return_arguments.append(default_values[index])
                    logging.info(msg.FILTER_DEFAULT_VALUE_INFO, filter_name,
                                 default_values[index], (index + 1))
            else:
                return_arguments.append(default_values[index])
                logging.warning(msg.FILTER_DEFAULT_TYPE_WARNING, filter_name,
                                core.types(expected_type),
                                core.types(template_value))
                logging.info(msg.FILTER_DEFAULT_VALUE_INFO, filter_name,
                             default_values[index], (index + 1))
        else:
            return_arguments.append(default_values[index])
            logging.info(msg.FILTER_DEFAULT_VALUE_INFO, filter_name,
                         default_values[index], (index + 1))
    return return_arguments


def add_filter(value: str or int or float,
               argument: list) -> str or int or float:
    """add - Adds the argument to the value

    This filter will first try to coerce both values to integers or floats. If
    this fails, it’ll concatenate the strings together.

    Arguments:
        value (str, int, float) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int, float) - number to add <'0'>

    Example:
        {{ "8"|add:"2" }}
        {{ price|add:tax }}
    """
    args = resolve_arguments('add', argument)
    def fix(value):
        fixed = value
        if isinstance(value, str):
            if value.isnumeric():
                fixed = int(value)
            elif '.' in value:
                try:
                    fixed = float(value)
                except ValueError:
                    fixed = str(value)
            else:
                try:
                    fixed = str(value)
                except ValueError:
                    logging.error(msg.FILTER_VALUE_TYPE_WARNING, 'add',
                                  core.types(value))
                    return None
        return fixed
    fixed_value = fix(value)
    fixed_arg = fix(args[0])
    if isinstance(fixed_value, str) or isinstance(fixed_arg, str):
        return str(fixed_value) + str(fixed_arg)
    return fixed_value + fixed_arg


def addslashes_filter(value: str, argument: list) -> str:
    """addslashes - Adds slashes before quotes

    Useful for escaping strings in CSV, for example.

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "I'm testing the 'addslashes' filter"|addslashes }}
    """
    del argument
    if isinstance(value, str) and len(value) > 0:
        return value.replace("'", "\\'").replace('"', '\\"')
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'addslashes',
                    core.types(value))
    return None


def capfirst_filter(value: str, argument: list) -> str:
    """capfirst - Capitalizes the first character of the value

    First character is capitalized, while the remaining characters are left
    as-is. If the first character is not a letter, this filter has no effect.

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "capFirst"|capfirst }}
    """
    del argument
    if isinstance(value, str) and len(value) > 0:
        return value[0].capitalize() + value[1:]
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'capfirst',
                    core.types(value))
    return None


def capitalize_filter(value: str, argument: list) -> str:
    """capitalize - Capitalizes the value

    First character is capitalized, and remaining characters are changed to
    lowercase

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "capFirst"|capitalize }}
    """
    del argument
    if isinstance(value, str):
        return value.capitalize()
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'capitalize',
                    core.types(value))
    return None


def center_filter(value: str, argument: list) -> str:
    """center - Centers the value in a field of a given width

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int) - width of the field <'0'>
            2 (str) - fill character <' '>

    Example:
        {{ "This Sentence  Has No   Spaces "|cut:" " }}
    """
    args = resolve_arguments('center', argument)
    argument_width = core.convert_to_int(args[0])
    argument_fillchar = args[1][0]
    return value.center(argument_width, argument_fillchar)


def cut_filter(value: str, argument: list) -> str:
    """cut - Removes all instances of the argument from the given string

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - sub-string to cut from value <''>

    Example:
        {{ "This Sentence  Has No   Spaces "|cut:" " }}
    """
    args = resolve_arguments('cut', argument)
    return value.replace(args[0], '')


def date_filter(value: str, argument: list) -> str:
    """date - Formats a date according to the given format

    Default format is Django/PHP style directives. Standard Python (strftime)
    directives are used by adding 'python' as argument 2.

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - Date format <'D, m M Y H:i:s O'>
            2 (str) - Style of date directives <'django'>

    Example:
        {{ value|date:"D d M Y" }}
        {{ value|date:"%a, %d %b %Y":"python" }}
    """
    args = resolve_arguments('date', argument)
    dt_format = args[0]
    format_type = args[1]
    return date.format_datetime(value, dt_format, format_type)


def default_filter(value, argument: list):
    """default - If value evaluates to False, uses the given default

    Arguments:
        value (str, int, float, dict, list, bool, None)
                - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int, float, dict, list, bool, None)
                - Returned if the value evaluates to False <''>

    Example:
        {{ colours.name|default_if_none:"Colour has no name" }}
        {{ colours|dictsort:"mix.price"|default_if_none:colours }}
    """
    args = resolve_arguments('default', argument)
    if value:
        return value
    return args[0]


def default_if_none_filter(value, argument: list):
    """default_if_none - If (and only if) value is None, uses the given default

    Arguments:
        value (str, int, float, dict, list, bool, None) 
                - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int, float, dict, list, bool, None)
                - Returned if the value is None <''>

    Example:
        {{ colours.name|default_if_none:"Colour has no name" }}
        {{ colours|dictsort:"mix.price"|default_if_none:colours }}
    """
    args = resolve_arguments('default_if_none', argument)
    if value is None:
        return args[0]
    return value


def dictsort_filter(value: list, argument: list) -> list:
    """dictsort - Takes a list of dictionaries and returns that list sorted by
    the key given in the argument

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - Dictionary/Object key to sort by <''>
                The key must be passed as a quoted literal, e.g. "example.key"
            2 (str) - Reverse the sort order <'reverse'>

    Example:
        {{ colours|dictsort:"colour-name" }}
        {{ websites|dictsort:"url.short":"reverse" }}
    """
    args = resolve_arguments('dictsort', argument)
    if isinstance(value, list) and core.index_in_list(0, value):
        key_ = []
        reverse_sort = args[1].lower().startswith('r')
        proc = processor.Processor(-1)
        if isinstance(value[0], dict):
            key_ = args[0]
            for val in value:
                proc.update_dataset(val)
            try:
                return sorted(value, key=lambda arg: proc.get_data(
                              return_type='any', key=key_, dataset=arg),
                              reverse=reverse_sort)
            except (KeyError, IndexError, TypeError):
                logging.error(msg.FILTER_DICTSORT_ERROR, key_)
                return None
        elif isinstance(value[0], list):
            key_ = core.convert_to_int(args[0])
            try:
                return sorted(value, key=lambda arg: arg[key_],
                              reverse=reverse_sort)
            except (KeyError, IndexError, TypeError):
                logging.error(msg.FILTER_DICTSORT_ERROR, key_)
                return None
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'dictsort',
                    core.types(value))
    return None


def dictsortreversed_filter(value: list, argument: list) -> list:
    """dictsortreversed - Takes a list of dictionaries and returns that list
    sorted in reverse order by the key given in the argument

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - Dictionary/Object key to reverse sort by <''>

    Example:
        {{ colours|dictsortreversed:"colour-name" }}
    """
    key = ''
    if core.index_in_list(0, argument):
        key = argument[0]
    argument = [key, 'reverse']
    return dictsort_filter(value, argument)


def divisibleby_filter(value: str or int or float, argument: list) -> bool:
    """divisibleby - Returns True if the value is divisible by the argument

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int, float) - divide by value <'1'>

    Example:
        {% if "3.5"|divisibleby:"0.5" %} Pass {% else %} Fail {% endif %}
    """
    args = resolve_arguments('divisibleby', argument)
    if isinstance(value, (str, int, float)):
        left = core.convert_to_float(value)
        right = core.convert_to_float(args[0])
        if left > 0 and right > 0:
            return left % right == 0.0
        logging.error(msg.FILTER_DIVISIBLEBY_ERROR, left, right)
        return None
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'divisibleby',
                    core.types(value))
    return None


def escape_filter(value: str, argument: list) -> str:
    """escape - Escapes a string’s HTML

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "testing\\r\\njavascript 'string\\" <b>escaping</b>"|escapejs }}
    """
    del argument
    if isinstance(value, str):
        remove_escapes = core.substitute(core.esc_html(), value, True)
        apply_escapes = html.escape(remove_escapes)
        return apply_escapes
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'escape',
                    core.types(value))
    return None


def escapejs_filter(value: str, argument: list) -> str:
    """escapejs - Escapes characters for use in JavaScript strings

    This does not make the string safe for use in HTML or JavaScript template
    literals, but does protect you from syntax errors when using templates to
    generate JavaScript/JSON.

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "testing\\r\\njavascript 'string\\" <b>escaping</b>"|escapejs }}
    """
    del argument
    if isinstance(value, str):
        remove_escapes = core.substitute(core.esc_js(), value, True)
        apply_escapes = core.substitute(core.esc_js(), remove_escapes)
        return apply_escapes
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'escapejs',
                    core.types(value))
    return None


def filesizeformat_filter(value: str or int or float, argument: list) -> str:
    """filesizeformat - Formats the value to a ‘human-readable’ file size

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "1234567"|filesizeformat }}
    """
    # Solution by nneonneo on stackoverflow.com
    del argument
    if isinstance(value, (str, int, float)):
        value = core.convert_to_float(value)
        suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB',
                    'PiB', 'EiB', 'ZiB', 'YiB']
        count = 0
        while value >= 1024 and count < len(suffixes)-1:
            value /= 1024.
            count += 1
        number = f'{value:.2f}'.rstrip('0').rstrip('.')
        return f'{number} {suffixes[count]}'
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'filesizeformat',
                    core.types(value))
    return None


def first_filter(value: list or str, argument: list):
    """first - Returns the first item in a list

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ listdata|first }}
    """
    del argument
    if isinstance(value, (list, str)) and len(value) > 0:
        return value[0]
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'first',
                    core.types(value))
    return None


def floatformat_filter(value: float or str, argument: list) -> str:
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

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int) - decimal places to round to <'-1'>

    Example:
        {{ longint|get_digit:"8" }}
        {{ 456723|get_digit:position }}
    """
    args = resolve_arguments('floatformat', argument)
    decimals = core.convert_to_int(args[0])
    if value in (None, ''):
        value = 0.0
    value = core.convert_to_float(value)
    if decimals == 0 or core.sign(decimals) == 1:
        filtered_value = f'{value:.{decimals}f}'
    else:
        filtered_value = round(value, abs(decimals))
        if filtered_value == int(filtered_value):
            filtered_value = int(filtered_value)
    return str(filtered_value)


def force_escape_filter(value: str, argument: str) -> str:
    # Return to this filter with autoescape tag
    # Low priority
    filtered_value = value
    return filtered_value


def get_digit_filter(value: int or str, argument: list) -> int:
    """get_digit - Given a whole number, returns the requested digit

    Digits are counted from right to left, starting with 1. Returns an integer.

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int) - position digit for value <'1'>

    Example:
        {{ longint|get_digit:"8" }}
        {{ 456723|get_digit:position }}
    """
    args = resolve_arguments('get_digit', argument)
    if isinstance(value, (str, int)):
        number = str(value)
        number_len = len(number)
        digit = core.convert_to_int(args[0])
        if number_len >= digit > 0:
            return int(number[core.int_negate(digit)])
        logging.error(msg.FILTER_GET_DIGIT_ARG_ERROR, number_len, digit)
        return None
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'get_digit',
                    core.types(value))
    return None


def iriencode_filter(value: str, argument: str) -> str:
    # Low priority
    """iriencode - 
    """
    filtered_value = value
    return filtered_value


def join_filter(value: list or str, argument: list) -> str:
    """join - Joins a list (or split string) with a specified string

    If the value is a string, a split character must be specified

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - joining character/string <''>
            2 (str) - split character/string <' '>

    Example:
        {{ list|join }}
        {{ "item1;item2"|join:", ":";" }}
    """
    args = resolve_arguments('join', argument)
    joiner = args[0]
    splitter = args[1]
    if isinstance(value, str):
        value = value.split(splitter)
    if isinstance(value, list):
        return joiner.join(string for string in value
                           if isinstance(string, str))
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'join', core.types(value))
    return None


def json_script_filter(value: str, argument: str) -> str:
    # Low priority
    filtered_value = value
    return filtered_value


def last_filter(value: list, argument: list):
    """last - Returns the last item in a list

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ datasetlist|last }}
    """
    del argument
    if isinstance(value, (str, list)):
        return value[-1]
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'last',
                    core.types(value))
    return None


def length_filter(value: str or list or dict, argument: list) -> int:
    """length - Returns the length of the value

    This works for both strings and lists

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (int) - amount to add after determining length of value <0>

    Example:
        {{ "name"|length }}
        {{ datastring|length:padding }}
    """
    args = resolve_arguments('length', argument)
    add_number = core.convert_to_int(args[0])
    if isinstance(value, (str, list, dict)):
        return len(value) + add_number
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'length',
                    core.types(value))
    return None


def length_is_filter(value: str or list or dict, argument: list) -> bool:
    """length_is - Checks if the length of an object matches a supplied number

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (int) - length to compare to <0>

    Returns:
        (bool) - True if the value’s length is the argument, or False otherwise

    Example:
        {% if "name"|length_is:"4" %} Length is 4 {% endif %}
    """
    args = resolve_arguments('length_is', argument)
    comp = core.convert_to_int(args[0])
    if isinstance(value, (str, list, dict)):
        return len(value) == comp
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'length_is',
                    core.types(value))
    return False


def linebreaks_filter(value: str, argument: list) -> str:
    """linebreaks - Replaces line breaks in plain text with appropriate HTML

    A single newline becomes an HTML line break (<br>) and a double new line
    followed becomes a paragraph break (</p>)

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - delimiter for paragraph break <double *newline*>
            2 (str) - delimiter for line break <*newline*>

    Example:
        {{ textstring|linebreaks }}
        {{ "Address: Street, Town, State"|linebreaks:": ":", " }}
    """
    args = resolve_arguments('linebreaks', argument)
    filtered_value = ''
    para_break = args[0]
    line_break = args[1]
    if para_break == '\n\n':
        value = value.replace('\\n\\n', '\n\n')
    paragraphs = value.split(para_break)
    for paragraph in paragraphs:
        filtered_value += '<p>'
        filtered_value += linebreaksbr_filter(paragraph, [line_break])
        filtered_value += '</p>'
    return filtered_value


def linebreaksbr_filter(value: str, argument: list) -> str:
    """linebreaksbr - Converts all newlines to HTML line breaks (<br>)

    Arguments:
        value (str) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str) - alternative delimiter for line break <*newline*>

    Example:
        {{ textstring|linebreaksbr }}
        {{ "Address: Street, Town, State"|linebreaksbr:", " }}
    """
    args = resolve_arguments('linebreaksbr', argument)
    filtered_value = ''
    line_break = args[0]
    if line_break == '\n':
        value = value.replace('\\n', '\n')
    filtered_value = value.replace(line_break, '<br>')
    return filtered_value


def linenumbers_filter(value: str or list, argument: list) -> str:
    """linenumbers - Displays text with line numbers

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            1 (str, int) - starting number for list <"1">
            2 (str, int) - minimum spaces between symbol and text <"1">
            3 (str) - symbol to display after number, "" for no symbol <".">

    Example:
        {{ textlist|linenumbers:"200":"4":"" }}
        {{ textlist|linenumbers:"1":dataset_spaces:symbol }}
    """
    args = resolve_arguments('linenumbers', argument)
    filtered_value = ''
    lines = value
    if isinstance(value, str):
        value = value.replace('\\n', '\n')
        lines = value.split('\n')
    number = core.convert_to_int(args[0])
    minimum_spaces = core.convert_to_int(args[1])
    symbol = args[2]
    number_length = len(str(number + (len(lines) - 1)))
    tab_size = number_length + len(symbol) + minimum_spaces
    for line in lines:
        prefix = str(number) + symbol
        spaces = ' '*(tab_size - len(prefix))
        filtered_value += prefix + spaces + line + '\n'
        number += 1
    return filtered_value


def ljust_filter(value: str, argument: str) -> str:
    """[summary]

    Args:
        value (str): [description]
        argument (str): [description]

    Returns:
        str: [description]
    """
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


def unescape_filter(value: str, argument: list) -> str:
    """unescape - Unescapes an escaped HTML string

    Arguments:
        value (str, list) - value(s) to be filtered
        argument (list) - filter arguments <defualt values>
            Argument ignored

    Example:
        {{ "&lt;body class=\&quot;test\&quot;&gt;"|unescape }}
    """
    del argument
    if isinstance(value, str):
        return html.unescape(value)
    logging.warning(msg.FILTER_VALUE_TYPE_WARNING, 'unescape',
                    core.types(value))
    return None


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
    'length_is'
]


filter_select = {
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


"""
Default values for filter functions

    Defaults (tuple):

        Types (list) - List of types allowed for each argument, multiple
            types can be contained in a tuple.
            Example: [str, (int, float), str]

        Values (list) - One default value for each argument
            Example: ['name', 3.4, 'red']

        Disallowed Values (list) - Disallowed values for each argument,
            values (or no values) must be contained in a tuple.
            Example: [('',), (1, 2.2, 5), ()]
"""
filter_defaults = {
    'add': (
        [(str, int, float)],
        ['0'],
        [('',)],
    ),
    'addslashes': ([], [], []),
    'capfirst': ([], [], []),
    'capitalize': ([], [], []),
    'center': (
        [(str, int), (str)],
        ['0', ' '],
        [(), ('',)],
    ),
    'cut': (
        [(str)],
        [''],
        [()],
    ),
    'date': (
        [(str), (str)],
        ['D, m M Y H:i:s O', 'django'],
        [(), ()],
    ),
    'default': (
        [(str, int, float, dict, list, bool, None)],
        [''],
        [()],
    ),
    'default_if_none': (
        [(str, int, float, dict, list, bool, None)],
        [''],
        [()],
    ),
    'dictsort':  (
        [(str, int), (str)],
        ['', ''],
        [(), ()],
    ),
    'dictsortreversed': ([], [], []),
    'divisibleby': (
        [(str, int, float)],
        ['1'],
        [('', 0, 0.0)],
    ),
    'escape': ([], [], []),
    'escapejs': ([], [], []),
    'filesizeformat': ([], [], []),
    'first': ([], [], []),
    'floatformat': (
        [(str, int)],
        ['-1'],
        [('',)],
    ),
    'force_escape': ([], [], []),
    'get_digit': (
        [(str, int)],
        ['1'],
        [('',)],
    ),
    'iriencode': ([], [], []),
    'join': (
        [(str), (str)],
        ['', ' '],
        [(), ('',)],
    ),
    'json_script': ([], [], []),
    'last': ([], [], []),
    'length': (
        [(str, int)],
        [0],
        [()],
    ),
    'length_is': (
        [(str, int)],
        [0],
        [()],
    ),
    'linebreaks': (
        [(str), (str)],
        ['\n\n', '\n'],
        [('',), ('',)],
    ),
    'linebreaksbr': (
        [(str)],
        ['\n'],
        [('',)],
    ),
    'linenumbers': (
        [(str, int), (str, int), (str)],
        ['1', '1', '.'],
        [('',), ('',), ()],
    ),
    'ljust': ([], [], []),
    'lower': ([], [], []),
    'make_list': ([], [], []),
    'phone2numeric': ([], [], []),
    'pluralize': ([], [], []),
    'post': ([], [], []),
    'pprint': ([], [], []),
    'pre': ([], [], []),
    'random': ([], [], []),
    'rjust': ([], [], []),
    'safe': ([], [], []),
    'safeseq': ([], [], []),
    'slice': ([], [], []),
    'slugify': ([], [], []),
    'stringformat': ([], [], []),
    'striptags': ([], [], []),
    'time': ([], [], []),
    'timesince': ([], [], []),
    'timeuntil': ([], [], []),
    'title': ([], [], []),
    'truncatechars': ([], [], []),
    'truncatechars_html': ([], [], []),
    'truncatewords': ([], [], []),
    'truncatewords_html': ([], [], []),
    'unescape': ([], [], []),
    'unordered_list': ([], [], []),
    'upper': ([], [], []),
    'urlencode': ([], [], []),
    'urlize': ([], [], []),
    'urlizetrunc': ([], [], []),
    'wordcount': ([], [], []),
    'wordwrap': ([], [], []),
    'yesno': ([], [], []),
}
