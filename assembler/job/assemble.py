#!/usr/bin/env python3
from . import job as mjob


def run():
    test = mjob.Job('config.json')
    test.run()


if __name__ == "__main__":
    run()
