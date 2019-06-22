#!/usr/bin/env python

import argparse
import re

point_prog = re.compile(r'^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')
comma_prog = re.compile(r'^\s*,\s*')


def parse_point(s):
    ''' Returns ((x, y), remainder) '''
    result = point_prog.match(s)
    a, b = result.groups()
    return (int(a), int(b)), s[result.span()[1]:]


def maybe_consume_comma(s):
    ''' Returns bool if we ate a comma, and remainder string '''
    result = comma_prog.match(s)
    if result is None:
        return False, s
    return True, s[result.span()[1]:]


def parse_map(s):
    ''' Return list of points, and remainder string '''
    points = []
    is_another_point = True
    while is_another_point:
        p, s = parse_point(s)
        points.append(p)
        is_another_point, s = maybe_consume_comma(s)
    return points, s


def main(file='tests/test1.desc'):
    parse_point('(1,2)')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', default='tests/test1.desc')
    args = argparser.parse_args()
    main(file=args.file)
