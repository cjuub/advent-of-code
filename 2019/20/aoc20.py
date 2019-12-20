#!/usr/bin/env python3

from networkx import Graph
from networkx.algorithms import shortest_path_length

with open('input.txt') as fp:
    lines = fp.readlines()


h = len(lines)
w = len(lines[0]) - 1
grid = [[' ' for y in range(w)] for x in range(h)]

graph = Graph()


for y2 in range(h):
    for x2 in range(w):
        grid[y2][x2] = lines[y2][x2]
        print(grid[y2][x2], end='')
    print()


letters = 'abcdefghijklmnopqrstuvwxyz'.upper()

portals = {}

for y2 in range(h - 1):
    for x2 in range(w - 1):
        if grid[y2][x2] in letters:
            to_right = x2 + 2 == w or grid[y2][x2 + 2] == ' '
            above = y2 + 2 == h or grid[y2 + 2][x2] == ' '
            if not to_right:
                to_left = grid[y2][x2 + 2] == '.'
            if not above:
                under = grid[y2 + 2][x2] == '.'

            if grid[y2][x2 + 1] in letters and to_right:
                    portal = grid[y2][x2] + grid[y2][x2 + 1]
                    portal_coord = (x2 - 1, y2)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
            elif grid[y2][x2 + 1] in letters and to_left:
                    portal = grid[y2][x2] + grid[y2][x2 + 1]
                    portal_coord = (x2 + 2, y2)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
            elif grid[y2 + 1][x2] in letters and above:
                    portal = grid[y2][x2] + grid[y2 + 1][x2]
                    portal_coord = (x2, y2 - 1)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
            elif grid[y2 + 1][x2] in letters and under:
                    portal = grid[y2][x2] + grid[y2 + 1][x2]
                    portal_coord = (x2, y2 + 2)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
            else:
                continue
        elif grid[y2][x2] == '.':
            if grid[y2 + 1][x2] == '.':
                graph.add_edge((x2, y2), (x2, y2 + 1))
            if grid[y2][x2 + 1] == '.':
                graph.add_edge((x2, y2), (x2 + 1, y2))
            if grid[y2][x2 - 1] == '.':
                graph.add_edge((x2, y2), (x2 - 1, y2))
            if grid[y2 - 1][x2] == '.':
                graph.add_edge((x2, y2), (x2, y2 - 1))

start_pos = portals['AA'][0]
target_pos = portals['ZZ'][0]

for portal, coords in portals.items():
    # print(portal + ' ' + str(coords))
    if len(coords) == 1:
        continue

    graph.add_edge(coords[0], coords[1])

print('Part 1: ' + str(shortest_path_length(graph, source=start_pos, target=target_pos)))
