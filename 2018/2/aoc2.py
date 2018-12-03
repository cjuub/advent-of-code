#!/usr/bin/env python3

twos = 0
threes = 0
boxes = []
with open('input.txt') as fp:
    for line in fp:
        letter_count_map = {}
        for letter in line:
            if not letter_count_map.get(letter, None):
                letter_count_map[letter] = 0

            letter_count_map[letter] += 1
        
        has_twos = False
        has_threes = False
        for cnt in letter_count_map.values():
            if cnt == 2:
                has_twos = True
            elif cnt == 3:
                has_threes = True
        
        twos = twos + 1 if has_twos else twos
        threes = threes + 1 if has_threes else threes

        if has_twos or has_threes:
            boxes.append(line)

print(twos * threes)

correct_ids = []
for box1 in boxes:
    for box2 in boxes:
        diffing_letters = 0
        for j in range(0, len(max(box1, box2))):
            if box1[j] != box2[j]:
                diffing_letters += 1

        if diffing_letters == 1:
            correct_ids.append(box1)

answer = ''
first = correct_ids[0]
second = correct_ids[1]
for i in range(0, len(max(first, second))):
    if first[i] == second[i]:
        answer += first[i]

print(answer)

