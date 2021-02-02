#!/usr/bin/env python3
"""Djist: Template scanner
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


from . import prepper as mprepper
from ..generics import file
from ..template import tag as mtag
from ..job import config as conf


class Scanner:
    """Djist Template Scanner"""

    def __init__(self, raw_template: str):
        self.template = raw_template
        prepper = mprepper.Prepper()
        self.prepped_template = prepper.run(self.template)
        self.value_list = list()
        self.ignored = ["ignore", "copy"]

    def run(self):
        """Run scanner"""

        def argument_filter(token):
            while token.has_next_filter():
                token.load_next_filter()
                while token.has_next_filter_argument():
                    token.load_next_filter_argument()
                    if token.is_filter_argument_name():
                        self.value_list.append(token.get_filter_argument())

        def token_argument(token):
            if token.is_name():
                self.value_list.append(token.get_value())
                if token.is_argument_name():
                    self.value_list.append(token.get_argument())
                if token.is_filtered():
                    argument_filter(token)

        for action in self.prepped_template:
            action: mtag.Action
            if action.get_action() in self.ignored:
                continue
            for token in action.get_argument():
                token_argument(token)

        file.write_io(conf.IO_OUTFILE, "scan", self.value_list)
