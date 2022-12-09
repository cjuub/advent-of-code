from pathlib import Path
from typing import List

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

moves = []
for line in lines:
    direction = line.split(" ")[0]
    steps = int(line.split(" ")[1])
    moves.append((direction, steps))


def move(x, y, direction):
    if direction == "R":
        return x + 1, y
    elif direction == "L":
        return x - 1, y
    elif direction == "U":
        return x, y - 1
    else:
        return x, y + 1


def adjacents_with_diag(x, y):
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]


def adjacents(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]


def follow(hx, hy, tx, ty, hx_prev, hy_prev, direction):
    if (hx, hy) in [*adjacents_with_diag(tx, ty), (tx, ty)]:
        return tx, ty

    tx, ty = move(tx, ty, direction)
    if (hx, hy) in [*adjacents(tx, ty), (tx, ty)]:
        return tx, ty

    return hx_prev, hy_prev


def follow2(hx, hy, tx, ty, direction):
    if (hx, hy) in [*adjacents_with_diag(tx, ty), (tx, ty)]:
        return tx, ty

    orig_tx = tx
    orig_ty = ty
    tx, ty = move(tx, ty, direction)
    if (hx, hy) in [*adjacents(tx, ty), (tx, ty)]:
        return tx, ty

    s1 = set(adjacents_with_diag(orig_tx, orig_ty)).intersection(adjacents_with_diag(hx, hy))
    s2 = set(adjacents_with_diag(orig_tx, orig_ty)).intersection(adjacents(hx, hy))
    if len(s1) == 1:
        return s1.pop()
    elif len(s2) == 1:
        return s2.pop()
    else:
        assert False


head = (0, 0)
tail = (0, 0)
tail_poses = set()
tail_poses.add(tail)
for direction, steps in moves:
    for step in range(steps):
        head_prev = head
        head = move(*head, direction)
        tail = follow(*head, *tail, *head_prev, direction)
        tail_poses.add(tail)

print(f"Part 1: {len(tail_poses)}")


def print_rope(rope: List):
    w = 50
    h = 50
    w_half = int(w/2)
    h_half = int(h/2)
    grid = [["." for x in range(w)] for y in range(h)]

    print(rope)
    for y in range(-h_half, h_half):
        for x in range(-w_half, w_half):
            if (x, y) == (0, 0):
                grid[y][x] = "s"
            if (x, y) in rope:
                grid[y][x] = rope.index((x, y))
            print(grid[y][x], end="")
        print()
    print()


rope = [(0, 0)] * 10
tail_poses = {rope[-1]}
for direction, steps in moves:
    for step in range(steps):
        rope[0] = move(*rope[0], direction)
        knot_to_follow = rope[0]
        for i, knot in enumerate(rope[1:]):
            rope[i+1] = follow2(*knot_to_follow, *knot, direction)
            knot_to_follow = rope[i+1]
        tail_poses.add(rope[-1])

    # print_rope(rope)

print(f"Part 2: {len(tail_poses)}")
