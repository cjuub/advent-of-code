from pathlib import Path

positions = [int(x) for x in Path("input.txt").open().readlines()[0].split(',')]

min_cost = 999999999
for pos in range(min(positions), max(positions) + 1):
    cost = 0
    for p in positions:
        cost += abs(pos - p)

    min_cost = min(cost, min_cost)

print(f"Part 1: {min_cost}")

min_cost = 999999999
for pos in range(min(positions), max(positions) + 1):
    cost = 0
    for p in positions:
        cost += sum([x for x in range(abs(pos - p) + 1)])

    min_cost = min(cost, min_cost)

print(f"Part 2: {min_cost}")
