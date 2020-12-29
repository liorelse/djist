#!/usr/bin/env python3
from typing import List
import assembler
import sys


def main(argv: List[str]):
    #print(argv)
    assembler.job.assemble.run()


if __name__ == "__main__":
    main(sys.argv[1:])
