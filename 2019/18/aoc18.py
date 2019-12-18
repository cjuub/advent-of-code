#!/usr/bin/env python3
from collections import deque

with open('input.txt') as fp:
    lines = fp.readlines()

h = len(lines)
w = len(lines[0].strip())

grid = [[' ' for y in range(w)] for x in range(h)]

keys_input = 'abcdefghijklmnopqrstuvwxyz'
keys_test1 = 'abcdefg'
keys_test2 = 'abcdefghijklmnop'
keys_test3 = 'abcdefghi'
keys = keys_input
doors = keys.upper()

start_pos = [-1, -1]
for y in range(len(lines)):
    for x in range(len(lines[0].strip())):
        # if lines[y].strip()[x] not in doors + '.#':
        grid[y][x] = lines[y].strip()[x]

        if grid[y][x] == '@':
            start_pos = [x, y]

for y2 in range(h):
    for x2 in range(w):
        print(grid[y2][x2], end='')
    print()


class StepData:
    def __init__(self, x, y, gained_keys, steps, prev_step_data):
        self.x = x
        self.y = y
        self.gained_keys = gained_keys
        self.steps = steps
        self.prev_step_data = prev_step_data

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.gained_keys == other.gained_keys

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + str(self.gained_keys))


def visit(grid, queue, prev_step_data, x, y, target, visited):
    curr = grid[y][x]

    step_data = None
    if curr in doors:
        key = curr.lower()
        key_index = keys.find(key)

        if not target[key_index] or prev_step_data.gained_keys[key_index]:
            step_data = StepData(x, y, prev_step_data.gained_keys[:], prev_step_data.steps + 1, prev_step_data)
    elif curr in keys:
        key_index = keys.find(curr)
        new_gained_keys = prev_step_data.gained_keys[:]
        new_gained_keys[key_index] = True
        step_data = StepData(x, y, new_gained_keys, prev_step_data.steps + 1, prev_step_data)
    elif curr != '#':
        step_data = StepData(x, y, prev_step_data.gained_keys[:], prev_step_data.steps + 1, prev_step_data)

    if step_data and step_data not in visited:
        queue.append(step_data)

    if step_data:
        visited.add(step_data)


def bfs(start_x, start_y, target):
    visited = set()
    queue = deque([StepData(start_x, start_y, [False] * len(keys), 0, visited)])
    while queue:
        step_data = queue.popleft()
        if step_data.gained_keys == target:
            return step_data.steps

        visit(grid, queue, step_data, step_data.x - 1, step_data.y, target, visited)
        visit(grid, queue, step_data, step_data.x + 1, step_data.y, target, visited)
        visit(grid, queue, step_data, step_data.x, step_data.y - 1, target, visited)
        visit(grid, queue, step_data, step_data.x, step_data.y + 1, target, visited)


print('Part 1: ' + str(bfs(start_pos[0], start_pos[1], [True] * len(keys))))

grid[start_pos[1]][start_pos[0]] = '#'
grid[start_pos[1] - 1][start_pos[0]] = '#'
grid[start_pos[1] + 1][start_pos[0]] = '#'
grid[start_pos[1]][start_pos[0] - 1] = '#'
grid[start_pos[1]][start_pos[0] + 1] = '#'

grid[start_pos[1] - 1][start_pos[0] - 1] = '@'
grid[start_pos[1] + 1][start_pos[0] - 1] = '@'
grid[start_pos[1] - 1][start_pos[0] + 1] = '@'
grid[start_pos[1] + 1][start_pos[0] + 1] = '@'

keys_1 = 'lidgw'
keys_2 = 'equx'
keys_3 = 'pyhfrmovnsc'
keys_4 = 'bzkjat'
assert len(keys_1 + keys_2 + keys_3 + keys_4) == len(keys)

target_1 = [False] * len(keys)
for key in keys_1:
    target_1[keys.find(key)] = True

target_2 = [False] * len(keys)
for key in keys_2:
    target_2[keys.find(key)] = True

target_3 = [False] * len(keys)
for key in keys_3:
    target_3[keys.find(key)] = True

target_4 = [False] * len(keys)
for key in keys_4:
    target_4[keys.find(key)] = True

bfs_1 = bfs(start_pos[0] - 1, start_pos[1] - 1, target_1)
bfs_2 = bfs(start_pos[0] + 1, start_pos[1] - 1, target_2)
bfs_3 = bfs(start_pos[0] - 1, start_pos[1] + 1, target_3)
bfs_4 = bfs(start_pos[0] + 1, start_pos[1] + 1, target_4)

print('Part 2: ' + str(bfs_1 + bfs_2 + bfs_3 + bfs_4))
