from pathlib import Path

from networkx import Graph, shortest_path, NetworkXNoPath


def adjacents(x, y, z):
    return [(x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)]


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

cubes = []
for line in lines:
    cubes.append(tuple([int(x) for x in line.split(",")]))

connections = {}
for c1 in cubes:
    connections.setdefault(c1, [])
    for c2 in cubes:
        if c1 == c2:
            continue

        if c2 in adjacents(*c1):
            connections[c1].append(c2)

sides = 0
for cube in cubes:
    sides += 6
    sides -= len(connections[cube])

print(f"Part 1: {sides}")

max_x = 0
max_y = 0
max_z = 0
for cube in cubes:
    max_x = max(max_x, cube[0] + 1)
    max_y = max(max_y, cube[1] + 1)
    max_z = max(max_z, cube[2] + 1)

g = Graph()
for z in range(-2, max_z + 2):
    for y in range(-2, max_y + 2):
        for x in range(-2, max_x + 2):
            for adj in adjacents(x, y, z):
                g.add_node(adj)
            if (x, y, z) in cubes:
                continue

            for adj in adjacents(x, y, z):
                if adj not in cubes:
                    g.add_edge((x, y, z), adj)

air_pockets = set()
for cube in cubes:
    for adj in adjacents(*cube):
        if adj not in cubes:
            try:
                shortest_path(g, adj, (0, 0, 0))
            except NetworkXNoPath:
                air_pockets.add(adj)

for air_pocket in air_pockets:
    for adj in adjacents(*air_pocket):
        if adj in cubes:
            sides -= 1

print(f"Part 2: {sides}")
