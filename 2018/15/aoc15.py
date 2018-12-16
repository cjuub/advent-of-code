#!/usr/bin/env python3

from collections import deque


class Unit:
    def __init__(self, id, x, y, type, pow):
        self.id = id
        self.pos = (x, y)
        self.type = type
        self.pow = pow
        self.hp = 200
        self.dead = False

    def __repr__(self):
        return 'id: ' + str(self.id) + ' pos: ' + str(self.pos) + ' hp: ' + str(self.hp)

    def ranges(self):
        ranges = []
        for adj in self.adjacents():
            if map[adj[0]][adj[1]] == '.':
                ranges.append((adj[0], adj[1]))

        return ranges

    def adjacents(self):
        return adjacents_to(self.pos[0], self.pos[1])

    def move(self, ranges, units):
        new_x = 0
        new_y = 0

        ranges = sorted(ranges, key=lambda range: (range[1], range[0]))
        best_dist = 9999
        best_move = None
        best_target_pos = None
        for adj in self.adjacents():
            move, dist, selected_target_pos = breadth_first_search(map, units, adj, ranges, self.pos)

            if dist == best_dist:
                choices = [(selected_target_pos[0], selected_target_pos[1]), (best_target_pos[0], best_target_pos[1])]
                choices = sorted(choices, key=lambda x: (x[1], x[0]))
                if best_target_pos != choices[0]:
                    best_move = move
                    best_target_pos = selected_target_pos
            if dist < best_dist:
                best_dist = dist
                best_move = move
                best_target_pos = selected_target_pos

        if best_move:
            new_x = best_move[0]
            new_y = best_move[1]

        if new_x != 0 and new_y != 0:
            map[self.pos[0]][self.pos[1]] = '.'
            self.pos = (new_x, new_y)
            map[self.pos[0]][self.pos[1]] = self.type

    def attack(self, target):
        target.hp -= self.pow

        if target.hp <= 0:
            map[target.pos[0]][target.pos[1]] = '.'
            target.dead = True
            target.hp = 0


def adjacents_to(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def print_map(map):
    for y in range(len(map[0])):
        for x in range(len(map)):
            print(str(map[x][y]), end=' ')
        print()


def build_path(curr, parent, meta, curr_pos):
    path = []
    next = parent
    path.append(curr)
    while next != None:
        path.append(next)
        next = meta[next][1]

    path.append(curr_pos)
    path = path[:-1]

    return path


def breadth_first_search(map, units, start_pos, targets, curr_pos):
    queue = deque([(start_pos, 0)])
    visited = set()
    blocked_positions = [unit.pos for unit in units if not unit.dead]
    if start_pos in blocked_positions or map[start_pos[0]][start_pos[1]] != '.':
        return None, 999999, None

    node_info = {}
    node_info[start_pos] = (0, None)
    while queue:
        pos, dist = queue.popleft()
        for adj in adjacents_to(pos[0], pos[1]):
            if adj in visited:
                continue

            if map[adj[0]][adj[1]] != '.' or adj in blocked_positions:
                continue

            if adj not in node_info.keys() or node_info[adj] > (dist + 1, pos):
                node_info[adj] = (dist + 1, pos)

            adj_in_queue = False
            for entry in queue:
                if adj == entry[0]:
                    adj_in_queue = True

            if not adj_in_queue:
                queue.append((adj, dist + 1))

        visited.add(pos)

    path = []
    for curr, (dist, parent) in node_info.items():
        if curr in targets:
            if len(path) > 0 and dist + 1 < len(path):
                pass

            elif dist + 1 == len(path) and len(path) > 1:
                choices = [(curr[0], curr[1]), (path[0][0], path[0][1])]
                choices = sorted(choices, key=lambda x: (x[1], x[0]))
                if path[0] == choices[0]:
                    continue
            elif len(path) > 0:
                continue

            path = build_path(curr, parent, node_info, curr_pos)

    if len(path) > 0:
        return path[-1], len(path), path[0]
    else:
        return None, 999999, None


for pow in range(3, 500):
    lines = []
    with open('input.txt') as fp:
        for line in fp:
            lines.append(list(line.strip()))

    map = [['' for y in range(len(lines))] for x in range(len(lines[0]))]
    goblins = {}
    elves = {}
    units = []
    id = 0
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            map[x][y] = lines[y][x]
            if map[x][y] == 'G':
                goblin = Unit(id, x, y, 'G', 3)
                goblins[id] = goblin
                id += 1
                units.append(goblin)
            elif map[x][y] == 'E':
                elf = Unit(id, x, y, 'E', pow)
                elves[id] = elf
                id += 1
                units.append(elf)

    rounds_completed = 0
    done = False
    dead_elf = False
    for round in range(1, 200):
        units = sorted(units, key=lambda unit: (unit.pos[1], unit.pos[0]))
        sum = 0

        for unit in [x for x in units if not x.dead]:
            if unit.dead:
                continue

            is_elf = unit.id in elves.keys()
            target = 'G' if is_elf else 'E'
            enemies = goblins if is_elf else elves

            all_dead = True
            for enemy in enemies.values():
                if not enemy.dead:
                    all_dead = False

            if all_dead:
                rounds_completed = round - 1
                done = True
                break

            ranges = []
            enemy_list = sorted(enemies.values(), key=lambda enemy: (enemy.pos[1], enemy.pos[0]))
            for enemy in enemy_list:
                if not enemy.dead:
                    ranges.extend(enemy.ranges())

            selected_target = None
            min_hp = 9999999
            for adj in unit.adjacents():
                if map[adj[0]][adj[1]] == target:
                    for enemy in enemy_list:
                        if enemy.pos == (adj[0], adj[1]):
                            if enemy.hp < min_hp and not enemy.dead:
                                selected_target = enemy
                                min_hp = enemy.hp
            if selected_target:
                unit.attack(selected_target)
                continue

            if len(ranges) == 0:
                continue

            unit.move(ranges, units)

            selected_target = None
            min_hp = 9999999
            for adj in unit.adjacents():
                if map[adj[0]][adj[1]] == target:
                    for enemy in enemy_list:
                        if enemy.pos == (adj[0], adj[1]):
                            if enemy.hp < min_hp and not enemy.dead:
                                selected_target = enemy
                                min_hp = enemy.hp

            if selected_target:
                unit.attack(selected_target)

        if not done:
            for enemies in [goblins, elves]:
                all_dead = True
                for enemy in enemies.values():
                    if not enemy.dead:
                        all_dead = False

                if all_dead:
                    rounds_completed = round
                    done = True
                    break

        if done:
            break

    sum = 0
    for unit in units:
        sum += unit.hp
    print(sum)
    print(rounds_completed)
    print(sum * rounds_completed)

    all_elves_alive = True
    for elf in elves.values():
        if elf.dead:
            all_elves_alive = False

    if all_elves_alive:
        exit(0)
