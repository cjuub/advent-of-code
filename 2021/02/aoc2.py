from pathlib import Path


with Path("input.txt").open() as fp:
    lines = fp.readlines()

hor = 0
dep = 0
for line in lines:
    if line.startswith("forward"):
        hor += int(line.split(" ")[1])
    if line.startswith("down"):
        dep += int(line.split(" ")[1])
    elif line.startswith("up"):
        dep -= int(line.split(" ")[1])

print(f"Part 1: {hor * dep}")


hor = 0
dep = 0
aim = 0
for line in lines:
    if line.startswith("forward"):
        hor += int(line.split(" ")[1])
        dep += aim * int(line.split(" ")[1])
    if line.startswith("down"):
        aim += int(line.split(" ")[1])
    elif line.startswith("up"):
        aim -= int(line.split(" ")[1])

print(f"Part 2: {hor * dep}")
