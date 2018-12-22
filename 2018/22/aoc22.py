#!/usr/bin/env python3

from networkx import Graph, dijkstra_path_length

target = None
depth = -1
with open('input.txt') as fp:
    for line in fp:
        if 'depth' in line:
            depth = int(line.split(' ')[1].strip())

        if 'target' in line:
            line = line.split(' ')[1].strip()
            target = (int(line.split(',')[0]), int(line.split(',')[1]))

extra_space = 100
max_x = target[0] + 1 + extra_space
max_y = target[1] + 1 + extra_space
erosion_map = [[-1 for y in range(max_y)] for x in range(max_x)]
map = [[-1 for y in range(max_y)] for x in range(max_x)]

risk_level = 0
for y in range(max_y):
    for x in range(max_x):
        geo_index = -1
        if (x == 0 and y == 0) or (x == target[0] and y == target[1]):
            geo_index = 0
            erosion = (geo_index + depth) % 20183
        elif y == 0:
            geo_index = x * 16807
            erosion = (geo_index + depth) % 20183
        elif x == 0:
            geo_index = y * 48271
            erosion = (geo_index + depth) % 20183
        else:
            geo_index = erosion_map[x-1][y] * erosion_map[x][y-1]
            erosion = (geo_index + depth) % 20183

        erosion_map[x][y] = erosion

        if (erosion % 3) == 0:
            map[x][y] = '.'
        elif erosion % 3 == 1:
            map[x][y] = '='
        elif erosion % 3 == 2:
            map[x][y] = '|'
        else:
            print('err')

for y in range(target[1] + 1):
    for x in range(target[0] + 1):
        erosion = erosion_map[x][y]

        if erosion % 3 == 1:
            risk_level += 1
        elif erosion % 3 == 2:
            risk_level += 2
        print(map[x][y], end='')
    print()

print(risk_level)


def adjacents_to(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


graph = Graph()
for y in range(max_y):
    for x in range(max_x):
        curr = map[x][y]
        choices = []
        if curr == '.':
            choices = ['t', 'c']
        elif curr == '=':
            choices = ['c', 'n']
        elif curr == '|':
            choices = ['t', 'n']

        for t1 in choices:
            for t2 in choices:
                if t1 != t2:
                    graph.add_edge((x, y, t1), (x, y, t2), weight=7)

for y in range(max_y):
    for x in range(max_x):
        for adj in adjacents_to(x, y):
            if (adj[0] < 0 or adj[0] >= max_x) or (adj[1] < 0 or adj[1] >= max_y):
                continue

            curr = map[x][y]
            curr_choices = []
            if curr == '.':
                curr_choices = {'t', 'c'}
            elif curr == '=':
                curr_choices = {'c', 'n'}
            elif curr == '|':
                curr_choices = {'t', 'n'}

            next = map[adj[0]][adj[1]]
            next_choices = []
            if next == '.':
                next_choices = {'t', 'c'}
            elif next == '=':
                next_choices = {'c', 'n'}
            elif next == '|':
                next_choices = {'t', 'n'}

            tools = curr_choices.intersection(next_choices)

            for tool in tools:
                graph.add_edge((x, y, tool), (adj[0], adj[1], tool), weight=1)

len = dijkstra_path_length(graph, (0, 0, 't'), (target[0], target[1], 't'))
print(len)
