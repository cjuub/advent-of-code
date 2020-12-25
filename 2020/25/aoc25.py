#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

# card_public = 5764801
# door_public = 17807724

card_public = int(lines[0].strip())
door_public = int(lines[1].strip())

card_loop_size = 0
door_loop_size = 0

subject_nbr = 7
val = 1
for loop_size in range(100000000):
    val = (val * subject_nbr) % 20201227
    if val == card_public and card_loop_size == 0:
        card_loop_size = loop_size + 1
    elif val == door_public and door_loop_size == 0:
        door_loop_size = loop_size + 1

    if card_loop_size > 0 and door_loop_size > 0:
        break


val = 1
for i in range(card_loop_size):
    val = (val * door_public) % 20201227

print(f'Part 1: {val}')