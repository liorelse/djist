#!/usr/bin/env python3
from pyparsing import (Combine, printables, ZeroOrMore, MatchFirst, Word,
                       quotedString, Group, delimitedList)
from . import token_filter as tf

"""
Module Docstring
"""

__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


class Token:

    def __init__(self):
        self.token_string = ''
        # Token
        self.value = ''
        self.is_literal_ = False
        self.is_name_ = False
        self.is_verbatim_ = False
        self.is_expression_ = False
        # Argument
        self.has_argument_ = False
        self.argument_value = ''
        self.argument_is_literal = False
        self.argument_is_name = False
        # Filter
        self.is_filtered_ = False
        self.filter_list = []
        self.filter_value = ''
        self.filter_argument_value = ''
        self.filter_argument_is_literal = False
        self.filter_argument_is_name = False
        self.filter_is_boolean = False

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return f'{self.__class__} {self.token_string}'

    # Utilties
    def is_quoted(self, val: str):
        return val[0] == val[-1] and val[0] in ('\'', '\"')

    def unquote(self, val: str):
        return val[1:-1]

    # Token building
    def build(self, token_string: str, verbatim: bool = False,
              expression: bool = False):
        self.token_string = token_string
        self.is_verbatim_ = verbatim
        self.is_expression_ = expression

        match_literal = quotedString
        match_name = Word(printables, excludeChars='|:')
        match_argument = ZeroOrMore(
            Combine(":" + MatchFirst(match_literal | match_name)))
        match_filter = Group(ZeroOrMore(
            Group(Combine("|" + match_name) + match_argument)))
        match = (Group(match_literal + match_argument) + match_filter) \
            | (Group(match_name + match_argument) + match_filter)

        if self.is_verbatim_:
            match_list = [[token_string]]
        else:
            match_list = delimitedList(
                match, ' ').parseString(token_string).asList()

        # Set token
        if len(match_list) > 0:
            token_list = match_list.pop(0)
            if len(token_list) > 0:
                self.value = token_list.pop(0)
                if self.is_quoted(self.value):
                    if not self.is_verbatim_:
                        self.is_literal_ = True
                    self.value = self.unquote(self.value)
                else:
                    if not self.is_verbatim_:
                        self.is_name_ = True
            # Set argument
            if len(token_list) > 0:
                self.has_argument_ = True
                self.argument_value = token_list.pop(0)[1:]
                if self.is_quoted(self.argument_value):
                    self.argument_is_literal = True
                    self.argument_value = self.unquote(self.argument_value)
                else:
                    self.argument_is_name = True
        # Set filter
        if len(match_list) > 0:
            filter_list = match_list.pop(0)
            for filter in filter_list:
                self.is_filtered_ = True
                token_filter = filter.pop(0)[1:]
                f_type = ''
                if token_filter in tf.boolean_filters:
                    f_type = 'boolean'
                f_arg = ''
                f_arg_type = ''
                if filter:
                    f_arg = filter.pop(0)[1:]
                    if self.is_quoted(f_arg):
                        f_arg = self.unquote(f_arg)
                        f_arg_type = 'literal'
                    else:
                        f_arg_type = 'name'
                self.filter_list.append((token_filter, f_type, f_arg, f_arg_type))

    def rebuild(self):
        self.build(self.token_string, self.is_verbatim_)

    # Token

    def get_value(self):
        return self.value

    def is_literal(self):
        return self.is_literal_

    def is_name(self):
        return self.is_name_

    def is_verbatim(self):
        return self.is_verbatim_

    def is_expression(self):
        return self.is_expression_

    # Argument

    def get_argument(self):
        return self.argument_value

    def is_argument_literal(self):
        return self.argument_is_literal

    def is_argument_name(self):
        return self.argument_is_name

    # Filter

    def is_filtered(self):
        return self.is_filtered_

    def has_next_filter(self):
        return len(self.filter_list) > 0

    def load_next_filter(self):
        if self.has_next_filter():
            f_value, f_type, f_arg_value, f_arg_type = self.filter_list.pop(0)
            self.filter_value = f_value
            self.filter_argument_value = f_arg_value
            if 'boolean' in f_type:
                self.filter_is_boolean = True
            if 'literal' in f_arg_type:
                self.filter_argument_is_literal = True
            elif 'name' in f_arg_type:
                self.filter_argument_is_name = True


    def get_filter_value(self):
        return self.filter_value

    def get_filter_argument(self):
        return self.filter_argument_value

    def is_filter_argument_literal(self):
        return self.filter_argument_is_literal

    def is_filter_argument_name(self):
        return self.filter_argument_is_name

    def is_filter_boolean(self):
        return self.filter_is_boolean
