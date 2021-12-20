import ast
import copy
import math
from pathlib import Path


def explode(n_orig, n_prev, n, left, right, depth):
    if depth == 4 and isinstance(n, list):
        if left:
            if isinstance(left[1], int):
                left[1] += n[0]
            else:
                left[0] += n[0]
        if right:
            if isinstance(right[0], int):
                right[0] += n[1]
            else:
                right[1] += n[1]

        if isinstance(n_prev[0], list):
            n_prev[0] = 0
        else:
            n_prev[1] = 0

        return True
    else:
        if isinstance(n[0], list):
            if explode(n_orig, n, n[0], left, right, depth + 1):
                return True
        if isinstance(n[1], list):
            if explode(n_orig, n, n[1], left, right, depth + 1):
                return True

    return False


def split(n_orig, n_prev, n):
    if isinstance(n, int):
        if n > 9:
            spl = [math.floor(n / 2), math.ceil(n / 2)]
            if isinstance(n_prev[0], int) and n == n_prev[0]:
                n_prev[0] = spl
            else:
                n_prev[1] = spl
            return True
    else:
        for i in range(len(n)):
            if split(n_orig, n, n[i]):
                return True

    return False


def traverse(n, n0, n1, depth, left, right, found, leftmost):
    if depth == 4:
        found[0] = True
        return True

    if isinstance(n0, list):
        if found[0] and not right and isinstance(n0[0], int):
            right.append(n0)
        at_depth = traverse(n0, n0[0], n0[1], depth + 1, left, right, found, leftmost)
        if not left and at_depth and isinstance(n[0], int):
            left.append(n)
        elif not left and at_depth:
            left.append(leftmost[0])
    else:
        leftmost[0] = n
        if found[0] and not right:
            right.append(n)

    if isinstance(n1, list):
        if found[0] and not right and isinstance(n1[0], int):
            right.append(n1)
        at_depth = traverse(n1, n1[0], n1[1], depth + 1, left, right, found, leftmost)
        if not left and at_depth and isinstance(n[0], int):
            left.append(n)
    else:
        leftmost[0] = n
        if found[0] and not right:
            right.append(n)

    return False


numbers = [ast.literal_eval(x.strip()) for x in Path('input.txt').open().readlines()]
n1 = numbers.pop(0)
n = [n1]

while len(numbers) > 0:
    n2 = numbers.pop(0)
    n.append(n2)

    left = []
    right = []
    traverse(n, n[0], n[1], 0, left, right, [False], [False])
    left = left[0] if left else None
    right = right[0] if right else None

    while True:
        left = []
        right = []
        traverse(n, n[0], n[1], 0, left, right, [False], [False])
        left = left[0] if left else None
        right = right[0] if right else None
        if explode(n, n, n, left, right, 0):
            left = []
            right = []
            traverse(n, n[0], n[1], 0, left, right, [False], [False])
            left = left[0] if left else None
            right = right[0] if right else None
            continue
        if not split(n, n, n):
            break

    n = [n]
n = n[0]


def magnitude(n):
    if isinstance(n[0], int) and isinstance(n[1], int):
        return n[0] * 3 + n[1] * 2
    elif isinstance(n[0], int) and isinstance(n[1], list):
        return 3 * n[0] + 2 * magnitude(n[1])
    elif isinstance(n[0], list) and isinstance(n[1], int):
        return 3 * magnitude(n[0]) + 2 * n[1]
    else:
        return 3 * magnitude(n[0]) + 2 * magnitude(n[1])


print(f"Part 1: {magnitude(n)}")


numbers = [ast.literal_eval(x.strip()) for x in Path('input.txt').open().readlines()]
numbers_to_add = []
for i, n1 in enumerate(numbers):
    for j, n2 in enumerate(numbers):
        if i != j:
            numbers_to_add.append([n1, n2])
            numbers_to_add.append([n2, n1])


largest = 0
while len(numbers_to_add) > 0:
    n = copy.deepcopy(numbers_to_add.pop(0))
    left = []
    right = []
    traverse(n, n[0], n[1], 0, left, right, [False], [False])
    left = left[0] if left else None
    right = right[0] if right else None

    while True:
        left = []
        right = []
        traverse(n, n[0], n[1], 0, left, right, [False], [False])
        left = left[0] if left else None
        right = right[0] if right else None
        if explode(n, n, n, left, right, 0):
            left = []
            right = []
            traverse(n, n[0], n[1], 0, left, right, [False], [False])
            left = left[0] if left else None
            right = right[0] if right else None
            continue
        if not split(n, n, n):
            break

    largest = max(largest, magnitude(n))

print(f"Part 2: {largest}")
