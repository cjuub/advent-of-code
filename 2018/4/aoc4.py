#!/usr/bin/env python3


entries = []
with open('input.txt') as fp:
    for line in fp:
        entries.append(line)
        
entries = sorted(entries)

curr_guard = -1
start_time = -1
end_time = -1
minute_map = {}
sleepmap = {}
for entry in entries:
    if 'Guard' in entry:
        curr_guard = int(entry.split()[3][1:])
        minute_map.setdefault(curr_guard, {})
    elif 'asleep' in entry:
        start_time = int(entry.split()[1].split(':')[1][:-1])
    elif 'wakes' in entry:
        end_time = int(entry.split()[1].split(':')[1][:-1])

        sleepmap.setdefault(curr_guard, 0)
        sleepmap[curr_guard] += end_time - start_time

        for i in range(start_time, end_time):
            minute_map[curr_guard].setdefault(i, 0)
            minute_map[curr_guard][i] += 1


max_sleep = -1
sleepiest_guard = -1
for guard, time in sleepmap.items():
    if time > max_sleep:
        max_sleep = time
        sleepiest_guard = guard

minutes = minute_map[sleepiest_guard]
max_count = -1
selected_minute = -1
for minute, count in minutes.items():
    if count > max_count:
        max_count = count 
        selected_minute = minute

print(str(sleepiest_guard * selected_minute))


highest_count = -1
selected_minute = -1
selected_guard = -1
for guard, minutes in minute_map.items():
    for minute, count in minutes.items():
        if count > highest_count:
            highest_count = count
            selected_guard = guard
            selected_minute = minute

print(str(selected_guard * selected_minute))

