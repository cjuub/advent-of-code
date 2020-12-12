#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

navs = []
for line in lines:
    line = line.strip()
    navs.append((line[:1], int(line[1:])))


pos_e = 0
pos_n = 0
angle = 0
curr_dir = 'E'
for nav in navs:
    if nav[0] == 'N':
        pos_n += nav[1]
    elif nav[0] == 'S':
        pos_n -= nav[1]
    elif nav[0] == 'W':
        pos_e -= nav[1]
    elif nav[0] == 'E':
        pos_e += nav[1]
    elif nav[0] == 'L':
        angle += nav[1]

        if angle >= 360:
            angle = angle - 360

        if 0 <= angle < 90:
            curr_dir = 'E'
        if 90 <= angle < 180:
            curr_dir = 'N'
        if 180 <= angle < 270:
            curr_dir = 'W'
        if 270 <= angle < 360:
            curr_dir = 'S'
    elif nav[0] == 'R':
        angle -= nav[1]
        
        if angle < 0:
            angle = angle + 360

        if 0 <= angle < 90:
            curr_dir = 'E'
        if 90 <= angle < 180:
            curr_dir = 'N'
        if 180 <= angle < 270:
            curr_dir = 'W'
        if 270 <= angle < 360:
            curr_dir = 'S'
    elif nav[0] == 'F':
        if curr_dir == 'N':
            pos_n += nav[1]
        elif curr_dir == 'S':
            pos_n -= nav[1]
        elif curr_dir == 'W':
            pos_e -= nav[1]
        elif curr_dir == 'E':
            pos_e += nav[1]

print('Part 1: {}'.format(abs(pos_e) + abs(pos_n)))

pos_e = 0
pos_n = 0
angle = 0
way_e = 10
way_n = 1
for nav in navs:
    if nav[0] == 'N':
        way_n += nav[1]
    elif nav[0] == 'S':
        way_n -= nav[1]
    elif nav[0] == 'W':
        way_e -= nav[1]
    elif nav[0] == 'E':
        way_e += nav[1]
    elif nav[0] == 'L':
        a = nav[1]
        while a != 0:
            angle += 90
        
            if angle >= 360:
                angle = angle - 360

            if 0 <= angle < 90:
                tmp = way_n
                way_n = way_e
                way_e = -tmp
            if 90 <= angle < 180:
                tmp = way_n
                way_n = way_e
                way_e = -tmp
            if 180 <= angle < 270:
                tmp = way_n
                way_n = way_e
                way_e = -tmp
            if 270 <= angle < 360:
                tmp = way_n
                way_n = way_e
                way_e = -tmp
                
            a -= 90

    elif nav[0] == 'R':
        a = nav[1]
        while a != 0:
            angle -= 90

            if angle < 0:
                angle = angle + 360

            if 0 <= angle < 90:
                tmp = way_n
                way_n = -way_e
                way_e = tmp
            if 90 <= angle < 180:
                tmp = way_n
                way_n = -way_e
                way_e = tmp
            if 180 <= angle < 270:
                tmp = way_n
                way_n = -way_e
                way_e = tmp
            if 270 <= angle < 360:
                tmp = way_n
                way_n = -way_e
                way_e = tmp

            a -= 90
    elif nav[0] == 'F':
        pos_n += nav[1] * way_n
        pos_e += nav[1] * way_e

print('Part 2: {}'.format(abs(pos_e) + abs(pos_n)))

