#!/usr/bin/env python

import unittest

from parser import point_prog, parse_point, parse_map


class TestParser(unittest.TestCase):
    def check_point_prog(self, s, x, y):
        result = point_prog.match(s)
        self.assertIsNotNone(result)
        (a, b) = result.groups()
        self.assertEqual(x, int(a))
        self.assertEqual(y, int(b))

    def check_parse_point(self, s, x, y, rem):
        self.assertEqual(((x, y), rem), parse_point(s))

    def test_point_prog(self):
        self.check_point_prog('(1,2)', 1, 2)
        self.check_point_prog(' (1,2)', 1, 2)
        self.check_point_prog('( 1,2)', 1, 2)
        self.check_point_prog('(1 ,2)', 1, 2)
        self.check_point_prog('(1, 2)', 1, 2)
        self.check_point_prog('(1,2 )', 1, 2)
        self.check_point_prog('(1,2) ', 1, 2)
        self.check_point_prog('(1,2) ', 1, 2)
        self.check_point_prog('(1,2)', 1, 2)
        self.check_parse_point('(1,2),(3, 4)', 1, 2, ',(3, 4)')

    def check_parse_map(self, s, points, rem):
        p, r = parse_map(s)
        self.assertEqual(points, p)
        self.assertEqual(r, rem)

    def test_parse_map(self):
        self.check_parse_map('(1,2),(3,4) # blah', [(1, 2), (3, 4)], '# blah')


if __name__ == '__main__':
    unittest.main()
