from pathlib import Path

rucksacks = [x.strip() for x in Path("input.txt").open("r").readlines()]

letters = "abcdefghijklmnopqrstuvwxyz"
prio_map = {}
for i, letter in enumerate(letters):
    prio_map[letter] = i + 1
for i, letter in enumerate(letters.upper()):
    prio_map[letter] = i + len(letters) + 1

prio_sum = 0
for rucksack in rucksacks:
    l = int(len(rucksack) / 2)
    comp1, comp2 = (set(rucksack[:l]), set(rucksack[l:]))

    item = comp1.intersection(comp2).pop()
    prio = prio_map[item]
    prio_sum += prio

print(f"Part 1: {prio_sum}")

i = 1
prio_sum = 0
groups = [set(letters + letters.upper())]
for rucksack in rucksacks:
    groups[len(groups) - 1] = groups[len(groups) - 1].intersection(rucksack)
    if i % 3 == 0:
        item = groups[len(groups) - 1].pop()
        prio = prio_map[item]
        prio_sum += prio
        groups.append(set(letters + letters.upper()))

    i += 1

print(f"Part 2: {prio_sum}")
