#!/usr/bin/python3
from ..generics import (core, file)
from . import prepper as mprepper
from . import processor as mprocessor

"""
Site Assembler: Context
"""

__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


class Context:

    def __init__(self, parent_level: int, source: str = ''):
        self.context_level = parent_level + 1
        self.source_tag_state = list(source.split('.'))
        self.source_tag = str(self.source_tag_state.pop(0))
        self.dataset = {}
        self.prepped_template = []
        self.result = ''

    # Data

    def get_dataset(self):
        return self.dataset

    def set_dataset(self, new_dataset):
        self.dataset.update(new_dataset)

    # Template

    def get_template(self):
        return self.prepped_template

    def set_template(self, raw_template):
        prepper = mprepper.Prepper()
        self.prepped_template.extend(prepper.run(raw_template,
                                                 self.source_tag,
                                                 self.source_tag_state))
        self.template_to_file()

    def template_to_file(self):
        template_report = []
        for action in self.get_template():
            template_report.append(
                f'''TAG: {action.get_action()}\nARGUMENTS:
                {action.get_argument()}\nCONTENT:\n{action.get_content()}
                \n-------------------------------------------------------
                ----------------------------------\n\n''')
        file.write_file(template_report, f'prepped-{self.context_level}')

    # Process

    def process(self):
        processor = mprocessor.Processor(self.context_level)
        self.result = processor.run(self.prepped_template, self.dataset)
        self.prepped_template = []
        return self.result
