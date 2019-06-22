#!/usr/bin/env python

import unittest

from parser import point_prog, parse_point


class TestParser(unittest.TestCase):
    def check_point_prog(self, s, x, y):
        result = point_prog.match(s)
        self.assertIsNotNone(result)
        a, b = result.groups()
        self.assertEqual(x, int(a))
        self.assertEqual(y, int(b))
        self.assertEqual((x, y), parse_point(s))


    def test_point_prog(self):
        self.check_point_prog('(1,2)', 1, 2)
        self.check_point_prog(' (1,2)', 1, 2)
        self.check_point_prog('( 1,2)', 1, 2)
        self.check_point_prog('(1 ,2)', 1, 2)
        self.check_point_prog('(1, 2)', 1, 2)
        self.check_point_prog('(1,2 )', 1, 2)
        self.check_point_prog('(1,2) ', 1, 2)


if __name__ == '__main__':
    unittest.main()
