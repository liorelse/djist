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
    """Djist Job"""

    def __init__(self, config: dict):
        logging.debug("create new job")
        self.config = config
        self.sites = self.config.pop("djist_sites")

    def run(self):
        logging.debug("start job")
        for site in self.sites:
            if isinstance(site, str):
                site = file.json_to_dict(site)
            site_config = {**self.config, **site}
            pages = site_config.pop("djist_pages")
            for page in pages:
                if isinstance(page, str):
                    page = file.json_to_dict(page)
                page_config = {**site_config, **page}
                assemble_page = mpage.Page(page_config)
                assemble_page.process()
        logging.debug("completed job")
