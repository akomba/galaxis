import argparse
import sys

# handles common arguments for galaxis apps
# --version
# --community


def parsecommon():
    global __version__

    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)
