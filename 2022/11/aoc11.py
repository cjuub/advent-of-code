import dataclasses
from pathlib import Path
from typing import List, Callable, Tuple


@dataclasses.dataclass
class Monkey:
    items: List[int]
    operation: Callable
    operands: Tuple[str, str]
    divisor: int
    throws_to: Tuple[int, int]


def mul1(a, b):
    return a * b


def add1(a, b):
    return a + b


lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

i = 0
monkeys = []
inspection_counts = {}
for j in range(0, len(lines), 7):
    items = [int(x) for x in lines[j+1].split(": ")[1].split(", ")]
    op = lines[j+2].split(" = ")[1]
    if "*" in op:
        operands = (op.split(" * ")[0], op.split(" * ")[1])
        op = mul1
    else:
        operands = (op.split(" + ")[0], op.split(" + ")[1])
        op = add1
    divisor = int(lines[j+3].split(" ")[-1])
    throws_to = (int(lines[j+4].split(" ")[-1]), int(lines[j+5].split(" ")[-1]))
    monkeys.append(Monkey(items, op, operands, divisor, throws_to))
    inspection_counts.setdefault(i, 0)
    i += 1

for i in range(20):
    for j, monkey in enumerate(monkeys):
        if len(monkey.items) == 0:
            continue

        for item in monkey.items:
            operands = (int(monkey.operands[0].replace("old", f"{item}")), int(monkey.operands[1].replace("old", f"{item}")))
            worry = monkey.operation(*operands)
            worry = int(worry / 3)
            if worry % monkey.divisor == 0:
                monkeys[monkey.throws_to[0]].items.append(worry)
            else:
                monkeys[monkey.throws_to[1]].items.append(worry)

            inspection_counts[j] += 1
        monkey.items.clear()

inspection_counts_list = list(inspection_counts.values())
inspection_counts_list.sort(reverse=True)
print(f"Part 1: {inspection_counts_list[0] * inspection_counts_list[1]}")


def mul2(item, a, b):
    if a == "old" and b != "old":
        return item * int(b)
    else:
        return item * item


def add2(item, a, b):
    res = item + int(b)
    return res


i = 0
monkeys = []
inspection_counts = {}
mod_prod = 1
for j in range(0, len(lines), 7):
    items = [int(x) for x in lines[j+1].split(": ")[1].split(", ")]
    op = lines[j+2].split(" = ")[1]
    if "*" in op:
        operands = (op.split(" * ")[0], op.split(" * ")[1])
        op = mul2
    else:
        operands = (op.split(" + ")[0], op.split(" + ")[1])
        op = add2
    divisor = int(lines[j+3].split(" ")[-1])
    throws_to = (int(lines[j+4].split(" ")[-1]), int(lines[j+5].split(" ")[-1]))
    monkeys.append(Monkey(items, op, operands, divisor, throws_to))
    inspection_counts.setdefault(i, 0)
    mod_prod *= divisor
    i += 1


for i in range(10000):
    for j, monkey in enumerate(monkeys):
        if len(monkey.items) == 0:
            continue

        for item in monkey.items:
            worry = monkey.operation(item, *monkey.operands)
            is_divisible = (worry % monkey.divisor) == 0
            next_worry = worry % mod_prod

            if is_divisible:
                monkeys[monkey.throws_to[0]].items.append(next_worry)
            else:
                monkeys[monkey.throws_to[1]].items.append(next_worry)

            inspection_counts[j] += 1
        monkey.items.clear()


inspection_counts_list = list(inspection_counts.values())
inspection_counts_list.sort(reverse=True)
print(f"Part 2: {inspection_counts_list[0] * inspection_counts_list[1]}")
