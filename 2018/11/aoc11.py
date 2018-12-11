#!/usr/bin/env python3

input = '2694'

size = 300
grid = [[0 for y in range(size)] for x in range(size)]

for y in range(size):
    for x in range(size):
        rackid = x + 1 + 10
        try:
            val = int(str((rackid * (y + 1) + int(input)) * rackid)[-3])
        except:
            val = 0

        val -= 5
        grid[x][y] = val


max_square = -99999999

max_grudsz = -1
last_sizes = {}
max_y = -1
max_x = -1
first = True

#for gridsz in range(2, 3): # solution 1
for gridsz in range(size): # solution 2
    print(gridsz)
    for y in range(size - gridsz):
        for x in range(size - gridsz):
            last_sizes.setdefault(str(x) + ',' + str(y), 0)
            sum = last_sizes[str(x) + ',' + str(y)]

            if not first:
                for i in range(x + gridsz, x + gridsz + 1):
                    for j in range(y, y + gridsz):
                        sum += grid[i][j]

                for i in range(x, x + gridsz):
                    for j in range(y + gridsz, y + gridsz + 1):
                        sum += grid[i][j]
            else:
                for i in range(y, y + gridsz + 1):
                    for j in range(x, x + gridsz + 1):
                        sum += grid[i][j]

            last_sizes[str(x) + ',' + str(y)] = sum
            if sum > max_square:
                max_square = sum
                max_x = x + 1
                max_y = y + 1
                max_grudsz = gridsz + 1


    first = False

print(str(max_x) + ',' + str(max_y) + ' ' + str(max_square) + ' ' + str(max_grudsz))
