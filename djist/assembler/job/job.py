#!/usr/bin/python3
"""Djist: Job from config file
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import logging
from ..generics import file
from . import page as mpage


class Job:
    """Djist Job"""

    def __init__(self, config: dict):
        logging.debug("create new job")
        self.config = config

    def base(self):
        if "djist_base_location" in self.config.keys():
            return self.config.get("djist_base_location")
        return ""

    def enabled(self, config: dict) -> bool:
        if "djist_enabled" in config.keys():
            return config.get("djist_enabled")
        return True

    def run(self):
        if self.enabled(self.config):
            job_name = self.config.pop("djist_job_name")
            logging.debug(f"start job: {job_name}")
            sites = self.config.pop("djist_sites")
            for site in sites:
                if isinstance(site, str):
                    site = file.path_join(self.base(), site)
                    site = file.json_to_dict(site)
                site_config = {**self.config, **site}
                if self.enabled(site_config):
                    site_name = site_config.get("djist_site_name")
                    logging.debug(f"start site: {site_name}")
                    pages = site_config.pop("djist_pages")
                    for page in pages:
                        if isinstance(page, str):
                            page = file.path_join(self.base(), page)
                            page = file.json_to_dict(page)
                        page_config = {**site_config, **page}
                        if self.enabled(page_config):
                            page_name = page_config.get("djist_page_name")
                            logging.debug(f"start page: {page_name}")
                            assemble_page = mpage.Page(page_config)
                            assemble_page.process()
                            logging.debug(f"completed page: {page_name}")
                    logging.debug(f"completed site: {site_name}")
            logging.debug(f"completed job: {job_name}")
