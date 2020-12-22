#!/usr/bin/env python3

with open('input.txt') as fp:
    lines = fp.readlines()

all_ingredients = set()
all_allergens = set()
foods = []
for line in lines:
    line = line.strip()
    
    ingredients = set(line.split('(')[0].strip().split(' '))
    allergens = set(line.split('(contains ')[1][:-1].split(', '))

    all_ingredients.update(ingredients)
    all_allergens.update(allergens)
    
    foods.append((ingredients, allergens))
    
all_candidates = set()
for a in all_allergens:
    candidates = set()
    not_its = set()
    for ingredients, allergens in foods:
        if a in allergens:
            if not candidates:
                candidates.update(ingredients)
            else:
                candidates = candidates.intersection(ingredients)

    all_candidates.update(candidates)
    
no_allergens = all_ingredients.difference(all_candidates)
    
cnt = 0
for i in no_allergens:
    for ingredients, allergens in foods:
        if i in ingredients:
            cnt += 1

print(f'Part 1: {cnt}')

for i, (ingredients, allergens) in enumerate(foods):
    ingredients = ingredients.difference(no_allergens)
    foods[i] = (ingredients, allergens)

solution = {}
while len(solution) != len(all_allergens):
    for a in all_allergens:
        candidates = set()
        for ingredients, allergens in foods:
            if a in allergens:
                if not candidates:
                    candidates.update(ingredients)
                else:
                    candidates = candidates.intersection(ingredients)
        if len(candidates) == 1:
            solution[a] = candidates.pop()
            for i, (ingredients, allergens) in enumerate(foods):
                if solution[a] in ingredients:
                    ingredients.remove(solution[a])
                if a in allergens:
                    allergens.remove(a)

                foods[i] = (ingredients, allergens)
            break
res = ''
for a in sorted(solution.keys()):
    res += solution[a] + ','

print(f'Part 2: {res[:-1]}')