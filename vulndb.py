import argparse

from commands import cmd_check, cmd_safe
from database import DEFAULT_DB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("product")
    parser.add_argument("version", nargs="?")
    args = parser.parse_args()
    args.db = DEFAULT_DB

    if args.version is None:
        cmd_safe(args)
    else:
        cmd_check(args)


if __name__ == "__main__":
    main()
