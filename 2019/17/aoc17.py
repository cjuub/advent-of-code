#!/usr/bin/env python3

from typing import List


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

grid = [['/' for y3 in range(100)] for x3 in range(100)]

x = 0
y = 0

comp = IntCodeComputer(code)
try:
    while True:
        out = comp.execute()

        if out == 10:
            grid[y][x] = 'N'
            x = 0
            y += 1
        else:
            x += 1
            grid[y][x] = chr(out)
except IntCodeComputer.HaltException:
    pass

intersections = set()
cnt = 0
for y in range(100):
    for x in range(100):
        if grid[y][x] == '#':
            intersection = True

            if grid[y][x + 1] != '#':
                intersection = False
            if grid[y][x - 1] != '#':
                intersection = False
            if grid[y + 1][x] != '#':
                intersection = False
            if grid[y - 1][x] != '#':
                intersection = False

            if intersection:
                grid[y][x] = 'O'
                cnt += 1
                intersections.add((x, y))

sum_param = 0
for intersection in intersections:
    align_x = intersection[0] - 1
    align_y = intersection[1]
    param = align_x * align_y
    sum_param += param

print('Part 1: ' + str(sum_param))

code[0] = 2
MAIN = 'B,C,B,C,A,A,C,B,C,A\n'
A = 'L,10,R,12,R,8\n'
B = 'L,12,L,10,R,8,L,12\n'
C = 'R,8,R,10,R,12\n'
VIDEO = 'n\n'

PROGRAM = MAIN + A + B + C + VIDEO
PROGRAM_ASCII = []
for c in PROGRAM:
    PROGRAM_ASCII.append(ord(str(c)))

comp = IntCodeComputer(code)
comp.set_input(PROGRAM_ASCII)
try:
    while True:
        out = comp.execute()
        # print(chr(out), end='')

except IntCodeComputer.HaltException as e:
    print('Part 2: ' + str(e.args[0]))
