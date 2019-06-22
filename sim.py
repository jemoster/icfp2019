#!/usr/bin/env python

import imgcat
import numpy as np

from icfp_parser import parse_task


def fill(m):
    ''' Return a list of points inside of a given map '''
    pass



class Sim:
    def __init__(self, map_, point, obstacles, boosters):
        self.map = map_
        self.point = point
        self.obstacles = obstacles
        self.boosters = boosters
        self.extents = [(min(p[0] for p in map_), min(p[1] for p in map_)),
                        (max(p[0] for p in map_), max(p[1] for p in map_))]
        self.area = fill(map_)


    @classmethod
    def from_string(cls, s):
        (m, p, o, b), _ = parse_task(s)
        return cls(map_=m, point=p, obstacles=o, boosters=b)

    @classmethod
    def from_filename(cls, filename):
        with open(filename) as f:
            return cls.from_string(f.read())


if __name__ == '__main__':
    sim = Sim.from_filename('examples/example-01.desc')
    print(sim)
