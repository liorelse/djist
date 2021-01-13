#!/usr/bin/env python3
from typing import List
import sys
import logging
import assembler
import tests


def main(argv: List[str]):
    #print(argv)
    assembler.generics.log.start_logging(log_level='debug',
                                         console_level='info')
    assembler.job.assemble.run()
    logging.shutdown()


if __name__ == "__main__":
    main(sys.argv[1:])
