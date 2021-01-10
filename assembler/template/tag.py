#!/usr/bin/env python3
"""Djist: Tags and tag actions
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


from pyparsing import (alphas, MatchFirst, Word, SkipTo)
from . import prepper as mprepper


def tag_identifiers():
    return {
        'open': ['{{', '{%', '{#'],
        'close': ['}}', '%}', '#}'],
    }


def match_tag():
    return {
        'deconstruct':
            MatchFirst(['{{', '{%' + Word(alphas), '{#'])
            + SkipTo(MatchFirst(tag_identifiers()['close'])),
    }


def valid_tags():
    pass


def block_tags():
    return {
        'comment': 'endcomment',
        'filter': 'endfilter',
        'for': 'endfor',
        'if': 'endif',
        'with': 'endwith',
    }


def multiblock_tags():
    return {
        'if': ['elif', 'else'],
    }


def expression_argument_tags():
    return ['if', 'elif', 'else']


class Action:

    def __init__(self, action: str = 'ignore', argument: tuple = (),
                 content: str = ''):
        self.main_action = action
        self.action = action
        self.argument = argument
        self.content = content
        # Multiblock
        self.is_multiblock_ = self.action in multiblock_tags().keys()
        self.multiblock_list = []
        if self.is_multiblock():
            self.build_multiblock()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return f'{self.__class__} {self.action}'

    def get_action(self):
        return self.action

    def get_argument(self):
        return self.argument

    def get_content(self):
        return self.content

    def get(self):
        return (self.argument, self.content)

    def get_all(self):
        return (self.action, self.argument, self.content)

    # Multiblock
    def is_multiblock(self):
        return self.is_multiblock_

    def build_multiblock(self):
        mb_prep = mprepper.Prepper()
        tag_list = mb_prep.tags_as_list(self.get_content())
        tag_list = mb_prep.current_level_tags(tag_list, self.get_action())
        self.multiblock_list = mb_prep.segments(
            tag_list, self.get_content(), self.get_action())
        if self.multiblock_list[0].get_action() == 'copy':
            leading_action = self.multiblock_list.pop(0)
            self.content = leading_action.get_content()

    def has_next(self):
        return len(self.multiblock_list) > 0

    def next(self):
        if self.has_next():
            self.action, self.argument, self.content \
                    = self.multiblock_list.pop(0).get_all()
