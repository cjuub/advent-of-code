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
        try:
            self._memory[op1] = self._input[self._inputs_read]
        except:
            self._memory[op1] = -1
            return -1

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
                if op_code == IntCodeComputer.OP_LOAD:
                    return None
                return int(ret)

    def set_input(self, value):
        self._input = value


with open('input.txt') as fp:
    code = list(map(int, fp.readline().strip().split(",")))

comps = {}
for i in range(50):
    comp = IntCodeComputer(code)
    comp.set_input([i, -1])
    comps[i] = comp


done = False
while not done:
    for i in range(50):
        try:
            comp = comps[i]
            addr = comp.execute()
            if addr is None:
                continue

            x = comp.execute()
            y = comp.execute()

            if addr == 255:
                print('Part 1: ' + str(y))
                done = True
                break

            comps[addr].set_input(comps[addr]._input + [x, y])
            comps[addr]._inputs_read = 0

            comp.set_input([-1])
            comp._inputs_read = 0
        except IntCodeComputer.HaltException as e:
            pass


comps = {}
for i in range(50):
    comp = IntCodeComputer(code)
    comp.set_input([i, -1])
    comps[i] = comp

nat_x = -1
nat_y = -1
prev_nat_y = -1
while True:
    idle = True
    for i in range(50):
        try:
            comp = comps[i]
            addr = comp.execute()
            if addr is None:
                continue

            idle = False
            x = comp.execute()
            y = comp.execute()

            if addr == 255:
                nat_x = x
                nat_y = y
            else:
                comps[addr].set_input(comps[addr]._input + [x, y])
                comps[addr]._inputs_read = 0

            comp.set_input([-1])
            comp._inputs_read = 0
        except IntCodeComputer.HaltException as e:
            pass

    if idle:
        if nat_y == prev_nat_y:
            print('Part 2: ' + str(nat_y))
            break
        comps[0].set_input(comps[0]._input + [nat_x, nat_y])
        comps[0]._inputs_read = 0
        prev_nat_y = nat_y

