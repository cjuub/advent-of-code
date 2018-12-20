#!/usr/bin/env python3

import sys

from networkx import Graph
from networkx.algorithms import shortest_path_length

sys.setrecursionlimit(100000)


def parse(regex, x, y, depth, last_pos_stack, graph):
    if len(regex) == 0:
        return

    curr = regex[0]
    if curr == 'N':
        graph.add_edge((x, y), (x, y - 1))
        y -= 1
    elif curr == 'W':
        graph.add_edge((x, y), (x - 1, y))
        x -= 1
    elif curr == 'E':
        graph.add_edge((x, y), (x + 1, y))
        x += 1
    elif curr == 'S':
        graph.add_edge((x, y), (x, y + 1))
        y += 1

    elif curr == '(':
        depth += 1
        last_pos_stack.insert(0, (x, y))
    elif curr == ')':
        depth -= 1
        last_pos_stack = last_pos_stack[1:]

    elif curr == '|':
        x = last_pos_stack[0][0]
        y = last_pos_stack[0][1]

    parse(regex[1:], x, y, depth, last_pos_stack, graph)


regex = ''
with open('input.txt') as fp:
    for line in fp:
        regex += line[1:-1]

graph = Graph()
parse(regex, 0, 0, 0, [(0, 0)], graph)

path_lengths = shortest_path_length(graph, source=(0, 0), target=None)
print('part 1: ' + str(max(path_lengths.values())))

sum = 0
for len in path_lengths.values():
    if len >= 1000:
        sum += 1

print('part 2: ' + str(sum))
