from pathlib import Path
from typing import OrderedDict

lines = Path("input.txt").read_text().splitlines()

maps = OrderedDict()
current_map = None
seeds = [int(x) for x in lines[0].split(": ")[1].split(" ")]
for line in lines[2:]:
    if line == "":
        continue

    if line.endswith("map:"):
        current_map = line.split(" ")[0]
        maps[current_map] = []
    else:
        dst = int(line.split(" ")[0])
        src = int(line.split(" ")[1])
        size = int(line.split(" ")[2])
        maps[current_map].append((range(src, src+size), range(dst, dst+size)))

locations = []
for seed in seeds:
    i = seed
    for mapper, map in maps.items():
        for src, dst in map:
            if i in src:
                offset = i - src[0]
                i = dst[offset]
                break

    locations.append(i)

print(f"Part 1: {min(locations)}")

def range_intersect(r1, r2):
    return range(max(r1.start,r2.start), min(r1.stop,r2.stop)) or None

all_seeds = []
for i in range(0, len(seeds), 2):
    all_seeds.append(range(seeds[i], seeds[i] + seeds[i+1]))

reversed_maps = []
for mapper, map in reversed(maps.items()):
    reversed_maps.append(map)

def find_path(m, curr_map, curr):
    if curr_map == len(m):
        for r in all_seeds:
            if curr in r:
                return True
        return False

    is_mapped = False
    for dst, src in m[curr_map]:
        if curr in src:
            is_mapped = True
            offset = curr - src[0]
            res = find_path(m, curr_map + 1, dst[offset])
            if res:
                return res

    if not is_mapped:
        res = find_path(m, curr_map + 1, curr)
        if res:
            return res

    return False

lowest = -1
# this takes a while
for i in range(0, 100000000):
    lowest = i
    res = find_path(reversed_maps, 0, i)
    if res:
        break

print(f"Part 2: {lowest}")

