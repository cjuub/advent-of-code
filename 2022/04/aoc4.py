from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

pairs = []
for line in lines:
    split = line.split(",")
    r1 = split[0].split("-")
    r2 = split[1].split("-")
    pairs.append((range(int(r1[0]), int(r1[1])+1), range(int(r2[0]), int(r2[1])+1)))


cnt = 0
cnt2 = 0
for r1, r2 in pairs:
    if set(r1).issubset(r2) or set(r2).issubset(r1):
        cnt += 1

    if len(set(r1).intersection(r2)) != 0:
        cnt2 += 1

print(f"Part 1: {cnt}")
print(f"Part 2: {cnt2}")
