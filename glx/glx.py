#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from textwrap import dedent


__version__ = "0.3.3"


def main():
    if "--version" in sys.argv[1:]:
        print(__version__)
        exit(0)
    elif "--help" in sys.argv[1:]:
        print("glx init")
        exit(0)

    print("test")


if __name__ == "__main__":
    main()
