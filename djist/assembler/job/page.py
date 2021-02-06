#!/usr/bin/python3
"""Djist: Page
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import logging
from io import TextIOWrapper
from ..generics import file
from ..template import context as c


class Page:
    "Djist Page"
    def __init__(self, config: dict):
        logging.debug("create new page")
        self.config = config
        self.page_context = c.Context(0)
        self.processed_template = ""
        # Template
        self.page_template = self.read_template(self.config.get("djist_page_template"))
        self.page_context.set_template(self.page_template)
        # Dataset
        self.resolve_dataset(self.config.get("djist_page_dataset"))

    def read_template(self, config_template: str or TextIOWrapper) -> str:
        if isinstance(config_template, TextIOWrapper):
            return file.read_template(config_template)
        elif isinstance(config_template, str):
            return file.file_to_str(config_template)

    def set_dataset(self, new_dataset: dict):
        self.page_context.set_dataset(new_dataset)

    def resolve_dataset(self, dataset: list or str or dict or TextIOWrapper):
        if not isinstance(dataset, list):
            dataset = [dataset]
        for src in dataset:
            if isinstance(src, TextIOWrapper):
                self.set_dataset(file.read_json_dataset(src))
            elif isinstance(src, str):
                # Future resolve id
                self.set_dataset(file.json_to_dict(src))
            elif isinstance(src, dict):
                self.set_dataset(src)

    def write_page_to_file(self):
        if "djist_output_job" in self.config.keys():
            path_output_base = self.config.get("djist_output_job")
        else:
            path_output_base = ""
        if "djist_output_site" in self.config.keys():
            path_output_site = self.config.get("djist_output_site")
        else:
            path_output_site = ""
        full_path = file.path_join(path_output_base, path_output_site)
        if "djist_output_filename" in self.config.keys():
            path_output_filename = self.config.get("djist_output_filename")
        else:
            path_output_filename = ""
        if isinstance(path_output_filename, TextIOWrapper):
            file.write_io(path_output_filename, "template", self.processed_template)
        else:
            file.write_file(self.processed_template, path_output_filename, full_path)

    def process(self):
        logging.debug("start page")
        self.processed_template = self.page_context.process()
        self.write_page_to_file()
        logging.debug("completed page")
