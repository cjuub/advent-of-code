from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open("r").readlines()]

dirs = {"/": {"name": "/", "dir": True, "children": {}}}
curr_path = []
for i, line in enumerate(lines):
    if line.startswith("$ cd"):
        d = line.split(" ")[2]
        if d == "..":
            curr_path = curr_path[:-1]
        else:
            if d == "/":
                curr_path = ["/"]
            else:
                curr_path.append(d)
    elif line.startswith("$ ls"):
        contents = []
        for j, ls_res in enumerate(lines[i+1:]):
            if ls_res.startswith("$"):
                i += j
                break
            s = ls_res.split(" ")
            size = s[0]
            name = s[1]
            try:
                size = int(size)
                curr_node = dirs
                for d in curr_path:
                    curr_node = curr_node[d]["children"]
                curr_node[name] = {"name": name, "dir": False, "size": size, "children": {}}
            except:
                curr_node = dirs
                for d in curr_path:
                    curr_node = curr_node[d]["children"]
                curr_node[name] = {"name": name, "dir": True, "children": {}}


def find_directory_nodes(node, depth, directory_nodes):
    # print("  " * depth + "- " + node["name"] + (" (dir)" if node["dir"] else f" (file, size={node['size']})"))
    if not node["dir"]:
        return

    directory_nodes.append(node)

    for child_name in node["children"]:
        find_directory_nodes(node["children"][child_name], depth + 1, directory_nodes)

    return directory_nodes


def find_directory_size(node):
    if not node["dir"]:
        return node["size"]

    dir_size = 0
    for child_name in node["children"]:
        dir_size += find_directory_size(node["children"][child_name])

    return dir_size


directory_nodes = find_directory_nodes(dirs["/"], 0, [])

tot_size = 0
for directory_node in directory_nodes:
    size = find_directory_size(directory_node)
    if size <= 100000:
        tot_size += size

print(f"Part 1: {tot_size}")

free_space = 70000000 - find_directory_size(dirs["/"])
candidates = []
for directory_node in directory_nodes:
    size = find_directory_size(directory_node)
    if free_space + size >= 30000000:
        candidates.append(size)

candidates.sort()
print(f"Part 2: {candidates[0]}")
