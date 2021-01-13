#!/usr/bin/env python3
import logging
from . import job as mjob


def run():
    logging.info('Djist assemble running')
    test = mjob.Job('config.json')
    test.run()


if __name__ == "__main__":
    run()
