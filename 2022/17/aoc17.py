import dataclasses
from pathlib import Path
from typing import Tuple, List


def print_chamber():
    chamber = [["." for x in range(chamber_width)] for y in range(chamber_height)]
    for rock in rocks:
        for x, y in rock.points:
            chamber[y][x] = "#"
    for y in range(len(chamber)):
        for x in range(len(chamber[0])):
            print(chamber[len(chamber) - y - 1][x], end="")
        print()
    print()


def extend_chamber(rock_height):
    global chamber_height
    chamber_height += rock_height + 3


def shrink_chamber():
    global chamber_height
    lines_to_remove = 0
    for y in range(chamber_height - 1, -1, -1):
        for rock in rocks:
            for _, ry in rock.points:
                if ry == y:
                    if lines_to_remove > 0:
                        chamber_height -= lines_to_remove
                    return
        lines_to_remove += 1


@dataclasses.dataclass
class Rock:
    points: List[Tuple[int, int]]
    w: int
    h: int

    def __init__(self, rock_template_index):
        rock = rock_templates[rock_template_index]
        self.points = []
        self.w = len(rock[0])
        self.h = len(rock)
        extend_chamber(self.h)
        for y in range(chamber_height - self.h, chamber_height):
            for x in range(2, len(rock[0]) + 2):
                rtx = x - 2
                rty = self.h - (y - chamber_height + self.h) - 1
                if rock[rty][rtx] == "#":
                    self.points.append((x, y))


def add_rock(rock_template_index):
    rock = Rock(rock_template_index)
    rocks.append(rock)


def move_rock(air_index):
    air_direction = air[air_index]
    rock = rocks[-1]
    after_air_points = []
    moved_by_air = True
    if air_direction == "<":
        for x, y in rock.points:
            if x - 1 < 0:
                moved_by_air = False
                break
            after_air_points.append((x - 1, y))
    elif air_direction == ">":
        for x, y in rock.points:
            if x + 1 == chamber_width:
                moved_by_air = False
                break
            after_air_points.append((x + 1, y))

    if moved_by_air:
        for other_rock in rocks[:-1]:
            for after_air_point in after_air_points:
                if after_air_point in other_rock.points:
                    moved_by_air = False
                    break
            if not moved_by_air:
                break

    if moved_by_air:
        rock.points = after_air_points

    new_points = []
    for x, y in rock.points:
        if y - 1 < 0:
            return False
        new_points.append((x, y - 1))

    moved_down = True
    for other_rock in rocks[:-1]:
        for new_point in new_points:
            if new_point in other_rock.points:
                moved_down = False
        if not moved_down:
            break

    if moved_down:
        rock.points = new_points
        shrink_chamber()

    return moved_down


air = [x.strip() for x in Path("input.txt").open("r").readlines()][0]
rock_templates = [
    [
        "####",
    ],
    [
        ".#.",
        "###",
        ".#.",
    ],
    [
        "..#",
        "..#",
        "###",
    ],
    [
        "#",
        "#",
        "#",
        "#",
    ],
    [
        "##",
        "##",
    ],
]

chamber_height = 0
chamber_width = 7
rocks = []
rock_template_i = 0
air_i = 0
for i in range(2022):
    add_rock(rock_template_i % len(rock_templates))
    rock_template_i += 1
    while move_rock(air_i % len(air)):
        # print_chamber()
        air_i += 1
    air_i += 1
    # print_chamber()

print(f"Part 1: {chamber_height}")


chamber_height = 0
chamber_width = 7
rocks = []
rock_template_i = 0
air_i = 0
cycle_len = 0
cycles_found = 0
cycle_height_diff = {}
prev_chamber_height = 0
cycle_ended = False

# Change to run cycle finder
# while True:
while False:
    add_rock(rock_template_i % len(rock_templates))
    rock_template_i += 1
    while move_rock(air_i % len(air)):
        if rock_template_i % len(rock_templates) == 0 and air_i % len(air) == 0:
            cycle_ended = True
        air_i += 1
        # if rock_template_i % len(rock_templates) == 0 and air_i % len(air) == 0:
        #     cycle_ended = True
    # if rock_template_i % len(rock_templates) == 0 and air_i % len(air) == 0:
    #     cycle_ended = True
    # if rock_template_i % len(rock_templates) == 0 and air_i % len(air) == 0:
    #     cycle_ended = True
    air_i += 1
    # if rock_template_i % len(rock_templates) == 0 and air_i % len(air) == 0:
    #     cycle_ended = True
    cycle_len += 1

    if cycle_len == 1445:
        print("END CYCLE HEIGHT")
        print(chamber_height - prev_chamber_height)

    if cycle_ended:
        print(chamber_height - prev_chamber_height)
        prev_chamber_height = chamber_height
        print(cycle_len)
        print()
        cycle_len = 0
        cycle_ended = False

tot_dropped = 1000000000000

# example
# first_cycle_dropped = 15
# cycle_height = 26 + 27
# dropped_per_cycle = 35
# first_cycle_height = 25
# last_cycle_height = 0

# input
first_cycle_dropped = 1715
cycle_height = 2702
dropped_per_cycle = 1720
first_cycle_height = 2685
tot_dropped_by_cycles = tot_dropped - first_cycle_dropped
last_cycle_height = 2303

nbr_full_cycles = int((tot_dropped_by_cycles) / dropped_per_cycle)

# input remaining_drops as "END CYCLE HEIGHT" condition
# remaining_drops = tot_dropped - nbr_full_cycles * dropped_per_cycle - first_cycle_dropped
# print(remaining_drops)

print(f"Part 2: {nbr_full_cycles * cycle_height + first_cycle_height + last_cycle_height}")
