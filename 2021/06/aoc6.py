from pathlib import Path

with Path("input.txt").open() as fp:
    lines = fp.readlines()

fish = [int(x) for x in lines[0].split(',')]

for t in range(80):
    new_fish = []
    for i, f in enumerate(fish):
        if f == 0:
            fish[i] = 6
            new_fish.append(8)
        else:
            fish[i] -= 1
    fish.extend(new_fish)

print(f"Part 1: {len(fish)}")

fish = [int(x) for x in lines[0].split(',')]
fish_map = {}
for f in fish:
    if f not in fish_map.keys():
        fish_map[f] = 1
    else:
        fish_map[f] += 1

for t in range(256):
    new_fish_map = {}
    for f, c in fish_map.items():
        if f == 0:
            new_fish_map[6] = fish_map[0] if 6 not in new_fish_map.keys() else new_fish_map[6] + fish_map[0]
            new_fish_map[8] = fish_map[0] if 8 not in new_fish_map.keys() else new_fish_map[8] + fish_map[0]
        else:
            new_fish_map[f - 1] = fish_map[f] if f - 1 not in new_fish_map.keys() else new_fish_map[f - 1] + fish_map[f]

    fish_map = new_fish_map

tot = 0
for f, c in fish_map.items():
    tot += c

print(f"Part 2: {tot}")
