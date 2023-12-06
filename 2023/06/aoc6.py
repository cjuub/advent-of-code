from pathlib import Path
import sys

lines = Path("input.txt").read_text().splitlines()

line = " ".join(lines[0].split())
times = [int(x) for x in line.split(": ")[1].split(" ")]
line = " ".join(lines[1].split())
dists = [int(x) for x in line.split(": ")[1].split(" ")]

def find_solutions(curr_t, curr_d, curr_v, record_d, s, released):
    if curr_t == 0:
        if curr_d > record_d:
            s.append(curr_d)
        return

    if not released:
        find_solutions(curr_t - 1, curr_d, curr_v + 1, record_d, s, False)
    find_solutions(curr_t - 1, curr_d + curr_v, curr_v, record_d, s, True)


ans = 1
for race in range(len(times)):
    solutions = []
    find_solutions(times[race], 0, 0, dists[race], solutions, False)
    ans *= len(solutions)

print(f"Part 1: {ans}")

sys.setrecursionlimit(100000000)

def find_solutions2(curr_t, curr_d, curr_v, record_d):
    if curr_t == 0:
        if curr_d > record_d:
            return True
        return False

    return find_solutions2(curr_t - 1, curr_d + curr_v, curr_v, record_d)

time = int("".join([str(x) for x in times]))
dist = int("".join([str(x) for x in dists]))

lowest_hold_time = 0
lower = 0
higher = time
curr = int(time / 2)
while True:
    if find_solutions2(time - curr, 0, curr, dist):
        higher = min(curr, higher)
        curr = lower + int((higher - lower) / 2)
    else:
        lower = max(curr, lower)
        curr = higher - int((higher - lower) / 2)

    if lower == higher - 1:
        lowest_hold_time = higher
        break

highest_hold_time = 0
lower = 0
higher = time
curr = int(time / 2)
while True:
    if find_solutions2(time - curr, 0, curr, dist):
        lower = max(curr, lower)
        curr = higher - int((higher - lower) / 2)
    else:
        higher = min(curr, higher)
        curr = lower + int((higher - lower) / 2)

    if lower == higher - 1:
        highest_hold_time = lower
        break

print(f"Part 2: {highest_hold_time - lowest_hold_time + 1}")
