#!/usr/bin/env python

import argparse
import re

point_prog = re.compile(r'\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')


def parse_point(s):
    pass



def main(file='tests/test1.desc'):
    print('hi')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', default='tests/test1.desc')
    args = argparser.parse_args()
    main(file=args.file)
