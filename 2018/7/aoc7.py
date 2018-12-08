#!/usr/bin/env python3


reqs = {}
with open('input.txt') as fp:
    for line in fp:
        before = line.split(' ')[1]
        after = line.split(' ')[7]
        
        reqs.setdefault(before, [])
        reqs[before].append(after)

reqs_orig = dict(reqs)

order = ''
while not len(reqs) == 0:
    avails = []
    depends = set()
    for key, val in reqs.items():
        for dep in val:
            depends.add(dep)

    for key, val in reqs.items():
        if key not in depends:
            avails.append(key)

    avails = sorted(avails)

    del reqs[avails[0]]

    order += avails[0]

    if len(reqs) == 0:
        depends = sorted(depends)
        for dep in depends:
            order += dep


print(order)

reqs = dict(reqs_orig)
avails_order = []
deps = {}
times = {}
for i in range(1, 27):
    times[chr(ord('A') + i - 1)] = 60 + i


while not len(reqs) == 0:
    avails = []
    depends = set()
    for key, val in reqs.items():
        for dep in val:
            depends.add(dep)
            deps.setdefault(dep, set())

            deps[dep].add(key)

    for key, val in reqs.items():
        if key not in depends:
            avails.append(key)

    avails = sorted(avails)
    avails_order.append(avails)

    for avail in avails:
        del reqs[avail]

    if len(reqs) == 0:
        depends = sorted(depends)
        avails_order.append(depends)

seconds = []

start_time = 0
complete_times = {}
for tasks in avails_order:
    for task in tasks:
        deps.setdefault(task, set())

        # earliest time this task can begin due to deps
        start_time = 0
        for dep in deps[task]:
            start_time = max(start_time, complete_times[dep] + 1)

        # earliest time this task can begin due to free slots
        for second in range(start_time, start_time + times[task]):
            if second == len(seconds):
                seconds.append([False, False, False, False, False])
            one_free = False
            for slot in seconds[second]:
                if not slot:
                    one_free = True
                    break
            start_time = max(start_time, second)

            if one_free:
                break

        # print('task ' + task + ' from ' + str(start_time) + ' to ' + str(start_time + times[task] - 1))
        for second in range(start_time, start_time + times[task]):
            if second == len(seconds):
                seconds.append([False, False, False, False, False])
            for slot in range(len(seconds[0])):
                if not seconds[second][slot]:
                    seconds[second][slot] = True
                    break

        complete_times[task] = start_time + times[task] - 1


print(len(seconds))

