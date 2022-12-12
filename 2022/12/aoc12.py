from pathlib import Path

from networkx import DiGraph, shortest_path_length, NetworkXNoPath


def adjacents(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def adjacent_letters(x, y):
    adj_letters = []
    for ax, ay in adjacents(x, y):
        if ax < 0 or ay < 0 or ax == len(lines[0]) or ay == len(lines):
            continue

        adj_letters.append((lines[ay][ax], ax, ay))
    return adj_letters


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]


start = ("S", -1, -1)
goal = ("E", -1, -1)
graph = DiGraph()
for y, line in enumerate(lines):
    for x, letter in enumerate(line):
        if letter == "S":
            start = ("a", x, y)
            letter = "a"
        if letter == "E":
            goal = ("z", x, y)
            letter = "z"

        for adj_letter, ax, ay in adjacent_letters(x, y):
            if ord(adj_letter) <= ord(letter) + 1:
                graph.add_edge((letter, x, y), (adj_letter, ax, ay))
            if ord(letter) <= ord(adj_letter) + 1:
                graph.add_edge((adj_letter, ax, ay), (letter, x, y))

print(shortest_path_length(graph, start, goal))

shortest = 9999999999999
for y, line in enumerate(lines):
    for x, letter in enumerate(line):
        if letter == "a" or letter == "S":
            try:
                shortest = min(shortest_path_length(graph, ("a", x, y), goal), shortest)
            except NetworkXNoPath:
                pass

print(shortest)
