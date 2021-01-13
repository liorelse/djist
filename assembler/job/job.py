#!/usr/bin/python3
"""Djist: Job from config file
"""
__author__ = "llelse"
__version__ = "0.1.0"
__license__ = "GPLv3"


import logging
from ..generics import file
from . import page as mpage


class Job:

    def __init__(self, config: str):
        logging.debug('create new job')
        self.config = file.json_to_dict(config)
        # self.output_job = self.config.get('sa_output_job')
        self.sites = self.config.pop('sa_sites')

    def run(self):
        logging.debug('start job')
        for site in self.sites:
            if isinstance(site, str):
                site = file.json_to_dict(site)
            site_config = {**self.config, **site}
            pages = site_config.pop('sa_pages')
            for page in pages:
                if isinstance(page, str):
                    page = file.json_to_dict(page)
                page_config = {**site_config, **page}
                assemble_page = mpage.Page(page_config)
                assemble_page.process()
        logging.debug('completed job')
