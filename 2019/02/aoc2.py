#!/usr/bin/env python3

from typing import List


class IntCodeComputer:
    OP_ADD = 1
    OP_MUL = 2
    OP_HALT = 99

    class HaltException(Exception):
        pass

    def __init__(self, memory: List[int]):
        self._memory = memory[:]
        self._pc = 0

        self._instructions = {IntCodeComputer.OP_ADD: self._add,
                              IntCodeComputer.OP_MUL: self._mul,
                              IntCodeComputer.OP_HALT: self._halt}

    def _add(self, op1, op2, res):
        self._memory[res] = op1 + op2
        self._pc += 4

    def _mul(self, op1, op2, res):
        self._memory[res] = op1 * op2
        self._pc += 4

    def _halt(self, op1, op2, res):
        raise IntCodeComputer.HaltException()

    def execute(self):
        while True:
            op1 = self._memory[self._pc + 1]
            op2 = self._memory[self._pc + 2]
            res = self._memory[self._pc + 3]
            self._instructions[self._memory[self._pc]](self._memory[op1], self._memory[op2], res)


with open('input.txt') as fp:
    lines = fp.readlines()

code = [int(x) for x in lines[0].split(',')]

computer = IntCodeComputer(code)
computer._memory[1] = 12
computer._memory[2] = 2
try:
    computer.execute()
except IntCodeComputer.HaltException:
    pass

print('Part 1: ' + str(computer._memory[0]))

for x in range(100):
    for y in range(100):
        computer = IntCodeComputer(code)
        computer._memory[1] = x
        computer._memory[2] = y
        try:
            computer.execute()
        except IntCodeComputer.HaltException:
            pass

        if computer._memory[0] == 19690720:
            print('Part 2: ' + str(100 * x + y))
