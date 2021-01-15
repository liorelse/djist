#!/usr/bin/python3
"""Djist: Messages
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


# General messages
GENERAL_ERROR = 'Could not complete because %s'
EVAL_ATTEMPT = 'Tried to evaluate expression (%s)'
EVAL_ERROR = 'Could not evaluate because %s'
INDEX_OUT_OF_RANGE = 'Invalid index (%s) for list/array length (%s)'
INVALID_DICT_KEY = 'Invalid key (%s) for dictionary/object'
INVALID_LIST_INDEX = 'Invalid index (%s) for list/array'
KEY_VALUE = 'Key (%s) has value (%s)'
UNEXPECTED_TYPE = 'Unexpected data type (%s)'

# Filter messages
FILTER_DICTSORT_WARNING = 'dictsort filter: Could not be applied. Key (%s) was not found in all list items.'
FILTER_DICTSORTREVERSED_WARNING = 'dictsortreversed filter: Could not be applied. Key (%s) was not found in all list items.'
FILTER_GET_FILTER_ERROR = 'get_digit filter: Could not be applied. Expected digit in range 1-%s. Invalid digit (%s) given.'
FILTER_GET_FILTER_VALUE_ERROR = 'get_digit filter: Could not be applied: %s'

# Processor
PROC_GETDATA_ERROR_NONKEY = 'Key (%s) is not in dataset, and isn\'t a number'
PROC_GETDATA_INVALID_RETURN = 'Invalid return type (%s)'
PROC_GETDATA_LIST_1 = 'Invalid index (%s)'
