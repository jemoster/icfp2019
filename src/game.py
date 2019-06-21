import json


def convert_to_json(text):
    return json.loads('[' + text.replace('(', '[').replace(')', ']') + ']')


def loader(path):
    with open(path) as f:
        text = f.read()
    boardmap, point, obstacles, boosters = text.split('#')
    boardmap = parse_boardmap(boardmap)
    point = parse_starting_point(point)
    obstacles = parse_obstacles(obstacles)
    boosters = parse_boosters(boosters)
    print(boardmap, point, obstacles, boosters)


def parse_boardmap(text):
    return convert_to_json(text)


def parse_starting_point(text):
    return convert_to_json(text)


def parse_obstacles(text):
    text = '[[' + text.replace('(', '[').replace(')', ']').replace(';', '],[') + ']]'
    return json.loads(text)


def parse_boosters(text):
    boosters = {
        'B': [],
        'F': [],
        'L': [],
        'X': [],
    }
    text = text.strip()
    for t in text.split(';'):
        btype = t[0]
        bpoint = list(map(int, t[2:-1].split(',')))
        boosters[btype].append(bpoint)
    return boosters
