#!/usr/bin/python3
"""Djist: Main module
"""
__author__ = "llelse"
__version__ = "0.2.0"
__license__ = "GPLv3"


import argparse
import logging
from datetime import datetime
import assembler

# import tests


def parse_argument():
    """Set up and parse the argument"""
    msg = assembler.generics.msg

    # Top level
    parser = argparse.ArgumentParser(
        prog="djist", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "--log-file",
        type=argparse.FileType("w"),
        default="djist.log",
        help=msg.HELP_LOG_LEVEL,
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["quiet", "critical", "error", "warning", "info", "debug"],
        help=msg.HELP_LOG_LEVEL,
    )
    parser.add_argument(
        "--console",
        default="warning",
        choices=["quiet", "critical", "error", "warning", "info", "debug"],
        help=msg.HELP_CONSOLE_LEVEL,
    )
    subparsers = parser.add_subparsers(dest="djist_mode")

    # Scan
    parser_scan = subparsers.add_parser("scan", help=msg.HELP_SCAN)
    parser_scan.add_argument(
        "template",
        type=argparse.FileType("r"),
        help=msg.HELP_SCAN_TEMPLATE,
    )
    parser_scan.add_argument(
        "--dataset",
        type=argparse.FileType("r"),
        default=None,
        help=msg.HELP_SCAN_DATASET,
    )
    parser_scan.add_argument(
        "--output-file",
        type=argparse.FileType("w"),
        default=None,
        help=msg.HELP_SCAN_OUTPUT,
    )

    # Run
    parser_run = subparsers.add_parser("run", help=msg.HELP_RUN)
    parser_run.add_argument(
        "template",
        type=argparse.FileType("r"),
        help=msg.HELP_RUN_TEMPLATE,
    )
    parser_run.add_argument(
        "dataset",
        type=argparse.FileType("r"),
        default=None,
        help=msg.HELP_RUN_DATASET,
    )
    parser_run.add_argument(
        "--output-file",
        type=argparse.FileType("w"),
        help=msg.HELP_RUN_OUTPUT,
    )

    # Job
    parser_job = subparsers.add_parser("job", help=msg.HELP_JOB)
    parser_job.add_argument(
        "config",
        type=argparse.FileType("r"),
        default=None,
        help=msg.HELP_JOB_CONFIG,
    )

    # parse
    return parser.parse_args()


def configure():
    """Configure the run with the parsed argument"""
    args = parse_argument()
    conf = assembler.job.config

    # Log
    conf.LOG_FILE_LEVEL = args.log_level
    conf.LOG_FILE_LOCATION = args.log_file.name
    conf.IO_LOG = args.log_file
    if conf.LOG_FILE_LEVEL == "quiet":
        conf.LOG_FILE = False
        conf.IO_LOG.close()
    else:
        conf.LOG_FILE = True
    conf.LOG_CONSOLE_LEVEL = args.console
    if args.console == "quiet":
        conf.LOG_CONSOLE = False
    else:
        conf.LOG_CONSOLE = True

    # Scan
    if args.djist_mode == "scan":
        conf.MODE_SCAN = True
        conf.IO_TEMPLATE = args.template
        if args.dataset:
            conf.IO_DATASET = args.dataset
        else:
            conf.IO_DATASET = None
        if args.output_file:
            conf.IO_OUTFILE = args.output_file
        else:
            conf.IO_OUTFILE = None
            conf.LOG_CONSOLE = False

    # Run
    elif args.djist_mode == "run":
        conf.MODE_RUN = True
        conf.IO_TEMPLATE = args.template
        conf.IO_DATASET = args.dataset
        if args.output_file:
            conf.IO_OUTFILE = args.output_file
        else:
            filename = f"{conf.IO_TEMPLATE.name}.html"
            conf.IO_OUTFILE = assembler.generics.file.open_file(filename, "w")

    # Job
    elif args.djist_mode == "job":
        conf.MODE_JOB = True
        conf.IO_CONFIG = args.config


def main():
    """Djist"""
    run_time = datetime.now()
    configure()
    assembler.job.log.start_logging()
    assembler.job.assemble.run()
    logging.debug("Run time: %s", datetime.now() - run_time)
    assembler.generics.core.close()


if __name__ == "__main__":
    main()
