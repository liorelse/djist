#!/usr/bin/python3
import re
from ..generics import core
from . import tag as mtag
from . import token as mtoken
from pyparsing import (Combine, printables, ZeroOrMore, MatchFirst, Literal,
                       quotedString, Word, CaselessKeyword, delimitedList)


"""
Site Assembler: Prepper
"""

__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


class Prepper:

    def __init__(self):
        self.prepped_template = [('ignore', '', '')]
        # tag, argument, full tag, start postition, end position
        self.tag_list = [('', '', '', 0, 0)]
        self.matching_tags = mtag.block_tags()
        self.multiblock_tags = mtag.multiblock_tags()
        self.tag_patterns = {
            'all': r'((?s).*)',
            'tags_list':
            r'({#[\s\S]*?[\s\S]#})|({{[\s\S]*?[\s\S]}})|({%[\s\S]*?[\s\S]%})',
        }

        self.match_literal = quotedString
        self.match_name = Word(printables, excludeChars='|:')
        self.match_argument = ZeroOrMore(
            ":" + MatchFirst(self.match_literal | self.match_name))
        self.match_filter = ZeroOrMore(
            "|" + self.match_name + self.match_argument)

        self.match_lit_w_argument = self.match_literal + self.match_argument
        self.match_name_w_argument = self.match_name + self.match_argument
        self.match_literal_w_filter = Combine(
            self.match_lit_w_argument + self.match_filter)
        self.match_name_w_filter = Combine(
            self.match_name_w_argument + self.match_filter)

        self.argument_patterns = {
            'all': ZeroOrMore(self.match_literal_w_filter
                              | self.match_name_w_filter),
            # 'if': ZeroOrMore(self.match_literal),
            'filter': ZeroOrMore(self.match_name_w_filter),
            'firstof': ZeroOrMore(self.match_literal | self.match_name),
            'for': ZeroOrMore(Combine(self.match_name_w_argument)
                              + CaselessKeyword("in")
                              + self.match_name_w_argument),
            # 'replace': MatchFirst(self.match_name_w_filter),
            'usedataset': MatchFirst(self.match_literal
                                     + ZeroOrMore(CaselessKeyword("as")
                                                  + self.match_name_w_filter)),
        }

    def is_block_tag(self, action_tag):
        return action_tag in self.matching_tags.keys()

    def is_end_tag(self, action_tag):
        return action_tag in self.matching_tags.values()

    def is_multiblock_tag(self, action_tag):
        return action_tag in self.multiblock_tags.keys()
    
    def is_multiblock_match(self, action_tag: str, main_multiblock_tag: str):
        if not core.is_empty(main_multiblock_tag):
            return action_tag in self.multiblock_tags.get(main_multiblock_tag)
        return False

    def is_multiblock_inner_tag(self, action_tag: str = '',
                                main_multiblock_tag: str = ''):
        if not core.is_empty(main_multiblock_tag):
            return self.is_multiblock_match(action_tag, main_multiblock_tag)
        else:
            for multiblock_tag in self.multiblock_tags.values():
                if action_tag in multiblock_tag:
                    return True
        return False



    def get_end_tag(self, action_tag):
        return self.matching_tags[action_tag]

    def pattern(self, pattern):
        if pattern not in self.tag_patterns.keys():
            pattern = 'all'
        return self.tag_patterns[pattern]

    def arguments(self, action_tag, argument_string):
        # Tags with Verbatim arguments
        verbatim = action_tag in (None,)  # Add tag for verbatim tags
        expression = action_tag in mtag.expression_argument_tags()
        if action_tag not in self.argument_patterns.keys():
            action_tag = 'all'

        if verbatim:
            token_list = [argument_string]
        else:
            match = self.argument_patterns[action_tag]
            token_list = delimitedList(match, ' ').parseString(
                argument_string).asList()

        tokens = []
        for token_string in token_list:
            token = mtoken.Token()
            token.build(token_string, verbatim, expression)
            tokens.append(token)
        return tuple(tokens)

    def split_tag(self, full_tag: str):
        decon_match = mtag.match_tag()['deconstruct']
        decon_tag = decon_match.parseString(full_tag).asList()
        tag_group = decon_tag.pop(0)
        if tag_group == '{{' and len(decon_tag) > 0:
            return ('replace', ' '.join(decon_tag[0:]).strip())
        elif tag_group == '{%' and len(decon_tag) == 2:
            return (decon_tag[0].lower(), decon_tag[1].strip())
        elif tag_group == '{#':
            return ('replace', ' '.join(decon_tag[1:]))

    def tags_as_list(self, raw_template: str = ''):
        tag_list = []
        action, argument, full_tag = ('',)*3
        for match in re.finditer(self.pattern('tags_list'), raw_template):
            if match.group(1):
                full_tag = str(match.group(1))
                action, argument = ('ignore', '')
            elif match.group(2):
                full_tag = str(match.group(2))
                action, argument = self.split_tag(full_tag)
            elif match.group(3):
                full_tag = str(match.group(3))
                action, argument = self.split_tag(full_tag)
            tag_list.append((action, argument, full_tag,
                             match.start(), match.end()))
        return tag_list

    def current_level_tags(self, tag_list: list = [], multiblock: str = ''):
        checked_tag_list = []
        running_level = 0
        end_tag = ''
        if core.not_empty(multiblock):
            running_level = + 1
        for action_tag, argument, full_tag, start, end in tag_list:
            if self.is_block_tag(action_tag):
                if running_level == 0:
                    checked_tag_list.append(
                        (action_tag, argument, full_tag, start, end))
                    end_tag = self.get_end_tag(action_tag)
                running_level += 1
            elif self.is_end_tag(action_tag):
                if running_level == 1 and action_tag == end_tag:
                    checked_tag_list.append(
                        (action_tag, argument, full_tag, start, end))
                    end_tag = ''
                running_level -= 1
            elif self.is_multiblock_inner_tag(action_tag, multiblock):
                if running_level == 1 \
                        and self.is_multiblock_match(action_tag, multiblock):
                    checked_tag_list.append(
                        (action_tag, argument, full_tag, start, end))
            else:
                if running_level == 0:
                    checked_tag_list.append(
                        (action_tag, argument, full_tag, start, end))
        return checked_tag_list

    def segments(self, tag_list: list, raw_template: str,
                 multiblock: str = ''):
        sliced = []
        list_index = 0

        # Copy content to single segment if no tags are present
        if len(tag_list) == list_index:
            sliced.append(mtag.Action('copy', (), raw_template))

        # Change tags into segments for processing
        while len(tag_list) > list_index:
            # pylint: disable=unused-variable
            action_tag, argument, full_tag, tag_start, tag_end \
                = tag_list[list_index]
            argument = self.arguments(action_tag, argument)

            if len(tag_list) - list_index == 1:
                next_tag_start = len(raw_template)
            else:
                next_tag_start = tag_list[list_index + 1][3]

            # Copy segment before first tag encountered
            if list_index == 0:
                sliced.append(mtag.Action(
                    'copy', (), raw_template[0:tag_start]))

            if self.is_block_tag(action_tag):
                content = raw_template[tag_end:next_tag_start]
                sliced.append(mtag.Action(action_tag, argument, content))
            elif self.is_end_tag(action_tag):
                content = raw_template[tag_end:next_tag_start]
                sliced.append(mtag.Action('copy', (), content))
            elif self.is_multiblock_inner_tag(action_tag, multiblock):
                content = raw_template[tag_end:next_tag_start]
                sliced.append(mtag.Action(action_tag, argument, content))
            else:
                sliced.append(mtag.Action(action_tag, argument, ''))
                content = raw_template[tag_end:next_tag_start]
                sliced.append(mtag.Action('copy', (), content))

            list_index += 1
        return sliced

    def run(self, raw_template: str, src: str = '', src_state: list = []):
        # print(tags_as_list(raw_template))
        self.tag_list = self.current_level_tags(
            self.tags_as_list(raw_template))
        self.prepped_template = self.segments(self.tag_list, raw_template)
        return self.prepped_template
