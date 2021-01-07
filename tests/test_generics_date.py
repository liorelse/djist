# import pytest
from .context import assembler

dt = assembler.generics.date


# tokenize_format

def test_tokenize_format_1a():
    result = dt.tokenize_format('D, d M Y', 'PHP')
    expected = []
    assert result == expected


def test_tokenize_format_2a():
    result = dt.tokenize_format('D, d M Y', 'django')
    expected = ['D', ',', ' ', 'd', ' ', 'M', ' ', 'Y']
    assert result == expected


def test_tokenize_format_3a():
    result = dt.tokenize_format('D, d M Y', 'python')
    expected = ['D,', ' ', 'd', ' ', 'M', ' ', 'Y']
    assert result == expected


def test_tokenize_format_3b():
    result = dt.tokenize_format('%a, %d %b %Y %T %z', 'python')
    expected = ['%a', ',', ' ', '%d', ' ', '%b', ' ', '%Y', ' ',
                '%T', ' ', '%z']
    assert result == expected


def test_tokenize_format_3c():
    result = dt.tokenize_format('%a, and %-d %b %-Y %T  %%', 'python')
    expected = ['%a', ',', ' ', 'and', ' ', '%-d', ' ', '%b', ' ', '%-Y', ' ',
                '%T', '  ', '%%']
    assert result == expected


# translate_dj_py

def test_translate_dj_py_1a():
    result = dt.translate_dj_py('d')
    expected = '%d'
    assert result == expected


# format_dj_py

def test_format_dj_py_1a():
    dt_value = '07-Jan-2021 09:50:07.586525+03:00'
    dt_format = 'D, j M Y H:i:s O'
    format_type = 'django'
    result = dt.format_datetime(dt_value, dt_format, format_type)
    expected = 'Thu, 7 Jan 2021 09:50:07 +0300'
    assert result == expected


def test_format_dj_py_2a():
    dt_value = '07-Jan-2021 09:50:07.586525+03:00'
    dt_format = '%A, %-d %B %Y %-I.%M%p'
    format_type = 'python'
    result = dt.format_datetime(dt_value, dt_format, format_type)
    expected = 'Thursday, 7 January 2021 9.50AM'
    assert result == expected
