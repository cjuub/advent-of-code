#!/usr/bin/env python3
import math

with open('input.txt') as fp:
    lines = fp.readlines()

reqs = {}
for line in lines:
    mat = line.split('=>')[1].strip()
    mat_name = mat.split(' ')[1]
    mat_amount = mat.split(' ')[0]

    mat_reqs = []
    mat_reqs_tmp = line.split('=>')[0].strip()
    mat_reqs_tmp = mat_reqs_tmp.split(', ')
    for mat_req in mat_reqs_tmp:
        mat_reqs.append((mat_req.split(' ')[1], int(mat_req.split(' ')[0])))

    reqs[mat_name] = (mat_amount, mat_reqs)


def find_req(reqs, req, wanted, excess):
    if req == 'ORE':
        return wanted

    if req in excess.keys():
        wanted -= excess[req]
        excess[req] = 0

    curr_needed = int(reqs[req][0])
    multiplier = int(math.ceil(wanted / curr_needed))
    excess.setdefault(req, 0)
    excess[req] += multiplier * curr_needed - wanted
    sum_req_wanted = 0
    for curr_req in reqs[req][1]:
        req_wanted = find_req(reqs, curr_req[0], curr_req[1] * multiplier, excess)
        sum_req_wanted += req_wanted

    return sum_req_wanted


print('Part 1: ' + str(find_req(reqs, 'FUEL', 1, {})))

for i in range(1120000, 10000000):
    res = find_req(reqs, 'FUEL', i, {})
    if res > 1000000000000:
        print('Part 2: ' + str(i - 1))
        break
