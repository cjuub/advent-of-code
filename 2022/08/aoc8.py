from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]
w = len(lines[0])
h = len(lines)
grid = [[0 for x in range(w)] for y in range(h)]

for y in range(h):
    for x in range(w):
        grid[y][x] = int(lines[y][x])


def is_visible(curr_x, curr_y):
    curr_height = grid[curr_y][curr_x]
    visible_down = True
    for y1 in range(curr_y + 1, h):
        if grid[y1][curr_x] >= curr_height:
            visible_down = False

    visible_up = True
    for y1 in range(0, curr_y):
        if grid[y1][curr_x] >= curr_height:
            visible_up = False

    visible_right = True
    for x1 in range(curr_x + 1, w):
        if grid[curr_y][x1] >= curr_height:
            visible_right = False

    visible_left = True
    for x1 in range(0, curr_x):
        if grid[curr_y][x1] >= curr_height:
            visible_left = False

    return visible_up or visible_down or visible_right or visible_left


cnt = 0
for y in range(1, h-1):
    for x in range(1, w-1):
        if is_visible(x, y):
            cnt += 1

print(f"Part 1: {cnt + w * 2 + h * 2 - 4}")


def scenic_score(curr_x, curr_y):
    curr_height = grid[curr_y][curr_x]
    trees_down = 0
    for y1 in range(curr_y + 1, h):
        if grid[y1][curr_x] < curr_height:
            trees_down += 1
        else:
            trees_down += 1
            break

    trees_up = 0
    for y1 in range(curr_y-1, -1, -1):
        if grid[y1][curr_x] < curr_height:
            trees_up += 1
        else:
            trees_up += 1
            break

    trees_right = 0
    for x1 in range(curr_x + 1, w):
        if grid[curr_y][x1] < curr_height:
            trees_right += 1
        else:
            trees_right += 1
            break

    trees_left = 0
    for x1 in range(curr_x-1, -1, -1):
        if grid[curr_y][x1] < curr_height:
            trees_left += 1
        else:
            trees_left += 1
            break

    return trees_up * trees_down * trees_right * trees_left


best_scenic_score = 0
for y in range(1, h-1):
    for x in range(1, w-1):
        best_scenic_score = max(scenic_score(x, y), best_scenic_score)

print(f"Part 2: {best_scenic_score}")
