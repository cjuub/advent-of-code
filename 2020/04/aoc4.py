#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

passports = []
passport = {}
for line in lines:
    line = line.strip()
    if line == '':
        passports.append(passport)
        passport = {}
        continue
        
    data = line.split(' ')

    for d in data:
        d2 = d.split(':')
        passport[d2[0]] = d2[1]

passports.append(passport)

cnt1 = 0
cnt2 = 0
for passport in passports:
    valid = True
    ok = True

    all = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    for a in all:
        if a not in passport.keys():
            valid = False

            break

    if valid:
        if not (len(passport['byr']) == 4 and int(passport['byr']) >= 1920 and int(passport['byr']) <= 2002):
            ok = False

        if not (len(passport['iyr']) == 4 and int(passport['iyr']) >= 2010 and int(passport['iyr']) <= 2020):
            ok = False

        if not (len(passport['eyr']) == 4 and int(passport['eyr']) >= 2020 and int(passport['eyr']) <= 2030):
            ok = False

        if passport['hgt'].endswith('in'):
            if passport['hgt'][:-2].isnumeric():
                if not (int(passport['hgt'][:-2]) >= 59 and int(passport['hgt'][:-2]) <= 76):
                    ok = False
            else:
                ok =False
        elif passport['hgt'].endswith('cm'):
            if passport['hgt'][:-2].isnumeric():
                if not (int(passport['hgt'][:-2]) >= 150 and int(passport['hgt'][:-2]) <= 193):
                    ok = False
            else:
                ok =False
        else:
            ok = False

        if passport['hcl'].startswith('#') and len(passport['hcl']) == 7:
            l = 'abcdef0123456789'
            for b in passport['hcl'][1:]:
                if b not in l:
                    ok = False
        else:
            ok = False

        if passport['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            ok = False

        if not (len(passport['pid']) == 9 and passport['pid'].isnumeric()):
            ok = False

    if valid and ok:
        cnt1 += 1
        cnt2 += 1
    elif valid:
        cnt1 += 1

print('Part 1: {}'.format(cnt1))
print('Part 2: {}'.format(cnt2))
