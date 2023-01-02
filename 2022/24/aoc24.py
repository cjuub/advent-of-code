from copy import deepcopy
from pathlib import Path

from networkx import DiGraph, shortest_path_length


def adjacents_to(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def step_blizzards(blizzards):
    stepped_blizzards = []
    for (bx, by), blizzard in blizzards:
        if blizzard == ">":
            new_pos = (bx + 1, by)
            if new_pos in walls:
                new_pos = (1, by)
        elif blizzard == "v":
            new_pos = (bx, by + 1)
            if new_pos in walls:
                new_pos = (bx, 1)
        elif blizzard == "<":
            new_pos = (bx - 1, by)
            if new_pos in walls:
                new_pos = (width - 2, by)
        elif blizzard == "^":
            new_pos = (bx, by - 1)
            if new_pos in walls:
                new_pos = (bx, height - 2)
        else:
            assert False

        stepped_blizzards.append((new_pos, blizzard))

    return tuple(stepped_blizzards)


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]
width = len(lines[0])
height = len(lines)

initial_blizzards = []
walls = []
for y in range(height):
    for x in range(width):
        if lines[y][x] in "<>^v":
            initial_blizzards.append(((x, y), lines[y][x]))
        if lines[y][x] == "#":
            walls.append((x, y))

start = (1, 0)
end = (width - 2, height - 1)
curr_blizzards = deepcopy(initial_blizzards)
tot = 0
for i in range(3):
    if i == 0 or i == 2:
        curr_pos = start
        curr_start = start
        curr_end = end
    else:
        curr_pos = end
        curr_start = end
        curr_end = start

    g = DiGraph()
    t = 0
    while True:
        curr_blizzard_poses = [(x, y) for (x, y), _ in curr_blizzards]

        new_blizzards = step_blizzards(curr_blizzards)
        new_blizzard_poses = [(x, y) for (x, y), _ in new_blizzards]

        for y in range(height):
            for x in range(width):
                if (x, y) in walls or (x, y) in curr_blizzard_poses:
                    continue
                if (x, y) not in new_blizzard_poses:
                    g.add_edge(((x, y), t), ((x, y), t + 1))
                for ax, ay in adjacents_to(x, y):
                    if (ax, ay) not in walls and (ax, ay) not in new_blizzard_poses and ax >= 0 and ay >= 0:
                        g.add_edge(((x, y), t), ((ax, ay), t + 1))

        curr_blizzards = deepcopy(new_blizzards)

        t += 1
        try:
            res = shortest_path_length(g, (curr_start, 0), (curr_end, t))
            tot += res
            if i == 0:
                print(f"Part 1: {res}")
            break
        except:
            pass

print(f"Part 2: {tot}")
