#!/usr/bin/python3
"""Djist: Messages
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


# pylint: disable=line-too-long

# General messages
GENERAL_ERROR = 'Could not complete because %s'
EVAL_ATTEMPT = 'Tried to evaluate expression (%s)'
EVAL_ERROR = 'Could not evaluate because %s'
INDEX_OUT_OF_RANGE = 'Invalid index (%s) for list/array length (%s)'
INVALID_DICT_KEY = 'Invalid key (%s) for dictionary/object'
INVALID_LIST_INDEX = 'Invalid index (%s) for list/array'
JSON_DECODE_ERROR = 'The JSON data file (%s) contains an error: %s'
KEY_VALUE = 'Key (%s) has value (%s)'
UNEXPECTED_TYPE = 'Unexpected data type (%s)'

# Filter messages
FILTER_GENERAL = 'Could not be applied: %s'
FILTER_DEFAULT_TYPE_WARNING = '%s filter: Default value used due to a type mismatch.  Expected: %s  Supplied: %s'
FILTER_DEFAULT_VALUE_INFO = '%s filter: Default value (%s) was used (argument %s)'
FILTER_DICTSORT_WARNING = 'dictsort filter: Could not be applied. Key (%s) was not found in all list items.'
FILTER_DICTSORTREVERSED_WARNING = 'dictsortreversed filter: Could not be applied. Key (%s) was not found in all list items.'
FILTER_FIRST_ERROR = 'first filter: ' + FILTER_GENERAL
FILTER_GET_FILTER_ERROR = 'get_digit filter: Could not be applied. Expected digit in range 1-%s. Invalid digit (%s) given.'
FILTER_GET_FILTER_VALUE_ERROR = 'get_digit filter: ' + FILTER_GENERAL
FILTER_JOIN_ERROR = 'join filter: ' + FILTER_GENERAL
FILTER_LAST_ERROR = 'last filter: ' + FILTER_GENERAL
FILTER_LENGTH_ERROR = 'length filter: Could not be applied. No length for object (%s)'

# Processor
PROC_GETDATA_ERROR_NONKEY = 'Key (%s) is not in dataset, and isn\'t a number'
PROC_GETDATA_INVALID_RETURN = 'Invalid return type (%s)'
PROC_GETDATA_LIST_1 = 'Invalid index (%s)'
