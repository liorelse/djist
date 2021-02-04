#!/usr/bin/python3
"""Djist: Messages
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


# pylint: disable=line-too-long


# General messages
STOP_ERROR = "Could not complete. Error: %s"
GENERAL_ERROR = "Could not complete because %s"
EVAL_ATTEMPT = "Tried to evaluate expression (%s)"
EVAL_ERROR = "Could not evaluate because %s"
DATE_FORMAT_ERROR = "The %s date format string (%s) is invalid."
INDEX_OUT_OF_RANGE = "Invalid index (%s) for list/array length (%s)"
INVALID_DICT_KEY = "Invalid key (%s) for dictionary/object."
INVALID_LIST_INDEX = "Invalid index (%s) for list/array."
JSON_DECODE_ERROR = "The JSON data file contains an error: %s"
KEY_VALUE = "Key (%s) has value (%s)."
UNEXPECTED_TYPE = "Unexpected data type (%s)."


# Help
HELP_LOG_LEVEL = (
    "Level of information to output to log file, or 'quiet' for no logging."
)
HELP_CONSOLE_LEVEL = "Level of information sent to console, or 'quiet' for no messages."
HELP_SCAN = "Scan a djist-format template to determine data fields."
HELP_SCAN_TEMPLATE = "Individual template to scan."
HELP_SCAN_DATASET = (
    "Check if dataset contains the required fields to process the template."
)
HELP_SCAN_OUTPUT = "Location to save the scan results. If no location is specified, console logging will be disabled and the scan results streamed to the console instead."
HELP_RUN = "Process an individual djist-format template. A template and dataset should be specified when using this option."
HELP_RUN_TEMPLATE = "Individual template to process."
HELP_RUN_DATASET = "Dataset to use for individual template."
HELP_RUN_OUTPUT = "Location to save the processed template."
HELP_JOB = "Run a job using a config file."
HELP_JOB_CONFIG = "Job configuration file."


# Filter messages
FILTER_GENERAL = "Could not be applied: %s"
FILTER_DEFAULT_TYPE_WARNING = "%s filter: Expected type (%s) but found (%s)"
FILTER_DEFAULT_VALUE_INFO = "%s filter: Default value (%s) was used (argument %s)"
FILTER_VALUE_TYPE_WARNING = "%s filter: Unexpected value type (%s)"
FILTER_VALUE_EMPTY_WARNING = "%s filter: Unexpected empty value."

FILTER_DICTSORT_ERROR = (
    "dictsort filter: Could not be applied. Key (%s) was not found in all list items"
)
FILTER_DICTSORTREVERSED_ERROR = "dictsortreversed filter: Could not be applied. Key (%s) was not found in all list items"
FILTER_DIVISIBLEBY_ERROR = (
    "divisibleby filter: Value (%s) or argument (%s) has an unexpected zero value"
)
FILTER_GET_DIGIT_ARG_ERROR = (
    "get_digit filter: Expected digit in range 1-%s. Invalid digit (%s) given"
)


# Processor
PROC_GETDATA_ERROR_NONKEY = "Key (%s) is not in dataset, and isn't a number"
PROC_GETDATA_INVALID_RETURN = "Invalid return type (%s)"
PROC_GETDATA_LIST_1 = "Invalid index (%s)"
PROC_ACTION_SUCCESS = "Action (%s) was successfully processed"
