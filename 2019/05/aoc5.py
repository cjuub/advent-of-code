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
    OP_HALT = 99

    class HaltException(Exception):
        pass

    def __init__(self, memory: List[int]):
        self._memory = memory[:] + [0] * 10000
        self._pc = 0
        self._input = 0
        self._output = 0
        self._instructions = {IntCodeComputer.OP_ADD: self._add,
                              IntCodeComputer.OP_MUL: self._mul,
                              IntCodeComputer.OP_LOAD: self._load,
                              IntCodeComputer.OP_STORE: self._store,
                              IntCodeComputer.OP_JUMP_IF_TRUE: self._jump_if_true,
                              IntCodeComputer.OP_JUMP_IF_FALSE: self._jump_if_false,
                              IntCodeComputer.OP_LESS_THAN: self._less_than,
                              IntCodeComputer.OP_EQUALS: self._equals}

    def _add(self, op1, op2, res):
        self._memory[res] = op1 + op2
        self._pc += 4

    def _mul(self, op1, op2, res):
        self._memory[res] = op1 * op2
        self._pc += 4

    def _load(self, op1, op2, res):
        self._memory[op1] = self._input
        self._pc += 2

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

    def _store(self, op1, op2, res):
        self._output = op1
        self._pc += 2

    def execute(self):
        while True:
            op_code_str = str(self._memory[self._pc]).rjust(5, '0')
            op_code = int(op_code_str[-2:])
            op1_mode = int(op_code_str[2])
            op2_mode = int(op_code_str[1])
            op3_mode = int(op_code_str[0])

            if op_code == IntCodeComputer.OP_HALT:
                raise IntCodeComputer.HaltException(self._output)

            if op_code == IntCodeComputer.OP_LOAD:
                op1_mode = 1

            op1 = self._memory[self._memory[self._pc + 1]] if op1_mode == 0 else self._memory[self._pc + 1]
            op2 = self._memory[self._memory[self._pc + 2]] if op2_mode == 0 else self._memory[self._pc + 2]
            res = self._memory[self._pc + 3] if op3_mode == 0 else self._pc + 3

            self._instructions[op_code](op1, op2, res)

    def set_input(self, value):
        self._input = value


with open('input.txt') as fp:
    lines = fp.readlines()

code = [int(x) for x in lines[0].split(',')]

computer = IntCodeComputer(code)
try:
    computer.set_input(1)
    computer.execute()
except IntCodeComputer.HaltException as e:
    print('Part 1: ' + str(e))


computer = IntCodeComputer(code)
try:
    computer.set_input(5)
    computer.execute()
except IntCodeComputer.HaltException as e:
    print('Part 2: ' + str(e))
