import dataclasses
from pathlib import Path
from typing import Optional, Tuple

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

steps = []
for line in lines:
    state = True if line.split(" ")[0] == "on" else False
    line = line.split(" ")[1]

    rs = []
    for r in line.split(","):
        tmp = r.split("=")[1]
        cuboid_dim = range(max(int(tmp.split("..")[0]), -50), min(int(tmp.split("..")[1]) + 1, 51))
        rs.append(cuboid_dim)

    steps.append((state, rs))

cubes_on = set()
for state, cuboid in steps:
    for x in cuboid[0]:
        for y in cuboid[1]:
            for z in cuboid[2]:
                if state:
                    cubes_on.add((x, y, z))
                elif (x, y, z) in cubes_on:
                    cubes_on.remove((x, y, z))


print(f"Part 1: {len(cubes_on)}")


@dataclasses.dataclass(frozen=True)
class Cuboid:
    xr: range
    yr: range
    zr: range

    def overlap(self, other: 'Cuboid') -> Optional['Cuboid']:
        xr_overlap = range(max(self.xr[0], other.xr[0]), min(self.xr[-1], other.xr[-1]) + 1)
        yr_overlap = range(max(self.yr[0], other.yr[0]), min(self.yr[-1], other.yr[-1]) + 1)
        zr_overlap = range(max(self.zr[0], other.zr[0]), min(self.zr[-1], other.zr[-1]) + 1)

        if len(xr_overlap) == 0 or len(yr_overlap) == 0 or len(zr_overlap) == 0:
            return None

        return Cuboid(xr_overlap, yr_overlap, zr_overlap)

    def count(self) -> int:
        return len(self.xr) * len(self.yr) * len(self.zr)


steps = []
for line in lines:
    state = True if line.split(" ")[0] == "on" else False
    line = line.split(" ")[1]

    rs = []
    for r in line.split(","):
        tmp = r.split("=")[1]
        cuboid_dim = range(int(tmp.split("..")[0]), int(tmp.split("..")[1]) + 1)
        rs.append(cuboid_dim)

    steps.append((state, Cuboid(*rs)))


diffs = []
for state, cuboid in steps:
    new_diffs = []
    if state:
        new_diffs.append((cuboid, True))

    for diff, diff_state in diffs:
        overlap = diff.overlap(cuboid)
        if overlap is not None:
            if state and not diff_state:
                new_diffs.append((overlap, True))
            elif state and diff_state:
                new_diffs.append((overlap, False))
            elif not state and not diff_state:
                new_diffs.append((overlap, True))
            elif not state and diff_state:
                new_diffs.append((overlap, False))

    diffs.extend(new_diffs)

on_cnt = 0
for diff, state in diffs:
    on_cnt = on_cnt + diff.count() if state else on_cnt - diff.count()

print(f"Part 2: {on_cnt}")
