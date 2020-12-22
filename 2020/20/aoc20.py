#!/usr/bin/env python3
import math

with open('input.txt') as fp:
    lines = fp.readlines()


def copy_grid(grid):
    copy = [['' for y in range(len(grid[0]))] for x in range(len(grid))]
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            copy[x][y] = grid[x][y]

    return copy


def print_grid(grid):
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            print(grid[x][y], end='')
        print()


n = 10
i = 0
imgs = []
ids = {}
id_to_img = {}

while True:
    line = lines[i].strip()
    while line == '':
        i += 1
        break

    if i == len(lines):
        break

    grid = [['.' for y in range(n)] for x in range(n)]
    for y in range(n):
        for x in range(n):
            grid[x][y] = lines[i + y + 1][x]

    img = copy_grid(grid)
    imgs.append(img)
    ids[len(imgs) - 1] = int(lines[i].strip().split(' ')[1][:-1])
    id_to_img[ids[len(imgs) - 1]] = img

    i += 12
    if i >= len(lines):
        break


def is_border_matching(b1, b2):
    for i, p1 in enumerate(b1):
        p2 = b2[i]
        if p1 != p2:
            return False

    return True

def is_border_matching_flipped(b1, b2):
    for i, p1 in enumerate(reversed(b1)):
        p2 = b2[i]
        if p1 != p2:
            return False

    return True

def get_hor_line(img, y):
    res = []
    for x in range(n):
        res.append(img[x][y])

    return res

BELOW = 0
ABOVE = 1
LEFT = 2
RIGHT = 3

ans = 1
matching = {}
for i, img1 in enumerate(imgs):
    left1 = [p for p in img1[0]]
    right1 = [p for p in img1[-1]]
    top1 = get_hor_line(img1, 0)
    bot1 = get_hor_line(img1, n - 1)
    borders1 = [left1, right1, top1, bot1]

    matches = []
    for j, img2 in enumerate(imgs):
        if i == j:
            continue

        left2 = [p for p in img2[0]]
        right2 = [p for p in img2[-1]]
        top2 = get_hor_line(img2, 0)
        bot2 = get_hor_line(img2, n-1)
        borders2 = [left2, right2, top2, bot2]

        for k, b1 in enumerate(borders1):
            for l, b2 in enumerate(borders2):
                if is_border_matching(b1, b2) or is_border_matching_flipped(b1, b2):
                    if k == 0:
                        matches.append((ids[j], LEFT))
                    if k == 1:
                        matches.append((ids[j], RIGHT))
                    if k == 2:
                        matches.append((ids[j], ABOVE))
                    if k == 3:
                        matches.append((ids[j], BELOW))

    if len(matches) == 2:
        ans *= ids[i]

    matching[ids[i]] = matches

print('Part 1: {}'.format(ans))

grid = [['.' for y in range((n-2) * int(math.sqrt(len(imgs))))] for x in range((n-2) * int(math.sqrt(len(imgs))))]


def add_to_grid(grid, img, x_slot, y_slot):
    for y in range(y_slot * len(img), y_slot * len(img) + len(img)):
        for x in range(x_slot * len(img), x_slot * len(img) + len(img)):
            grid[x][y] = img[x % len(img)][y % len(img)]


def flip_image_y(img):
    ret = copy_grid(img)

    for y in range(len(img)):
        for x in range(len(img)):
            ret[x][len(img) - y - 1] = img[x][y]

    return ret


def flip_image_x(img):
    ret = copy_grid(img)

    for y in range(len(img)):
        for x in range(len(img)):
            ret[len(img) - x - 1][y] = img[x][y]

    return ret


def rotate_image(img, rot):
    ret = copy_grid(img)

    while rot != 0:
        img_copy = copy_grid(ret)
        for y in range(len(img)):
            for x in range(len(img)):
                ret[len(img) - y - 1][x] = img_copy[x][y]

        rot -= 90

    return ret


def remove_border(img):
    ret = [['.' for y in range(len(img)-2)] for x in range(len(img)-2)]
    for y in range(1, len(img) - 1):
        for x in range(1, len(img) - 1):
            ret[x - 1][y - 1] = img[x][y]

    return ret


next_img = None
for i, img in enumerate(imgs):
    if len(matching[ids[i]]) == 2:
        matches = matching[ids[i]]
        if matches[0][1] == RIGHT and matches[1][1] == ABOVE:
            flipped = flip_image_y(imgs[i])
            next_img = (ids[i], flipped, 0, 0)
            break
        if matches[0][1] == RIGHT and matches[1][1] == BELOW:
            flipped = flip_image_y(imgs[i])
            next_img = (ids[i], imgs[i], 0, 0)
            break
        if matches[0][1] == LEFT and matches[1][1] == ABOVE:
            flipped = flip_image_y(flip_image_x(imgs[i]))
            next_img = (ids[i], flipped, 0, 0)
            break
        if matches[0][1] == LEFT and matches[1][1] == BELOW:
            flipped = flip_image_x(imgs[i])
            next_img = (ids[i], flipped, 0, 0)
            break


add_to_grid(grid, remove_border(next_img[1]), 0, 0)

slots_to_imgs = {}
slots_to_imgs[(0, 0)] = (next_img[0], next_img[1])

for slot_y in range(int(math.sqrt(len(imgs)))):
    for slot_x in range(int(math.sqrt(len(imgs)))):
        if (slot_x, slot_y) in slots_to_imgs.keys():
            continue

        if slot_x > 0:
            prev_id = slots_to_imgs[(slot_x - 1, slot_y)][0]

            img1 = slots_to_imgs[(slot_x - 1, slot_y)][1]
            right1 = [p for p in img1[-1]]

            for match in matching[prev_id]:
                img2 = id_to_img[match[0]]
                left2 = [p for p in img2[0]]
                cnt = 0
                this_one = True
                while not is_border_matching(right1, left2):
                    if cnt < 4:
                        img2 = rotate_image(img2, 90)
                    elif cnt < 5:
                        img2 = flip_image_x(img2)
                    elif cnt < 9:
                        img2 = rotate_image(img2, 90)
                    else:
                        this_one = False
                        break

                    left2 = [p for p in img2[0]]

                    cnt += 1

                if not this_one:
                    continue

                add_to_grid(grid, remove_border(img2), slot_x, slot_y)
                slots_to_imgs[(slot_x, slot_y)] = (match[0], img2)
                break

        if slot_x == 0:
            prev_id = slots_to_imgs[(slot_x, slot_y - 1)][0]

            img1 = slots_to_imgs[(slot_x, slot_y - 1)][1]
            bot1 = get_hor_line(img1, n - 1)

            for match in matching[prev_id]:
                img2 = id_to_img[match[0]]
                top2 = get_hor_line(img2, 0)
                cnt = 0
                this_one = True
                while not is_border_matching(bot1, top2):
                    if cnt < 4:
                        img2 = rotate_image(img2, 90)
                    elif cnt < 5:
                        img2 = flip_image_y(img2)
                    elif cnt < 9:
                        img2 = rotate_image(img2, 90)
                    else:
                        this_one = False
                        break

                    top2 = get_hor_line(img2, 0)

                    cnt += 1

                if not this_one:
                    continue

                add_to_grid(grid, remove_border(img2), slot_x, slot_y)
                slots_to_imgs[(slot_x, slot_y)] = (match[0], img2)
                break

sea_monster_str = '                  # \n' \
                  '#    ##    ##    ###\n' \
                  ' #  #  #  #  #  #   '

sea_monster = []
for line in sea_monster_str.split('\n'):
    sea_monster.append(list(line))

cnt = 0
nbr_sea_monster = 0
while True:
    for y in range(len(grid) - len(sea_monster)):
        for x in range(len(grid) - len(sea_monster[0])):
            sea_monster_ok = True
            for sea_y in range(len(sea_monster)):
                for sea_x in range(len(sea_monster[0])):
                    if sea_monster[sea_y][sea_x] == ' ':
                        continue
                    if grid[x + sea_x][y + sea_y] != sea_monster[sea_y][sea_x]:
                        sea_monster_ok = False
                        break
                if not sea_monster_ok:
                    break

            if sea_monster_ok:
                nbr_sea_monster += 1
    if nbr_sea_monster > 0:
        break

    if cnt < 4:
        grid = rotate_image(grid, 90)
    elif cnt < 5:
        grid = flip_image_x(grid)
    elif cnt < 9:
        grid = rotate_image(grid, 90)
    else:
        break

    cnt += 1

hashtag_cnt = 0
for y in range(len(grid)):
    for x in range(len(grid)):
        if grid[x][y] == '#':
            hashtag_cnt += 1

sea_monst_hashtag_cnt = 15

print(f'Part 2: {hashtag_cnt - nbr_sea_monster * sea_monst_hashtag_cnt}')
