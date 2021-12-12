from pathlib import Path

lines = [x.strip() for x in Path("input.txt").open().readlines()]

graph = {}
for line in lines:
    s, d = line.split('-')
    if s not in graph.keys():
        graph[s] = []
    if d not in graph.keys():
        graph[d] = []

    graph[s].append(d)
    graph[d].append(s)


def visit(g, n, path, paths):
    path.append(n)
    if n == 'end':
        paths.append(path)
        return

    for p in g[n]:
        if p.islower():
            if p in path:
                continue
            else:
                visit(g, p, path.copy(), paths)
        else:
            visit(g, p, path.copy(), paths)


paths = []
visit(graph, 'start', [], paths)
print(f"Part 1: {len(paths)}")


def visit2(g, n, path, used, paths):
    path.append(n)
    if n == 'end':
        paths.append(path)
        return

    for p in g[n]:
        if p.islower():
            if p == 'start':
                continue
            if path.count(p) == 1 and not used:
                visit2(g, p, path.copy(), True, paths)
            elif path.count(p) == 1 and used:
                continue
            elif path.count(p) == 2:
                continue
            else:
                visit2(g, p, path.copy(), used, paths)
        else:
            visit2(g, p, path.copy(), used, paths)

paths = []
visit2(graph, 'start', [], False, paths)
print(f"Part 2: {len(paths)}")
