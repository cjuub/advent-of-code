from pathlib import Path


def manhattan(x1, y1, x2, y2):
    dist = 0
    dist += abs(x1 - x2)
    dist += abs(y1 - y2)
    return dist


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

pairs = []
sensors = []
beacons = []
for line in lines:
    line = line[10:]
    s1 = line.split(": ")
    s2 = s1[0].split(", ")
    sx = int(s2[0][2:])
    sy = int(s2[1][2:])

    s2 = s1[1][21:].split(", ")
    bx = int(s2[0][2:])
    by = int(s2[1][2:])

    pairs.append(((sx, sy), (bx, by)))
    sensors.append((sx, sy))
    beacons.append((bx, by))

y = 2000000
not_beacons = {}
for (sx, sy), (bx, by) in pairs:
    dist = manhattan(sx, sy, bx, by)
    if sy not in range(sy - dist, sy + dist + 1):
        continue

    not_beacons.setdefault(y, set())
    for x in range(sx - dist, sx + dist + 1):
        d = manhattan(sx, sy, x, y)
        if d > dist:
            continue

        if (x, y) not in beacons:
            not_beacons[y].add((x, y))


print(f"Part 1: {len(not_beacons[y])}")

max_coordinate = 4000000
candidates = set()
for (sx, sy), (bx, by) in pairs:
    dist = manhattan(sx, sy, bx, by)
    y = sy
    for x in range(sx - dist - 1, sx + 1):
        if x in range(0, max_coordinate + 1) and y in range(0, max_coordinate + 1):
            candidates.add((x, y))
        y -= 1

    y = sy
    for x in range(sx - dist - 1, sx + 1):
        if x in range(0, max_coordinate + 1) and y in range(0, max_coordinate + 1):
            candidates.add((x, y))
        y += 1

    y = sy + dist + 1
    for x in range(sx, sx + dist + 1 + 1):
        if x in range(0, max_coordinate + 1) and y in range(0, max_coordinate + 1):
            candidates.add((x, y))
        y -= 1

    y = sy - dist - 1
    for x in range(sx, sx + dist + 1 + 1):
        if x in range(0, max_coordinate + 1) and y in range(0, max_coordinate + 1):
            candidates.add((x, y))
        y += 1

for x, y in candidates:
    in_range = False
    for (sx, sy), (bx, by) in pairs:
        d1 = manhattan(sx, sy, bx, by)
        d2 = manhattan(sx, sy, x, y)

        if d2 <= d1:
            in_range = True
            break

    if not in_range:
        print(f"Part 2: {x * 4000000 + y}")
        break
