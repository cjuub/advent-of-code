import dataclasses
import math
from collections import deque
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Tuple


@dataclasses.dataclass
class Blueprint:
    ore_bot_costs: Tuple[int, int, int]
    clay_bot_costs: Tuple[int, int, int]
    obsidian_bot_costs: Tuple[int, int, int]
    geode_bot_costs: Tuple[int, int, int]


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

blueprints = []
for line in lines:
    s = line.split(". ")
    ore_robot_ore = int(s[0].split(" ")[-2])
    clay_robot_ore = int(s[1].split(" ")[-2])
    obsidian_robot_ore = (int(s[2].split(" ")[-5]))
    obsidian_robot_clay = (int(s[2].split(" ")[-2]))
    geode_robot_ore = (int(s[3].split(" ")[-5]))
    geode_robot_obsidian = (int(s[3].split(" ")[-2]))

    blueprint = Blueprint(
        (ore_robot_ore, 0, 0),
        (clay_robot_ore, 0, 0),
        (obsidian_robot_ore, obsidian_robot_clay, 0),
        (geode_robot_ore, 0, geode_robot_obsidian)
    )

    blueprints.append(blueprint)


def job(index, blueprint):
    global best_geodes
    q = deque()
    visited = set()
    root = (0, 1, 0, 0, 0, 0, 0, 0, 0)
    visited.add(root)
    q.append(root)
    old_time = 0
    best_geode = 0
    nbr_best_found_in_time = []
    nbr_best_found = 0
    while len(q) > 0:
        time, ore_bots, clay_bots, obsidian_bots, geode_bots, ore, clay, obsidian, geode = q.popleft()

        if time > 24:
            break

        if time != old_time:
            nbr_best_found_in_time.append(nbr_best_found)
            old_time = time
            nbr_best_found = 0

        if geode > best_geode:
            best_geode = geode
            nbr_best_found += 1

        if nbr_best_found_in_time and geode_bots < nbr_best_found_in_time[-1]:
            continue

        if time == 18 and ore < blueprint.clay_bot_costs[0] and clay_bots == 0:
            continue
        if time == 19 and clay_bots == 0:
            continue
        if time == 20 and (ore < blueprint.obsidian_bot_costs[0] or clay < blueprint.obsidian_bot_costs[1]) and obsidian_bots == 0:
            continue
        if time == 21 and obsidian_bots == 0:
            continue
        if time == 22 and (ore < blueprint.geode_bot_costs[0] or obsidian < blueprint.geode_bot_costs[2]) and geode_bots == 0:
            continue
        if time == 23 and geode_bots == 0:
            continue

        if ore >= blueprint.ore_bot_costs[0]:
            w = (time + 1, ore_bots + 1, clay_bots, obsidian_bots, geode_bots, ore - blueprint.ore_bot_costs[0] + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.clay_bot_costs[0]:
            w = (time + 1, ore_bots, clay_bots + 1, obsidian_bots, geode_bots, ore - blueprint.clay_bot_costs[0] + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.obsidian_bot_costs[0] and clay >= blueprint.obsidian_bot_costs[1]:
            w = (time + 1, ore_bots, clay_bots, obsidian_bots + 1, geode_bots, ore - blueprint.obsidian_bot_costs[0] + ore_bots, clay - blueprint.obsidian_bot_costs[1] + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.geode_bot_costs[0] and obsidian >= blueprint.geode_bot_costs[2]:
            w = (time + 1, ore_bots, clay_bots, obsidian_bots, geode_bots + 1, ore - blueprint.geode_bot_costs[0] + ore_bots, clay + clay_bots, obsidian - blueprint.geode_bot_costs[2] + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        w = (time + 1, ore_bots, clay_bots, obsidian_bots, geode_bots, ore + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
        if w not in visited:
            visited.add(w)
            q.append(w)

    quality_levels[index] = (best_geode * (index + 1))


quality_levels = [0] * len(blueprints)
pool = ThreadPool(len(blueprints))
job_args = []
for i, blueprint in enumerate(blueprints):
    job_args.append((i, blueprint))

pool.starmap(job, job_args)

pool.close()
pool.join()
print(f"Part 1: {sum(quality_levels)}")


def job2(index, blueprint):
    global best_geodes
    q = deque()
    visited = set()
    root = (0, 1, 0, 0, 0, 0, 0, 0, 0)
    visited.add(root)
    q.append(root)
    old_time = 0
    best_geode = 0
    time_diff = 8
    nbr_best_found_in_time = []
    nbr_best_found = 0
    while len(q) > 0:
        time, ore_bots, clay_bots, obsidian_bots, geode_bots, ore, clay, obsidian, geode = q.popleft()

        if time > 24 + time_diff:
            break

        if time != old_time:
            old_time = time
            nbr_best_found_in_time.append(nbr_best_found)
            nbr_best_found = 0

        if geode > best_geode:
            best_geode = geode
            nbr_best_found += 1

        if nbr_best_found_in_time and geode_bots < nbr_best_found_in_time[-1]:
            continue

        if time > 18 + time_diff and ore < blueprint.clay_bot_costs[0] and clay_bots == 0:
            continue
        if time > 19 + time_diff and clay_bots == 0:
            continue
        if time > 20 + time_diff and (ore < blueprint.obsidian_bot_costs[0] or clay < blueprint.obsidian_bot_costs[1]) and obsidian_bots == 0:
            continue
        if time > 21 + time_diff and obsidian_bots == 0:
            continue
        if time > 22 + time_diff and (ore < blueprint.geode_bot_costs[0] or obsidian < blueprint.geode_bot_costs[2]) and geode_bots == 0:
            continue
        if time > 23 + time_diff and geode_bots == 0:
            continue

        if ore >= blueprint.ore_bot_costs[0]:
            w = (time + 1, ore_bots + 1, clay_bots, obsidian_bots, geode_bots, ore - blueprint.ore_bot_costs[0] + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.clay_bot_costs[0]:
            w = (time + 1, ore_bots, clay_bots + 1, obsidian_bots, geode_bots, ore - blueprint.clay_bot_costs[0] + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.obsidian_bot_costs[0] and clay >= blueprint.obsidian_bot_costs[1]:
            w = (time + 1, ore_bots, clay_bots, obsidian_bots + 1, geode_bots, ore - blueprint.obsidian_bot_costs[0] + ore_bots, clay - blueprint.obsidian_bot_costs[1] + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        if ore >= blueprint.geode_bot_costs[0] and obsidian >= blueprint.geode_bot_costs[2]:
            w = (time + 1, ore_bots, clay_bots, obsidian_bots, geode_bots + 1, ore - blueprint.geode_bot_costs[0] + ore_bots, clay + clay_bots, obsidian - blueprint.geode_bot_costs[2] + obsidian_bots, geode + geode_bots)
            if w not in visited:
                visited.add(w)
                q.append(w)

        w = (time + 1, ore_bots, clay_bots, obsidian_bots, geode_bots, ore + ore_bots, clay + clay_bots, obsidian + obsidian_bots, geode + geode_bots)
        if w not in visited:
            visited.add(w)
            q.append(w)

    best_geodes[index] = best_geode


blueprints = blueprints[:3]
best_geodes = [0] * len(blueprints)
pool = ThreadPool(len(blueprints))
job_args = []
for i, blueprint in enumerate(blueprints):
    job_args.append((i, blueprint))
pool.starmap(job2, job_args)
pool.close()
pool.join()

print(f"Part 2: {math.prod(best_geodes)}")
