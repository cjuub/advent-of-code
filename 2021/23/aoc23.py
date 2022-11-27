from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Tuple, List

lines = [x.replace("\n", "") for x in Path("input2.txt").open("r").readlines()]

w = len(lines[0])
h = len(lines)
g = [["" for y in range(h+1)] for x in range(w)]

initial_amphi_positions = defaultdict(list)
for y in range(h):
    for x in range(w):
        if x not in range(len(lines[y])):
            lines[y] = lines[y] + " "
        g[x][y] = lines[y][x]

        if lines[y][x] == "A":
            initial_amphi_positions["A"].append((x, y))
        if lines[y][x] == "B":
            initial_amphi_positions["B"].append((x, y))
        if lines[y][x] == "C":
            initial_amphi_positions["C"].append((x, y))
        if lines[y][x] == "D":
            initial_amphi_positions["D"].append((x, y))

energies = {"A": 1, "B": 10, "C": 100, "D": 1000}

initial_amphi_positions = dict(initial_amphi_positions)

# Part 1
# goals = {"A": [(3, 2), (3, 3)], "B": [(5, 2), (5, 3)], "C": [(7, 2), (7, 3)], "D": [(9, 2), (9, 3)]}
# Part 2
goals = {"A": [(3, 2), (3, 3), (3, 4), (3, 5)], "B": [(5, 2), (5, 3), (5, 4), (5, 5)], "C": [(7, 2), (7, 3), (7, 4), (7, 5)], "D": [(9, 2), (9, 3), (9, 4), (9, 5)]}
hallway = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1)]


def print_grid(grid):
    for y in range(h):
        for x in range(w):
            print(grid[x][y], end="")
        print()
    print()


def adjacents(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def valid_moves(grid, pos, amphi, prev_pos) -> List[Tuple[int, int]]:
    moves = []
    for x, y in adjacents(*pos):
        if grid[x][y] != ".":
            continue
        if (x, y) == prev_pos:
            continue

        moves.append((x, y))

    return moves


def do_can_move_to_room(grid, amphi, pos, prev_pos, path):
    if pos in goals[amphi]:
        if grid[pos[0]][pos[1]+1] == amphi or grid[pos[0]][pos[1]+1] == "#":
            return True, path
        elif grid[pos[0]][pos[1]+1] == ".":
            move = (pos[0], pos[1]+1)
            new_path = path[:]
            new_path.append(move)
            res, p = do_can_move_to_room(grid, amphi, move, pos, new_path)
            if res:
                return res, p
        else:
            assert False

    moves = valid_moves(grid, pos, amphi, prev_pos)
    if moves:
        for move in moves:
            new_path = path[:]
            new_path.append(move)
            res, p = do_can_move_to_room(grid, amphi, move, pos, new_path)
            if res:
                return res, p

    return False, []


def can_move_to_room(grid, amphi, pos):
    if other_amphi_in_goal(grid, amphi):
        return False, []
    return do_can_move_to_room(grid, amphi, pos, (-1, -1), [])


def is_other_room(amphi, position):
    other_goal = False
    for amphi_goal, goal_poses in goals.items():
        if amphi_goal == amphi:
            continue
        if position in goal_poses:
            other_goal = True
            break
    return other_goal


def is_all_in_goal(amphi_positions):
    all_in_goal = True
    for amphi, positions in amphi_positions.items():
        for i, position in enumerate(positions):
            if position not in goals[amphi]:
                all_in_goal = False
                break
        if not all_in_goal:
            break

    return all_in_goal


def do_can_move_to_pos(grid, amphi, curr_pos, target_pos, prev_pos, path):
    if curr_pos == target_pos:
        return True, path

    moves = valid_moves(grid, curr_pos, amphi, prev_pos)
    if moves:
        for move in moves:
            new_path = path[:]
            new_path.append(move)
            return do_can_move_to_pos(grid, amphi, move, target_pos, curr_pos, new_path)

    return False, []


def can_move_to_pos(grid, amphi, curr_pos, target_pos):
    return do_can_move_to_pos(grid, amphi, curr_pos, target_pos, (-1. -1), [])


def other_amphi_in_goal(grid, amphi):
    has_other_amphi = False
    for goal_pos_x, goal_pos_y in goals[amphi]:
        if grid[goal_pos_x][goal_pos_y] != amphi and grid[goal_pos_x][goal_pos_y] != ".":
            has_other_amphi = True
    return has_other_amphi


def in_top_of_room(grid, pos):
    next_pos = (pos[0], pos[1]-1)
    while next_pos not in hallway:
        if grid[next_pos[0]][next_pos[1]] != ".":
            return False
        next_pos = (next_pos[0], next_pos[1]-1)
    return True


blacklist = [(3, 1), (5, 1), (7, 1), (9, 1)]


def move(grid, amphi_positions):
    # print_grid(grid)
    if is_all_in_goal(amphi_positions):
        return True, 0

    super_best_energy = 9999999999
    solution_found = False
    for amphi, positions in amphi_positions.items():
        for i, position in enumerate(positions):
            is_in_other_room = is_other_room(amphi, position)
            if is_in_other_room and in_top_of_room(grid, position):
                can_move, path = can_move_to_room(grid, amphi, position)
                if can_move:
                    new_amphi_positions = deepcopy(amphi_positions)
                    new_grid = deepcopy(grid)
                    new_grid[position[0]][position[1]] = "."
                    new_grid[path[-1][0]][path[-1][1]] = amphi
                    new_amphi_positions[amphi][i] = path[-1]

                    res, energy = move(new_grid, new_amphi_positions)
                    if res:
                        solution_found = True
                        tot_energy = energy + energies[amphi] * len(path)
                        if tot_energy <= super_best_energy:
                            super_best_energy = tot_energy

            elif position in hallway:
                can_move, path = can_move_to_room(grid, amphi, position)
                if can_move:
                    new_amphi_positions = deepcopy(amphi_positions)
                    new_grid = deepcopy(grid)
                    new_grid[position[0]][position[1]] = "."
                    new_grid[path[-1][0]][path[-1][1]] = amphi
                    new_amphi_positions[amphi][i] = path[-1]

                    res, energy = move(new_grid, new_amphi_positions)
                    if res:
                        solution_found = True
                        tot_energy = energy + energies[amphi] * len(path)
                        if tot_energy <= super_best_energy:
                            super_best_energy = tot_energy

    if not solution_found:
        second_pass_amphi_positions = deepcopy(amphi_positions)
        second_pass_grid = deepcopy(grid)

        for amphi, positions in second_pass_amphi_positions.items():
            for i, position in enumerate(positions):
                is_in_other_room = is_other_room(amphi, position)
                if is_in_other_room and in_top_of_room(second_pass_grid, position):
                    best_energy = 99999999999
                    for hallway_pos in hallway:
                        if hallway_pos in blacklist:
                            continue

                        res, path = can_move_to_pos(second_pass_grid, amphi, position, hallway_pos)
                        if res:
                            new_amphi_positions = deepcopy(second_pass_amphi_positions)
                            new_grid = deepcopy(second_pass_grid)
                            new_grid[position[0]][position[1]] = "."
                            new_grid[path[-1][0]][path[-1][1]] = amphi
                            new_amphi_positions[amphi][i] = path[-1]
                            res, energy = move(new_grid, new_amphi_positions)
                            if res:
                                solution_found = True
                                tot_energy = energy + energies[amphi] * len(path)
                                best_energy = min(best_energy, tot_energy)
                    if solution_found:
                        super_best_energy = min(super_best_energy, best_energy)

                elif position in hallway:
                    # stay were we are
                    pass
                elif position in goals[amphi] and in_top_of_room(second_pass_grid, position):
                    if other_amphi_in_goal(second_pass_grid, amphi):
                        # move out of the way
                        best_energy = 99999999999
                        for hallway_pos in hallway:
                            if hallway_pos in blacklist:
                                continue

                            res, path = can_move_to_pos(second_pass_grid, amphi, position, hallway_pos)
                            if res:
                                new_amphi_positions = deepcopy(second_pass_amphi_positions)
                                new_grid = deepcopy(second_pass_grid)
                                new_grid[position[0]][position[1]] = "."
                                new_grid[path[-1][0]][path[-1][1]] = amphi
                                new_amphi_positions[amphi][i] = path[-1]
                                res, energy = move(new_grid, new_amphi_positions)
                                if res:
                                    solution_found = True
                                    tot_energy = energy + energies[amphi] * len(path)
                                    best_energy = min(best_energy, tot_energy)

                        if solution_found:
                            super_best_energy = min(super_best_energy, best_energy)

    return solution_found, super_best_energy


res = move(g, deepcopy(initial_amphi_positions))
print(res[1])
