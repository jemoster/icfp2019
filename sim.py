#!/usr/bin/env python

import os
# import imgcat
import numpy as np
from PIL import Image, ImageDraw

from icfp_parser import parse_task


def save_image(mat, name, dir='./'):
    new_im = Image.fromarray(mat * 255).transpose(Image.ROTATE_90)
    os.makedirs(dir, exist_ok=True)
    new_im.save(os.path.join(dir, "{}.png".format(name)))


class Sim:
    def __init__(self, map_, point, obstacles, boosters):
        self.map = map_
        self.point = point
        self.obstacles = obstacles
        self.boosters = boosters
        self.unwrapped = ((self.obstacles + self.map) != 1).astype(np.uint8)

    @classmethod
    def from_string(cls, s):
        (map_outline, start, obstacle_outine, boosters_list), _ = parse_task(s)
        static_map, obstacles, boosters = Sim._generate_maps(map_outline, obstacle_outine, boosters_list)
        return cls(map_=static_map, point=start, obstacles=obstacles, boosters=boosters)

    @classmethod
    def _generate_maps(cls, map_outline, obstacle_outine, boosters_list):
        x, y = zip(*map_outline)
        map_dim = max(x), max(y)

        def draw_shape(data, poly, fill_value):
            img = Image.fromarray(data)
            draw = ImageDraw.Draw(img)
            poly = [(p[1] * 10, p[0] * 10) for p in poly]
            draw.polygon(poly, fill=fill_value)
            new_data = np.asarray(img)
            return new_data

        # Generate base map
        static_map = np.ones((map_dim[0] * 10, map_dim[1] * 10), dtype=np.uint8)
        static_map = draw_shape(static_map, map_outline, 0)
        static_map = static_map[5::10, 5::10]

        # Generate obstacle map
        obstacles = np.zeros((map_dim[0] * 10, map_dim[1] * 10), dtype=np.uint8)
        # obstacles = map
        for obstacle in obstacle_outine:
            obstacles = draw_shape(obstacles, obstacle, 1)
        obstacles = obstacles[5::10, 5::10]

        # Generate booster map
        boosters = {
            'B': np.zeros(map_dim, dtype=np.uint8),
            'F': np.zeros(map_dim, dtype=np.uint8),
            'L': np.zeros(map_dim, dtype=np.uint8),
            'X': np.zeros(map_dim, dtype=np.uint8),
            'R': np.zeros(map_dim, dtype=np.uint8),
            'C': np.zeros(map_dim, dtype=np.uint8),
        }

        for booster_type, booster_pt in boosters_list:
            boosters[booster_type][booster_pt[0]][booster_pt[1]] = 1

        return static_map, obstacles, boosters

    @classmethod
    def from_filename(cls, filename):
        with open(filename) as f:
            return cls.from_string(f.read())

    def save_img_state(self, dir='./'):
        save_image(self.map, 'map', dir)
        save_image(self.obstacles, 'obstacles', dir)
        save_image(self.map + self.obstacles, 'blocked', dir)
        save_image(self.unwrapped, 'unwrapped', dir)
        for name, m in self.boosters.items():
            save_image(m, 'boosters-{}'.format(name), dir)


if __name__ == '__main__':
    sim = Sim.from_filename('problems/prob-150.desc')
    sim.save_img_state('./tmp')
