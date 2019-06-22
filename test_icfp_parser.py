#!/usr/bin/env python

import glob
import unittest

from icfp_parser import (
    point_prog, act_b_prog,
    parse_point, parse_map, parse_booster_code,
    parse_booster_location, parse_obstacles, parse_boosters, parse_task,
    parse_solution,
)


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
        self.check_parse_map('# blah', [], '# blah')

    def check_parse_booster_code(self, s, b, rem):
        a, r = parse_booster_code(s)
        self.assertEqual(b, a)
        self.assertEqual(rem, r)

    def test_parse_booster_code(self):
        self.check_parse_booster_code(' B ABCDEF', 'B', 'ABCDEF')

    def check_parse_booster_location(self, s, b, p, rem):
        a, c, r = parse_booster_location(s)
        self.assertEqual(b, a)
        self.assertEqual(p, c)
        self.assertEqual(rem, r)

    def test_parse_booster_location(self):
        self.check_parse_booster_location(' B (1,2) ABCDEF', 'B', (1,2), 'ABCDEF')

    def check_parse_obstacles(self, s, obs, rem):
        o, r = parse_obstacles(s)
        self.assertEqual(obs, o)
        self.assertEqual(rem, r)

    def test_parse_obstacles(self):
        self.check_parse_obstacles('(1,2);(3,4),(5,6) # A', [[(1,2)], [(3,4), (5,6)]], '# A')
        self.check_parse_obstacles('# A', [], '# A')

    def check_parse_boosters(self, s, bstr, rem):
        b, r = parse_boosters(s)
        self.assertEqual(bstr, b)
        self.assertEqual(rem, r)

    def test_parse_boosters(self):
        self.check_parse_boosters('B(1,2);C(3,4)# A', [('B',(1,2)), ('C',(3,4))], '# A')
        self.check_parse_boosters('# A', [], '# A')

    def test_parse_task(self):
        # task ::= map # point # obstacles # boosters
        s = '''
        (1,2) , (3, 4) #
        (5, 6) #
        (7, 8) ; (9, 0), (1, 2) ; (3, 4) #
        B (1, 2) ; C (3, 4) # A
        '''
        (m, p, o, b), rem = parse_task(s)
        self.assertEqual(m, [(1,2), (3,4)])
        self.assertEqual(p, (5,6))
        self.assertEqual(o, [[(7,8)], [(9,0), (1,2)], [(3, 4)]])
        self.assertEqual(b, [('B', (1,2)), ('C', (3, 4))])

    def test_parse_every_description(self):
        for filename in glob.glob('problems/*.desc'):
            with open(filename) as f:
                print(filename)
                parse_task(f.read())

    def test_act_b_prog(self):
        a, b = act_b_prog.match(' B ( 1 , 2 )').groups()
        self.assertEqual(int(a), 1)
        self.assertEqual(int(b), 2)

    def test_parse_solution(self):
        sol, _ = parse_solution('W#A#S#D')
        self.assertEqual(sol, [['W'], ['A'], ['S'], ['D']])

    def test_parse_every_solution(self):
        for filename in glob.glob('examples/*.sol'):
            with open(filename) as f:
                print(filename)
                parse_solution(f.read())



if __name__ == '__main__':
    unittest.main()
