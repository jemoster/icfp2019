#!/usr/bin/env python

import argparse
import numpy as np
from PIL import Image, ImageDraw
from icfp_parser import parse_task

BOOSTER_SCALE = 1


def map_size(map):
    x, y = zip(*map)
    return max(x), max(y)


def draw_shape(data, poly, fill_value):
    img = Image.fromarray(data)
    draw = ImageDraw.Draw(img)
    poly = [(p[1], p[0]) for p in poly]
    draw.polygon(poly, fill=fill_value)
    new_data = np.asarray(img)
    return new_data


def output(mat, name, scale=255):
    new_im = Image.fromarray(mat * scale).transpose(Image.ROTATE_90)
    new_im.save("{}.png".format(name))


def generate_maps(map_outline, obstacle_outine, boosters_list):
    map_dim = map_size(map_outline)

    # Generate base map
    static_map = np.ones(map_dim, dtype=np.uint8)
    static_map = draw_shape(static_map, map_outline, 0)

    # Generate obstacle map
    obstacles = np.zeros(map_dim, dtype=np.uint8)
    # obstacles = map
    for obstacle in obstacle_outine:
        obstacles = draw_shape(obstacles, obstacle, 1)

    # Generate booster map
    boosters = np.zeros(map_dim, dtype=np.uint8)
    for booster_type, booster_pt in boosters_list:
        boosters[booster_pt[0]][booster_pt[1]] = ord(booster_type)

    return static_map, obstacles, boosters


def main(file):
    with open(file) as f:
        s = f.read()
    (map_outline, start, obstacle_outine, boosters_list), _ = parse_task(s)

    static_map, obstacles, boosters = generate_maps(map_outline, obstacle_outine, boosters_list)

    output(static_map, 'map')
    output(obstacles, 'obstacles')
    output(obstacles + static_map, 'filled')
    output(boosters, 'boosters', BOOSTER_SCALE)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', default='tests/test1.desc')
    args = argparser.parse_args()
    main(file=args.file)
