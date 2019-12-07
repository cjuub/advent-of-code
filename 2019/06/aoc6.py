#!/usr/bin/env python3


def calc_orbit_chain(chain, obj):
    chain.append(obj)
    if obj == 'COM':
        return chain
    return calc_orbit_chain(chain, parents[obj])


with open('input.txt') as fp:
    lines = fp.readlines()

unique = set()
parents = {}
nbr_orbits = 0
parents['COM'] = None
for line in lines:
    orb1 = line.split(')')[0].strip()
    orb2 = line.split(')')[1].strip()

    unique.add(orb2)
    unique.add(orb1)
    parents[orb2] = orb1

orbit_chains = []
for obj in unique:
    parent = parents[obj]
    while parent != 'COM' and parent is not None:
        orbit_chain = []
        orbit_chains.append(calc_orbit_chain(orbit_chain, obj))
        parent = parents[obj]
        obj = parent

print('Part 1: ' + str(len(orbit_chains) + 1))

you_chain = []
you_chain = calc_orbit_chain(you_chain, 'YOU')
san_chain = []
san_chain = calc_orbit_chain(san_chain, 'SAN')

first_common = ''
for obj in you_chain:
    if obj in san_chain:
        first_common = obj
        break

first_common_chain = []
first_common_chain = calc_orbit_chain(first_common_chain, first_common)

san_chain = set(san_chain).difference(set(first_common_chain))
you_chain = set(you_chain).difference(set(first_common_chain))
you_chain.remove('YOU')
san_chain.remove('SAN')
you_chain.update(san_chain)

print('Part 2: ' + str(len(you_chain)))
