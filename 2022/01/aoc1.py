from pathlib import Path

lines = Path("input.txt").open("r").readlines()

elves = []
i = 0
for line in lines:
    if not line.strip():
        i += 1
        continue

    if len(elves) < i + 1:
        elves.append([])
    elves[i].append(int(line.strip()))

cal_sums = []
for elf in elves:
    cal_sums.append(sum(elf))

cal_sums.sort(reverse=True)

print(f"Part 1: {cal_sums[0]}")
print(f"Part 2: {cal_sums[0] + cal_sums[1] + cal_sums[2]}")
