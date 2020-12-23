#!/usr/bin/env python3

# input = '389125467'
input = '562893147'

cups = [int(x) for x in list(input)]
curr = 0
n = len(input)
for i in range(100):
    curr_label = cups[curr]
    removed = []
    for j in range(3):
        removed.append(cups.pop((curr + 1) % (n - j)))
        curr = cups.index(curr_label)

    curr = cups.index(curr_label)
    label = cups[curr]
    while True:
        if label - 1 in removed:
            label -= 1
        elif label - 1 in cups:
            dest_label = label - 1
            break
        elif label - 1 < min(cups):
            label = max(cups) + 1
        else:
            raise Exception('rip')

    for j in range(3):
        cups.insert(cups.index(dest_label) + 1, removed.pop())

    curr = (cups.index(curr_label) + 1) % n

res = ''
curr = cups.index(1) + 1
while True:
    if cups[curr % n] == 1:
        break
    res += str(cups[curr % n])
    curr += 1

print(f'Part 1: {res}')


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.mapper = {}

    def add(self, val):
        node = Node(val)
        if self.first is None:
            node.next = node
            node.prev = node
            self.first = node
            self.last = node
        else:
            node.prev = self.last
            node.next = self.first
            self.first.prev = node
            self.last.next = node
            self.last = node
        self.mapper[val] = node
    
    def pop_right(self, n: Node):
        if n.next == self.last:
            ret = self.last.val
            self.last = n
            self.last.next = self.first
            return ret
        elif n.next == self.first:
            ret = self.first.val
            self.first = self.first.next
            self.first.prev = n
            n.next = self.first
            return ret
        else:
            ret = n.next.val
            n.next = n.next.next
            n.next.prev = n
            return ret

    def find(self, val):
        return self.mapper[val]
    
    def insert_right(self, n: Node, val):
        if n == self.last:
            return self.add(val)
        new = Node(val)
        new.next = n.next
        new.prev = n
        n.next = new
        new.next.prev = new
        self.mapper[new.val] = new
        
    def __repr__(self):
        res = '['
        n = self.first
        while n != self.last:
            res += str(n.val) + ', '
            n = n.next
        res += str(self.last.val) + ']'

        return res


cups = LinkedList()
for c in [int(x) for x in list(input)]:
    cups.add(c)

for i in range(10, 1000000 + 1):
    cups.add(i)

min = 1
max = 1000000
curr = cups.first
for i in range(10000000):
    removed = []
    for j in range(3):
        removed.append(cups.pop_right(curr))
    
    label = curr.val
    while True:
        if label - 1 in removed:
            label -= 1
        elif label - 1 < min:
            label = max + 1
        else:
            dest_label = label - 1
            break
            
    dest_node = cups.find(dest_label)
    for j in range(3):
        cups.insert_right(dest_node, removed.pop())

    curr = curr.next

cup1 = cups.find(1).next
cup2 = cup1.next
print(f'Part 2: {cup1.val*cup2.val}')
