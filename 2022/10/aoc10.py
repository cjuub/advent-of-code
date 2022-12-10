from copy import deepcopy
from pathlib import Path

instructions = [x.strip() for x in Path("input.txt").open("r").readlines()]


def increase():
    global cycle, x
    cycle += 1
    if cycle in [20, 60, 100, 140, 180, 220]:
        signal_strengths.append(x * cycle )


x = 1
cycle = 0
signal_strengths = []
for instruction in instructions:
    s = instruction.split(" ")
    if len(s) == 2:
        increase()
        increase()
        x += int(s[1])
    else:
        increase()

print(f"Part 1: {sum(signal_strengths)}")


def update_sprite_row():
    global x, sprite_row
    sprite_row = ["."] * 40
    if x - 1 >= 0:
        sprite_row[x-1] = "#"
    if x >= 0:
        sprite_row[x] = "#"
    if x + 1 >= 0:
        sprite_row[x+1] = "#"


def increase2():
    global cycle, x, sprite_row, curr_row, screen
    index = cycle % 40
    if index == 0 and cycle != 0:
        screen.append(deepcopy(curr_row))
        curr_row = ["."] * 40
    curr_row[index] = sprite_row[index]
    cycle += 1


sprite_row = ["."] * 40
curr_row = ["."] * 40
screen = []
x = 1
cycle = 0
update_sprite_row()
for instruction in instructions:
    s = instruction.split(" ")
    if len(s) == 2:
        increase2()
        increase2()
        x += int(s[1])
        update_sprite_row()
    else:
        increase2()

screen.append(deepcopy(curr_row))

print("Part 2:")
for row in screen:
    for pixel in row:
        print(pixel, end="")
    print()
