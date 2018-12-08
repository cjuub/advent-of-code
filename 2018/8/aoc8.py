#!/usr/bin/env python3


global metadata_cnt
metadata_cnt = 0


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def __repr__(self):
        return 'children: ' + str(self.children) + ' metadata: ' + str(self.metadata)


def build_tree(tree, data, node_index: int) -> int:
    global metadata_cnt

    nbr_children = data[node_index]
    nbr_metadata = data[node_index + 1]

    if nbr_children == 0:
        metadata = [data[node_index + 2 + i] for i in range(nbr_metadata)]
        for i in metadata:
            metadata_cnt += i
        tree[node_index] = Node([], metadata)

        return node_index + 2 + len(metadata)

    curr_index = node_index + 2
    children = []
    for _ in range(nbr_children):
        children.append(curr_index)
        curr_index = build_tree(tree, data, curr_index)

    metadata = [data[curr_index + i] for i in range(nbr_metadata)]

    for i in metadata:
        metadata_cnt += i

    tree[node_index] = Node(children, metadata)
    return curr_index + len(metadata)


def valueof(node: Node):
    if len(node.children) == 0:
        sum = 0
        for metadata in node.metadata:
            sum += metadata

        return sum

    sum = 0
    for metadata in node.metadata:
        if metadata <= len(node.children):
            sum += valueof(tree[node.children[metadata - 1]])
    return sum


license = []
with open('input.txt') as fp:
    for line in fp:
        for entry in line.split(' '):
            license.append(int(entry))

tree = {}
node_index = 0
build_tree(tree, license, node_index)

print(metadata_cnt)
print(valueof(tree[node_index]))
