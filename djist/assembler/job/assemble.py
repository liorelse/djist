#!/usr/bin/env python3
"""Djist: Assemble
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import logging
from . import config as conf
from . import job as mjob
from . import page as mpage
from ..template import scanner as mscanner
from ..generics import file


def run():
    logging.info("Djist assemble running")

    # Job
    if conf.MODE_JOB:
        logging.info("Running predefined job")
        config_dict = file.read_io(conf.IO_CONFIG, "dataset")
        job = mjob.Job(config_dict)
        job.run()

    # Run
    elif conf.MODE_RUN:
        logging.info("Running standalone template")
        page_config = {
            "djist_page_template": conf.IO_TEMPLATE,
            "djist_page_dataset": conf.IO_DATASET,
            "djist_output_filename": conf.IO_OUTFILE,
        }
        assemble_page = mpage.Page(page_config)
        assemble_page.process()

    # Scan
    elif conf.MODE_SCAN:
        logging.info("Running template scan")
        raw_template = file.read_io(conf.IO_TEMPLATE, "template")
        scanner = mscanner.Scanner(raw_template)
        scanner.run()


if __name__ == "__main__":
    run()
