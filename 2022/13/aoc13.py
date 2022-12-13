import ast
from copy import deepcopy
from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

pairs = []
for i, line in enumerate(lines):
    if line == "":
        pairs.append((ast.literal_eval(lines[i-2]), ast.literal_eval(lines[i-1])))
pairs.append((ast.literal_eval(lines[-2]), ast.literal_eval(lines[-1])))


def compare(left, right):
    if not left and not right:
        return False, False

    if not left:
        return True, True

    if not right:
        return True, False

    if isinstance(left[0], int) and isinstance(right[0], int):
        if left[0] < right[0]:
            return True, True

        if right[0] < left[0]:
            return True, False
    elif isinstance(left[0], list) and isinstance(right[0], list):
        solution_found, solution = compare(deepcopy(left[0]), deepcopy(right[0]))
        if solution_found:
            return solution_found, solution

    elif isinstance(left[0], int) and isinstance(right[0], list):
        new_left = deepcopy(left)
        new_left[0] = [left[0]]
        return compare(new_left, right)
    elif isinstance(left[0], list) and isinstance(right[0], int):
        new_right = deepcopy(right)
        new_right[0] = [right[0]]
        return compare(left, new_right)
    else:
        assert False

    return compare(deepcopy(left[1:]), deepcopy(right[1:]))


s = 0
for i, (l, r) in enumerate(pairs):
    solution_found, solution = compare(l, r)
    if solution_found and solution:
        s += (i+1)

print(f"Part 1: {s}")

packets = []
for i, line in enumerate(lines):
    if line == "":
        continue
    packets.append(ast.literal_eval(line))

packets.append([[2]])
packets.append([[6]])

solutions = []
for p1 in packets:
    nbr_greater = 0
    for p2 in packets:
        if p1 == p2:
            continue
        solution_found, solution = compare(p1, p2)
        if solution_found and solution:
            nbr_greater += 1
    solutions.append((p1, nbr_greater))

solutions.sort(key=lambda x: x[1], reverse=True)

decoder_key = 1
for i, (packet, _) in enumerate(solutions):
    if str(packet) == "[[6]]":
        decoder_key *= (i+1)
    if str(packet) == "[[2]]":
        decoder_key *= (i+1)

print(f"Part 2: {decoder_key}")
