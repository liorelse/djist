import pytest
from .context import assembler

tf = assembler.template.token_filter
dt = assembler.generics.date


# add

def test_add_1():
    res = tf.add_filter('7', '3')
    assert res == '10'


def test_add_2():
    res = tf.add_filter('seven', '3')
    assert res == 'seven3'


# addslashes

def test_addslashes_1():
    res = tf.addslashes_filter(r"I'm testing", '')
    assert res == r"I\'m testing"


def test_addslashes_2():
    res = tf.addslashes_filter(r'You are "funny"', '')
    assert res == r'You are \"funny\"'


# date_filter

def input_dates():
    return [
        '2018-06-29 08:15:27.243860',
        'Jun 28 2018 7:40AM',
        'Jun 28 2018 at 7:40AM',
        'September 18, 2017, 22:19:55',
        'Sun, 05/12/1999, 12:30PM',
        'Mon, 21 March, 2015',
        '2018-03-12T10:12:45Z',
        '2018-06-29 17:08:00.586525+00:00',
        '2018-06-29 17:08:00.586525+05:00',
        'Tuesday, 6th September, 2017 at 4:30pm'
    ]

"""
def test_date_filter_1a():
    ""Test all Django directives individually"
    date_format = '2021-07-01 09:50:07.586525+03:00'
    django_directives = dt.directives_dj_py().keys()
    expected_list = [
        '',
    ]
    result_list = []
    for date in input_dates():
        for djdir in django_directives:
            result = tf.date_filter(date, djdir)
            print(result)
            result_list.append(result)
    assert result_list == expected_list



def test_date_filter_2a():
    date_format = 'j-M-Y (l) H:i:s:u *A e;django'
    expected_list = [
        '',
    ]
    result_list = []
    for date in input_dates():
        result = tf.date_filter(date, date_format)
        print(result)
        result_list.append(result)
    assert result_list == expected_list"""
