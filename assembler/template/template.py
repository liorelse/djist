#!/usr/bin/python3
from ..generics import core, file
from . import context as mcontext

"""
Site Assembler: Template
"""

__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


class Template:
    def __init__(self, config: dict = {}):
        self.config = config
        self.processed_template = ""
        self.page_context = mcontext.Context(0)
        # Template
        self.page_template = file.file_to_str(self.config.get("sa_page_template"))
        self.page_context.set_template(self.page_template)
        # Dataset
        self.resolve_dataset(self.config.get("sa_page_dataset"))

    def set_dataset(self, new_dataset: dict):
        self.page_context.set_dataset(new_dataset)

    def resolve_dataset(self, dataset: list or str or dict):
        if not isinstance(dataset, list):
            dataset = [dataset]
        for src in dataset:
            if isinstance(src, str):
                # Future resolve id
                self.set_dataset(file.json_to_dict(src))
            elif isinstance(src, dict):
                self.set_dataset(src)

    def write_page_to_file(self):
        if "sa_output_job" in self.config.keys():
            path_output_base = self.config.get("sa_output_job")
        else:
            path_output_base = ""
        if "sa_output_site" in self.config.keys():
            path_output_site = self.config.get("sa_output_site")
        else:
            path_output_site = ""
        full_path = file.path_join(path_output_base, path_output_site)
        if "sa_output_filename" in self.config.keys():
            path_output_filename = self.config.get("sa_output_filename")
        else:
            path_output_filename = ""
        file.write_file(self.processed_template, path_output_filename, full_path)

    def process(self):
        self.processed_template = self.page_context.process()
        self.write_page_to_file()
