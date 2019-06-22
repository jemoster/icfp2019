#!/usr/bin/env python

import argparse
import re

point_prog = re.compile(r'^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')


def parse_point(s):
    result = point_prog.match(s)
    a, b = result.groups()
    return (int(a), int(b)), s[result.span()[1]:]


def parse_map(s):
    # do parse_point while maybe_consume_comma
    pass


def main(file='tests/test1.desc'):
    parse_point('(1,2)')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', default='tests/test1.desc')
    args = argparser.parse_args()
    main(file=args.file)
