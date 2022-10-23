from pathlib import Path
from typing import Tuple, List

from networkx import DiGraph, shortest_path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

scanners = {}
scanner = 0
scanners[scanner] = []
for line in lines:
    if not line:
        scanner += 1
        scanners[scanner] = []
        continue
    if line.startswith("---"):
        continue

    scan = tuple(int(x) for x in line.split(","))
    scanners[scanner].append(scan)


def variations(xyz: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    res = []
    for variation in [
        (xyz[0], xyz[1], xyz[2]),
        (xyz[0], xyz[2], xyz[1]),
        (xyz[0], -xyz[1], -xyz[2]),
        (xyz[0], -xyz[2], xyz[1]),

        (-xyz[0], xyz[1], -xyz[2]),
        (-xyz[0], -xyz[2], -xyz[1]),
        (-xyz[0], -xyz[1], xyz[2]),
        (-xyz[0], xyz[2], xyz[1]),

        (xyz[1], xyz[0], -xyz[2]),
        (xyz[1], -xyz[2], -xyz[0]),
        (xyz[1], -xyz[0], xyz[2]),
        (xyz[1], xyz[2], xyz[0]),

        (-xyz[1], xyz[0], xyz[2]),
        (-xyz[1], xyz[2], -xyz[0]),
        (-xyz[1], -xyz[0], -xyz[2]),
        (-xyz[1], -xyz[2], xyz[0]),

        (xyz[2], xyz[0], xyz[1]),
        (xyz[2], xyz[1], -xyz[0]),
        (xyz[2], -xyz[0], -xyz[1]),
        (xyz[2], -xyz[1], xyz[0]),

        (-xyz[2], xyz[0], -xyz[1]),
        (-xyz[2], -xyz[1], -xyz[0]),
        (-xyz[2], -xyz[0], xyz[1]),
        (-xyz[2], xyz[1], xyz[0]),
    ]:
        res.append(variation)

    return res


def distance(x1, y1, z1, x2, y2, z2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    dist += abs(z1 - z2)
    return dist


def find_common_beacons(scanner1, scanner2) -> List[Tuple]:
    res = []
    for i in range(24):
        cnts = {}
        for beacon1 in scanners[scanner1]:
            for beacon2 in scanners[scanner2]:
                beacon1_var = variations(beacon1)[i]
                dist_diff = (
                    beacon2[0] - beacon1_var[0],
                    beacon2[1] - beacon1_var[1],
                    beacon2[2] - beacon1_var[2],
                )
                if dist_diff not in cnts:
                    cnts[dist_diff] = []
                cnts[dist_diff].append((beacon1, beacon2))
        for dist_diff, r in cnts.items():
            if len(r) >= 12:
                res.append((dist_diff, i))

    return res


offsets = {}
graph = DiGraph()
for scanner in scanners:
    offsets[scanner] = {}
    for other_scanner in scanners:
        if scanner == other_scanner:
            continue

        common_beacons = find_common_beacons(scanner, other_scanner)
        if common_beacons:
            graph.add_edge(scanner, other_scanner)
            for offset, translation in common_beacons:
                offsets[scanner][other_scanner] = (offset, translation)
                break

paths = {}
for scanner in scanners:
    if scanner == 0:
        continue

    paths[scanner] = (shortest_path(graph, scanner, 0))

beacons_seen_from_0 = set()
for scanner in scanners:
    if scanner == 0:
        beacons_seen_from_0.update(scanners[scanner])
    else:
        path_to_0 = paths[scanner]
        for beacon in scanners[scanner]:
            curr = scanner
            seen_from_curr = beacon[:]
            for next in path_to_0[1:]:
                offset, translation = offsets[curr][next]

                new = (
                    variations(seen_from_curr)[translation][0] + offset[0],
                    variations(seen_from_curr)[translation][1] + offset[1],
                    variations(seen_from_curr)[translation][2] + offset[2],
                )

                seen_from_curr = new[:]
                curr = next

            beacons_seen_from_0.add(seen_from_curr)

print(f"Part 1: {len(beacons_seen_from_0)}")


def distance(x1, y1, z1, x2, y2, z2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    dist += abs(z1 - z2)
    return dist


normalized_scanners = {}
for scanner in scanners:
    if scanner == 0:
        continue
    scanner_pos = (0, 0, 0)
    path_to_0 = paths[scanner][1:]
    curr = scanner
    for next in path_to_0:
        offset, trans = offsets[curr][next]
        scanner_pos = (
            variations(scanner_pos)[trans][0] + offset[0],
            variations(scanner_pos)[trans][1] + offset[1],
            variations(scanner_pos)[trans][2] + offset[2],
        )
        curr = next
    normalized_scanners[scanner] = scanner_pos


largest = 0
for scanner, dist in normalized_scanners.items():
    for other_scanner, other_dist in normalized_scanners.items():
        if scanner == other_scanner:
            continue
        largest = max(largest, distance(*dist, *other_dist))

print(f"Part 2: {largest}")
