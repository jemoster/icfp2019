#!/usr/bin/env python

import argparse
import re

point_prog = re.compile(r'^\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')
comma_prog = re.compile(r'^\s*,\s*')
hash_prog = re.compile(r'^\s*#\s*')
semicolon_prog = re.compile(r'^\s*;\s*')
booster_prog = re.compile(r'^\s*([BFLXRC])\s*')
act_b_prog = re.compile(r'^\s*B\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')
act_t_prog = re.compile(r'^\s*T\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*')
valid_acts = 'WASDZEQFLCR'  # Doesn't include B action


def parse_point(s):
    ''' Returns ((x, y), remainder) '''
    result = point_prog.match(s)
    a, b = result.groups()
    return (int(a), int(b)), s[result.span()[1]:]


def consume_hash(s):
    ''' Remove a preceding hash '''
    result = hash_prog.match(s)
    return s[result.span()[1]:]


def maybe_consume_hash(s):
    ''' Returns bool if we ate a hash, and remainder string '''
    result = hash_prog.match(s)
    if result is None:
        return False, s
    return True, s[result.span()[1]:]


def maybe_consume_comma(s):
    ''' Returns bool if we ate a comma, and remainder string '''
    result = comma_prog.match(s)
    if result is None:
        return False, s
    return True, s[result.span()[1]:]


def maybe_consume_semicolon(s):
    ''' Returns bool if we ate a semicolon, and remainder string '''
    result = semicolon_prog.match(s)
    if result is None:
        return False, s
    return True, s[result.span()[1]:]


def parse_map(s):
    ''' Return list of points, and remainder string '''
    points = []
    try:
        parse_point(s)
        is_another_point = True
    except AttributeError:
        is_another_point = False
    while is_another_point:
        p, s = parse_point(s)
        points.append(p)
        is_another_point, s = maybe_consume_comma(s)
    return points, s


def parse_booster_code(s):
    ''' Return booster code and remainder string '''
    result = booster_prog.match(s)
    return result.groups()[0], s[result.span()[1]:]


def parse_booster_location(s):
    ''' Return booster code, point location, and remainder string '''
    b, s = parse_booster_code(s)
    p, s = parse_point(s)
    return b, p, s


def parse_obstacles(s):
    ''' Return list of obstacles (which are lists of points) and remainder string '''
    obstacles = []
    try:
        m, _ = parse_map(s)
        is_another_obstacle = bool(m)
    except AttributeError:
        is_another_obstacle = False
    while is_another_obstacle:
        o, s = parse_map(s)
        obstacles.append(o)
        is_another_obstacle, s = maybe_consume_semicolon(s)
    return obstacles, s


def parse_boosters(s):
    ''' Return list of (booster_code, location point) and remainder string '''
    boosters = []
    try:
        parse_booster_location(s)
        is_another_boosters = True
    except AttributeError:
        is_another_boosters = False
    while is_another_boosters:
        b, p, s = parse_booster_location(s)
        boosters.append((b, p))
        is_another_boosters, s = maybe_consume_semicolon(s)
    return boosters, s


def parse_task(s):
    ''' Return tuple of (map border, starting point, obstacles list, boosters list), and remainder '''
    # task ::= map # point # obstacles # boosters
    m, s = parse_map(s)
    s = consume_hash(s)
    p, s = parse_point(s)
    s = consume_hash(s)
    o, s = parse_obstacles(s)
    s = consume_hash(s)
    b, s = parse_boosters(s)
    return (m, p, o, b), s

def parse_action(s):
    ''' Return next action and remainder string '''
    s = re.sub('^\s+', '', s)
    if not s:
        raise AttributeError('out of string')
    c = s[0]
    if c in valid_acts:
        return c, s[1:]

    result = act_b_prog.match(s)
    if result is not None:
        x, y = result.groups()
        return ('B', (int(x), int(y))), s[result.span()[1]:]

    result = act_t_prog.match(s)
    if result is not None:
        x, y = result.groups()
        return ('T', (int(x), int(y))), s[result.span()[1]:]

    raise AttributeError('No action here')


def parse_actions(s):
    ''' Return a list of actions, and remainder string '''
    s = re.sub(r'\s', '', s)
    actions = []
    is_another_action = True
    while is_another_action:
        try:
            a, s = parse_action(s)
            actions.append(a)
        except AttributeError:
            break
    return actions, s


def parse_solution(s):
    ''' parse a solution file into lists of action lists, and remainder string '''
    s = re.sub(r'\s', '', s)
    solution = []
    try:
        a, _ = parse_actions(s)
        is_another_actions_list = bool(a)
    except AttributeError:
        is_another_actions_list = False
    while is_another_actions_list:
        a, s = parse_actions(s)
        solution.append(a)
        is_another_actions_list, s = maybe_consume_hash(s)
    return solution, s


def main(file='tests/test1.desc'):
    print(parse_booster_code(' B ABC'))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--file', default='tests/test1.desc')
    args = argparser.parse_args()
    main(file=args.file)
