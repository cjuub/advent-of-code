#!/usr/bin/env python3
import random
from typing import List

from networkx import Graph
from networkx.algorithms import shortest_path_length


class IntCodeComputer:
    OP_ADD = 1
    OP_MUL = 2
    OP_LOAD = 3
    OP_STORE = 4
    OP_JUMP_IF_TRUE = 5
    OP_JUMP_IF_FALSE = 6
    OP_LESS_THAN = 7
    OP_EQUALS = 8
    OP_REL_BASE = 9
    OP_HALT = 99

    class HaltException(Exception):
        pass

    def __init__(self, memory: List[int]):
        self._memory = memory[:] + [0] * 100000
        self._pc = 0
        self._input = []
        self._inputs_read = 0
        self._output = 0
        self._rel_base = 0
        self._instructions = {IntCodeComputer.OP_ADD: self._add,
                              IntCodeComputer.OP_MUL: self._mul,
                              IntCodeComputer.OP_LOAD: self._load,
                              IntCodeComputer.OP_STORE: self._store,
                              IntCodeComputer.OP_JUMP_IF_TRUE: self._jump_if_true,
                              IntCodeComputer.OP_JUMP_IF_FALSE: self._jump_if_false,
                              IntCodeComputer.OP_LESS_THAN: self._less_than,
                              IntCodeComputer.OP_EQUALS: self._equals,
                              IntCodeComputer.OP_REL_BASE: self._change_rel_base}

    def _add(self, op1, op2, res):
        self._memory[res] = op1 + op2
        self._pc += 4

    def _mul(self, op1, op2, res):
        self._memory[res] = op1 * op2
        self._pc += 4

    def _load(self, op1, op2, res):
        self._memory[op1] = self._input[self._inputs_read]
        self._inputs_read += 1
        self._pc += 2

    def _store(self, op1, op2, res):
        self._output = op1
        self._pc += 2

        return self._output

    def _jump_if_true(self, op1, op2, res):
        if op1 != 0:
            self._pc = op2
        else:
            self._pc += 3

    def _jump_if_false(self, op1, op2, res):
        if op1 == 0:
            self._pc = op2
        else:
            self._pc += 3

    def _less_than(self, op1, op2, res):
        if op1 < op2:
            self._memory[res] = 1
        else:
            self._memory[res] = 0
        self._pc += 4

    def _equals(self, op1, op2, res):
        if op1 == op2:
            self._memory[res] = 1
        else:
            self._memory[res] = 0
        self._pc += 4

    def _change_rel_base(self, op1, op2, res):
        self._rel_base += op1
        self._pc += 2

    def execute(self) -> int:
        while True:
            op_code_str = str(self._memory[self._pc]).rjust(5, '0')
            op_code = int(op_code_str[-2:])
            op1_mode = int(op_code_str[2])
            op2_mode = int(op_code_str[1])
            op3_mode = int(op_code_str[0])

            if op_code == IntCodeComputer.OP_HALT:
                raise IntCodeComputer.HaltException(self._output)

            if op1_mode == 0:
                # Only instruction with write on op1
                if op_code == IntCodeComputer.OP_LOAD:
                    op1 = self._memory[self._pc + 1]
                else:
                    op1 = self._memory[self._memory[self._pc + 1]]
            elif op1_mode == 1:
                op1 = self._memory[self._pc + 1]
            else:
                if op_code == IntCodeComputer.OP_LOAD:
                    op1 = self._rel_base + self._memory[self._pc + 1]
                else:
                    op1 = self._memory[self._rel_base + self._memory[self._pc + 1]]

            if op2_mode == 0:
                op2 = self._memory[self._memory[self._pc + 2]]
            elif op2_mode == 1:
                op2 = self._memory[self._pc + 2]
            else:
                op2 = self._memory[self._rel_base + self._memory[self._pc + 2]]

            if op3_mode == 0:
                res = self._memory[self._pc + 3]
            elif op3_mode == 1:
                res = self._pc + 3
            else:
                res = self._rel_base + self._memory[self._pc + 3]

            ret = self._instructions[op_code](op1, op2, res)
            if ret is not None:
                return int(ret)

    def set_input(self, value):
        self._input = value


with open('input.txt') as fp:
    code = list(map(int, fp.readline().strip().split(",")))

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
OK = 1
WIN = 2

droid_x = 30
droid_y = 30
grid = [['/' for y in range(60)] for x in range(60)]

graph = Graph()
comp = IntCodeComputer(code)

visited = set()

mov_cmd = NORTH
cnt = 0
target = (-1, -1)
try:
    while True:
        comp.set_input([mov_cmd])
        comp._inputs_read = 0
        out = comp.execute()

        if out == WALL:

            if mov_cmd == NORTH:
                grid[droid_y - 1][droid_x] = '#'
                visited.add((droid_x, droid_y))
            elif mov_cmd == EAST:
                grid[droid_y][droid_x + 1] = '#'
            elif mov_cmd == SOUTH:
                grid[droid_y + 1][droid_x] = '#'
            else:
                grid[droid_y][droid_x - 1] = '#'
        elif out == OK or out == WIN:
            if mov_cmd == NORTH:
                droid_y -= 1
                graph.add_edge((droid_x, droid_y + 1), (droid_x, droid_y))
            elif mov_cmd == EAST:
                droid_x += 1
                graph.add_edge((droid_x - 1, droid_y), (droid_x, droid_y))
            elif mov_cmd == SOUTH:
                droid_y += 1
                graph.add_edge((droid_x, droid_y - 1), (droid_x, droid_y))
            else:
                droid_x -= 1
                graph.add_edge((droid_x + 1, droid_y), (droid_x, droid_y))

            grid[droid_y][droid_x] = '.'

        mov_cmd = random.randint(1, 4)

        if cnt % 10000 == 0:
            for y in range(60):
                for x in range(60):
                    print(grid[y][x], end='')
                print()
            print(cnt)

        if out == WIN:
            target = (droid_x, droid_y)
            grid[droid_y][droid_x] = 'O'
            # break

        cnt += 1
        if cnt > 1000000:
            break
except IntCodeComputer.HaltException:
    pass

pos = [target[0], target[1]]
i = 0
while True:
    dot_found = False
    new_o_pos = set()
    for y in range(60):
        for x in range(60):
            if grid[y][x] == '.':
                dot_found = True
            if grid[y][x] == 'O' and (x, y) not in new_o_pos:
                if grid[y][x + 1] != '#' and grid[y][x + 1] != 'O':
                    grid[y][x + 1] = 'O'
                    new_o_pos.add((x + 1, y))
                if grid[y][x - 1] != '#' and grid[y][x - 1] != 'O':
                    grid[y][x - 1] = 'O'
                    new_o_pos.add((x - 1, y))
                if grid[y + 1][x] != '#' and grid[y + 1][x] != 'O':
                    grid[y + 1][x] = 'O'
                    new_o_pos.add((x, y + 1))
                if grid[y - 1][x] != '#' and grid[y - 1][x] != 'O':
                    grid[y - 1][x] = 'O'
                    new_o_pos.add((x, y - 1))

    for y2 in range(60):
        for x2 in range(60):
            print(grid[y2][x2], end='')
        print()

    i += 1
    if not dot_found:
        break

path_lengths = shortest_path_length(graph, source=(30, 30), target=target)
print('Part 1: ' + str(path_lengths))
print('Part 2: ' + str(i))
