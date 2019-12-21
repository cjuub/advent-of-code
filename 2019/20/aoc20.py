#!/usr/bin/env python3

from networkx import Graph, DiGraph
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


graph = DiGraph()

for level in range(30):
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
                    try:
                        inner = grid[y2][x2 + 2] == ' '
                    except:
                        inner = False

                    if inner:
                        target_level = level + 1
                    else:
                        target_level = level

                    portal = grid[y2][x2] + grid[y2][x2 + 1]
                    portal_coord = (x2 - 1, y2, target_level, inner)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
                elif grid[y2][x2 + 1] in letters and to_left:
                    inner = grid[y2][x2 - 1] == ' ' and (x2 - 1) != -1
                    if inner:
                        target_level = level + 1
                    else:
                        target_level = level

                    portal = grid[y2][x2] + grid[y2][x2 + 1]
                    portal_coord = (x2 + 2, y2, target_level, inner)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
                elif grid[y2 + 1][x2] in letters and above:
                    try:
                        inner = grid[y2 + 2][x2] == ' '
                    except:
                        inner = False

                    if inner:
                        target_level = level + 1
                    else:
                        target_level = level

                    portal = grid[y2][x2] + grid[y2 + 1][x2]
                    portal_coord = (x2, y2 - 1, target_level, inner)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
                elif grid[y2 + 1][x2] in letters and under:
                    inner = grid[y2 - 1][x2] == ' ' and (y2 - 1) != -1
                    if inner:
                        target_level = level + 1
                    else:
                        target_level = level

                    portal = grid[y2][x2] + grid[y2 + 1][x2]
                    portal_coord = (x2, y2 + 2, target_level, inner)
                    portals.setdefault(portal, [])
                    portals[portal].append(portal_coord)
                else:
                    continue

                # print('Portal: ' + str(level) + ' ' + portal + ' ' + str(portal_coord) + ' ' + str(inner))
            elif grid[y2][x2] == '.':
                if grid[y2 + 1][x2] == '.':
                    graph.add_edge((x2, y2, level), (x2, y2 + 1, level))
                if grid[y2][x2 + 1] == '.':
                    graph.add_edge((x2, y2, level), (x2 + 1, y2, level))
                if grid[y2][x2 - 1] == '.':
                    graph.add_edge((x2, y2, level), (x2 - 1, y2, level))
                if grid[y2 - 1][x2] == '.':
                    graph.add_edge((x2, y2, level), (x2, y2 - 1, level))

    for portal, coords in portals.items():
        if len(coords) == 1:
            continue

        # lol wtf clean this up pls
        coords[0] = list(coords[0])
        coords[1] = list(coords[1])
        if not coords[0][3]:
            tmp = coords[0]
            coords[0] = coords[1]
            coords[1] = tmp

        tmp = coords[0][2]
        coords[0][2] = coords[1][2]
        coords[1][2] = tmp
        coords[0] = tuple(coords[0])
        coords[1] = tuple(coords[1])

        if coords[0][2] == -1 and not coords[0][3]:
            continue

        if coords[1][2] == -1 and not coords[1][3]:
            continue

        graph.add_edge(coords[0][:-1], coords[1][:-1])
        graph.add_edge(coords[1][:-1], coords[0][:-1])

        # print('level ' + str(level) + ' ' + portal + ' ' + str(coords))
    # print()

start_pos = (53, 2, 0)
target_pos = (104, 63, 0)

print('Part 2: ' + str(shortest_path_length(graph, source=start_pos, target=target_pos)))
