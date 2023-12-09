import sys
from math import lcm
from pathlib import Path


lines = Path("input.txt").read_text().splitlines()

turns = lines[0]
map = {}
for line in lines[2:]:
    key = line.split(" = ")[0]
    val_str = line.split(" = ")[1]
    val = tuple(val_str[1:-1].split(", "))
    map[key] = val

def traverse(curr_pos, turn_index, path, goal):
    path.append(curr_pos)

    if curr_pos == goal:
        return len(path) - 1

    turn = turns[turn_index]
    right = turn == "R"

    return traverse(map[curr_pos][int(right)], (turn_index + 1) % len(turns), path, goal)

sys.setrecursionlimit(1000000)
print(f'Part 1: {traverse("AAA", 0, [], "ZZZ")}')


def find_loop(start_pos):
    visited = set()
    curr_pos = start_pos
    turn_index = 0
    turn = int(turns[turn_index] == "R")
    loop = []
    steps = 0
    loop_start = 0
    while True:
        if (curr_pos, turn_index) in visited:
            loop_start = loop.index((curr_pos, turn_index))
            loop = loop[loop_start:]
            break

        visited.add((curr_pos, turn_index))
        loop.append((curr_pos, turn_index))

        curr_pos = map[curr_pos][turn]

        steps += 1
        turn_index = steps % len(turns)
        turn = int(turns[turn_index] == "R")

    dist_to_loop = loop_start
    loop_cycle_len = len(loop)
    return dist_to_loop, loop, loop_cycle_len


cycles = []
for pos in map:
    if pos.endswith("A"):
        cycles.append(find_loop(pos))
cycles.sort(key = lambda x: x[2])

i = 0
dist_to_loop, loop, loop_len = cycles[i]
tot_steps = dist_to_loop
curr_cycle_step = 1
while True:
    if i == len(cycles) - 1:
        break
    dist_to_loop1, loop1, loop1_len = cycles[i]
    dist_to_loop2, loop2, loop2_len = cycles[i+1]

    loop1_index = (tot_steps - dist_to_loop1) % len(loop1)
    loop2_index = (tot_steps - dist_to_loop2) % len(loop2)

    if loop1[loop1_index][0].endswith("Z") and loop2[loop2_index][0].endswith("Z"):
        curr_cycle_step = lcm(loop1_len, curr_cycle_step)
        i += 1
    else:
        tot_steps += curr_cycle_step

print(f"Part 2: {tot_steps}")

